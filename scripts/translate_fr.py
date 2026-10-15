#!/usr/bin/env python3
"""Build the French twin of every Programming01 notebook and slide deck.

The English files stay the only source. Their prose is translated once, stored in
a translation memory (`translations/fr.json`, one entry per Markdown cell or per
slide, keyed by a hash of the English text), and the French files are generated
from that memory. Re-running the script translates only what changed, so the
corrections made by hand in the memory survive every rebuild: that is the whole
point of keeping the French in a JSON file instead of in the notebooks.

  python_types.ipynb -> python_types-fr.ipynb
  slides.md          -> slides-fr.md   (and `make slides` turns it into a .pptx)

Code cells are copied as they are: identifiers, strings and outputs stay English,
on purpose, because that is what the students will see in their own terminal. The
SVG header cells and the image only cells are copied too.

Usage:
  translate_fr.py                      # fill the memory, write the French files
  translate_fr.py --engine argos       # offline and open source, after one install
  translate_fr.py --engine none        # no call at all: build from the memory only
  translate_fr.py --status             # what is translated, what is missing
  translate_fr.py --force Session04    # translate the Session04 strings again
  translate_fr.py --prune              # drop the entries no file uses

Engines: google (the default, free, no account) and argos (free, open source,
offline) cost nothing. deepl (DEEPL_API_KEY) and claude (ANTHROPIC_API_KEY) are
there for a better pass later, and read the same memory file.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha1
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS = "Programming01/Session*/*.ipynb"
DECKS = "Programming01/Session*/slides.md"
MEMORY = ROOT / "translations" / "fr.json"
GLOSSARY = ROOT / "translations" / "glossary.fr.json"
FIXUPS = ROOT / "translations" / "fixups.fr.json"
SUFFIX = "-fr"

CLAUDE_MODEL = "claude-sonnet-5-5"
CLAUDE_URL = "https://api.anthropic.com/v1/messages"
DEEPL_URL = "https://api-free.deepl.com/v2/translate"
GOOGLE_URL = "https://translate.googleapis.com/translate_a/single"
WORKERS = 3
ATTEMPTS = 3

SYSTEM = """\
You translate teaching material from English into French, for a French master's \
programme in digital health (Mastère Spécialisé Santé Numérique). The text is one \
Markdown cell of a Jupyter notebook, or one slide of a deck, from a Python course.

Rules:
1. Answer with the translated Markdown and nothing else: no preamble, no comment, \
no code fence around the answer.
2. Reproduce every code span between backticks exactly, byte for byte. Never \
translate a Python identifier, a method name, a library name, a file name, a column \
name or a shell command, inside backticks or outside them.
3. Reproduce every LaTeX formula between dollar signs exactly, every Markdown link \
or image target `](...)` exactly, and every `::: notes` fence exactly.
4. Keep the Markdown structure: the same heading levels, the same list markers, the \
same line breaks, the same bold and italic.
5. Address the student with "vous", and keep the tone of the original (direct, \
concrete, no padding).
6. Do not use dashes (-, –, —) as punctuation in the prose: use commas or \
parentheses.
7. Translate the prose only. If a text contains no prose, return it unchanged.
"""


# ============================================================ translation memory
def load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def key_of(text: str) -> str:
    """The memory key of a string: a hash of the English, whitespace stripped."""
    return sha1(text.strip().encode("utf-8")).hexdigest()[:12]


def is_prose(text: str) -> bool:
    """Is this worth translating, or is it only a logo, an image or blank?"""
    stripped = text.strip()
    if not stripped:
        return False
    if stripped.startswith(("<svg", "<div", "<img", "<table")):
        return False
    if re.fullmatch(r"!?\[[^\]]*\]\([^)]*\)", stripped):
        return False
    naked = re.sub(r"```.*?```|`[^`]*`", "", stripped, flags=re.S)
    return bool(re.search(r"[A-Za-z]{3,}", naked))


# ============================================================== what to protect
KEEP = r"```.*?```|`[^`\n]+`|\$[^$\n]+\$|\]\([^)]*\)|^:::[^\n]*$"
SLOT = "⟦{}⟧"  # the brackets a translator leaves alone, tested on every engine


def protected(text: str) -> list[str]:
    """The pieces a translation must reproduce exactly, used to check the answer."""
    return sorted(re.findall(KEEP, text, flags=re.S | re.M))


def checked(english: str, french: str) -> bool:
    return protected(english) == protected(french)


def mask(text: str) -> tuple[str, list[str]]:
    """Replace the code, the formulas, the link targets and the fences by slots.

    A plain translation engine has no idea that `df["age"]` must come back
    untouched, so it never sees it: it translates the prose around the slots.
    """
    pieces: list[str] = []

    def take(match: re.Match[str]) -> str:
        pieces.append(match.group(0))
        return SLOT.format(len(pieces) - 1)

    return re.sub(KEEP, take, text, flags=re.S | re.M), pieces


def unmask(text: str, pieces: list[str]) -> str:
    for i, piece in enumerate(pieces):
        text = text.replace(SLOT.format(i), piece)
    return text


def repair(text: str) -> str:
    """Put back the Markdown an engine likes to nibble at.

    Google drops the space after a `##` now and then, or replaces it by a non
    breaking space, and pandoc then prints a literal `##Titre` on the slide.
    """
    return re.sub(r"(?m)^(#{1,6})[ \u00a0]*(?=\S)", r"\1 ", text)


def fixed(text: str) -> str:
    """Apply the standing corrections: the mistakes a plain engine keeps making.

    `translations/fixups.fr.json` is a plain string to string map, applied to every
    machine answer. Add an entry when you correct the same word for the third time.
    """
    pairs = load_json(FIXUPS, {}).items()
    for wrong, right in sorted(pairs, key=lambda kv: -len(kv[0])):
        text = text.replace(wrong, right)
    return text


def masked(engine):
    """Wrap an engine that cannot be told what to leave alone."""

    def translate(text: str, glossary: dict[str, str], model: str) -> str:
        hidden, pieces = mask(text)
        answer = repair(engine(hidden, glossary, model))
        return fixed(unmask(answer, pieces).strip())

    return translate


# ===================================================================== engines
def _get(url: str):
    """One HTTP GET, retried on the errors that are worth retrying."""
    for attempt in range(ATTEMPTS):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(request, timeout=60) as response:
                return json.loads(response.read())
        except urllib.error.HTTPError as error:
            if error.code not in (408, 429, 500, 502, 503) or attempt == ATTEMPTS - 1:
                raise RuntimeError(f"{error.code} {error.reason}") from error
        except urllib.error.URLError as error:
            if attempt == ATTEMPTS - 1:
                raise RuntimeError(str(error)) from error
        time.sleep(3 * (attempt + 1))
    raise RuntimeError("unreachable")


def _post(url: str, data: bytes, headers: dict[str, str]) -> dict:
    """One HTTP POST, same retry policy."""
    for attempt in range(ATTEMPTS):
        try:
            request = urllib.request.Request(url, data=data, headers=headers)
            with urllib.request.urlopen(request, timeout=120) as response:
                return json.loads(response.read())
        except urllib.error.HTTPError as error:
            if error.code not in (408, 429, 500, 502, 503, 529) or attempt == ATTEMPTS - 1:
                raise RuntimeError(f"{error.code} {error.read()[:400].decode()}") from error
        except urllib.error.URLError as error:
            if attempt == ATTEMPTS - 1:
                raise RuntimeError(str(error)) from error
        time.sleep(2 ** attempt)
    raise RuntimeError("unreachable")


def translate_google(text: str, glossary: dict[str, str], model: str) -> str:
    """The free endpoint of Google Translate: no account, no key, no quota to sign.

    It is the unofficial one the web page itself calls, so it can rate limit or
    change shape; the script retries, and every answer is checked afterwards.
    """
    query = urllib.parse.urlencode(
        {"client": "gtx", "sl": "en", "tl": "fr", "dt": "t", "q": text}
    )
    answer = _get(f"{GOOGLE_URL}?{query}")
    return "".join(segment[0] for segment in answer[0] if segment[0])


def translate_argos(text: str, glossary: dict[str, str], model: str) -> str:
    """Argos Translate: open source, offline, no account at all.

    Needs `uv pip install argostranslate`; the first call downloads the en -> fr
    model (about 100 MB) into ~/.local/share/argos-translate.
    """
    try:
        import argostranslate.package
        import argostranslate.translate
    except ImportError:
        raise SystemExit("argos engine: uv pip install argostranslate") from None
    if not any(
        lang.code == "fr" for lang in argostranslate.translate.get_installed_languages()
    ):
        argostranslate.package.update_package_index()
        package = next(
            p
            for p in argostranslate.package.get_available_packages()
            if p.from_code == "en" and p.to_code == "fr"
        )
        argostranslate.package.install_from_path(package.download())
    return argostranslate.translate.translate(text, "en", "fr")


def translate_deepl(text: str, glossary: dict[str, str], model: str) -> str:
    key = os.environ.get("DEEPL_API_KEY")
    if not key:
        raise SystemExit("DEEPL_API_KEY is not set (try --engine google)")
    payload = urllib.parse.urlencode(
        {
            "text": text,
            "source_lang": "EN",
            "target_lang": "FR",
            "preserve_formatting": "1",
        }
    ).encode("utf-8")
    answer = _post(
        DEEPL_URL,
        payload,
        {
            "Authorization": f"DeepL-Auth-Key {key}",
            "content-type": "application/x-www-form-urlencoded",
        },
    )
    return answer["translations"][0]["text"]


def translate_claude(text: str, glossary: dict[str, str], model: str) -> str:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise SystemExit("ANTHROPIC_API_KEY is not set (try --engine google)")
    terms = "\n".join(f"{en} -> {fr}" for en, fr in sorted(glossary.items()))
    payload = {
        "model": model,
        "max_tokens": 4000,
        "system": SYSTEM + f"\nGlossary, to use consistently:\n{terms}\n",
        "messages": [{"role": "user", "content": text}],
    }
    answer = _post(
        CLAUDE_URL,
        json.dumps(payload).encode("utf-8"),
        {
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
    )
    return "".join(b.get("text", "") for b in answer["content"]).strip()


# claude is told in its prompt what to leave alone; the others are given slots
ENGINES = {
    "google": masked(translate_google),
    "argos": masked(translate_argos),
    "deepl": masked(translate_deepl),
    "claude": translate_claude,
}


# =============================================================== the notebooks
def as_source(text: str) -> list[str]:
    """Back to the nbformat line list: every line keeps its \\n but the last."""
    return text.splitlines(keepends=True) or [""]


def map_notebook(path: Path, convert) -> tuple[str, int, int]:
    """Rewrite every prose Markdown cell of a notebook through `convert`."""
    notebook = json.loads(path.read_text(encoding="utf-8"))
    done = missing = 0
    for cell in notebook["cells"]:
        if cell["cell_type"] != "markdown":
            continue
        text = "".join(cell["source"])
        if not is_prose(text):
            continue
        french = convert(text)
        if french is None:
            missing += 1
            continue
        cell["source"] = as_source(french)
        done += 1
    return json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", done, missing


# =================================================================== the decks
FRONT = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def map_front_matter(front: str, convert) -> tuple[str, int, int]:
    """Translate the title, the subtitle and the date; leave the author alone."""
    out, done, missing, in_title = [], 0, 0, False

    def one(text: str) -> str:
        nonlocal done, missing
        french = convert(text)
        if french is None:
            missing += 1
            return text
        done += 1
        return french

    for line in front.split("\n"):
        field = re.match(r'^(\w+):\s*(.*)$', line)
        if field:
            name, value = field.group(1), field.group(2)
            in_title = name == "title" and value.strip() == "|"
            quoted = re.fullmatch(r'"(.*)"', value)
            if name in ("subtitle", "date") and quoted:
                out.append(f'{name}: "{one(quoted.group(1))}"')
                continue
            out.append(line)
            continue
        if in_title and line.startswith("  ") and line.strip():
            body = line[2:]
            fold = "\\" if body.endswith("\\") else ""
            out.append("  " + one(body[: -1 if fold else None]) + fold)
            continue
        out.append(line)
    return "\n".join(out), done, missing


def map_deck(path: Path, convert) -> tuple[str, int, int]:
    """Rewrite a slides.md: the front matter, then one unit per `##` slide."""
    text = path.read_text(encoding="utf-8")
    head = FRONT.match(text)
    body = text[head.end():] if head else text
    done = missing = 0

    if head:
        front, got, lost = map_front_matter(head.group(1), convert)
        done, missing = done + got, missing + lost
        out = [f"---\n{front}\n---\n"]
    else:
        out = []

    for block in re.split(r"(?m)^(?=## )", body):
        core = block.strip("\n")
        if not is_prose(core):
            out.append(block)
            continue
        french = convert(core)
        if french is None:
            missing += 1
            out.append(block)
            continue
        done += 1
        lead = block[: len(block) - len(block.lstrip("\n"))]
        trail = block[len(block.rstrip("\n")):]
        out.append(lead + french + trail)
    return "".join(out), done, missing


# ======================================================================= files
def sources(selection: list[str]) -> list[Path]:
    """The English files: every notebook and deck that is not a French one."""
    found = [
        p
        for p in sorted([*ROOT.glob(NOTEBOOKS), *ROOT.glob(DECKS)])
        if not p.stem.endswith(SUFFIX)
    ]
    if selection:
        found = [p for p in found if any(s in str(p.relative_to(ROOT)) for s in selection)]
    return found


def rewrite(path: Path, convert) -> tuple[str, int, int]:
    mapper = map_notebook if path.suffix == ".ipynb" else map_deck
    return mapper(path, convert)


def strings_of(paths: list[Path]) -> dict[str, str]:
    """Every distinct English string of those files, by memory key."""
    wanted: dict[str, str] = {}

    def collect(text: str) -> None:
        wanted[key_of(text)] = text
        return None  # nothing is rewritten in this pass

    for path in paths:
        rewrite(path, collect)
    return wanted


def write_french(path: Path, memory: dict[str, dict]) -> tuple[Path | None, int, int]:
    """Write the French twin of one file, unless not one string is translated."""

    def convert(text: str) -> str | None:
        entry = memory.get(key_of(text))
        return entry["fr"] if entry and entry.get("fr") else None

    content, done, missing = rewrite(path, convert)
    if not done:
        return None, 0, missing
    out = path.with_name(f"{path.stem}{SUFFIX}{path.suffix}")
    out.write_text(content, encoding="utf-8")
    return out, done, missing


# ========================================================================= main
def fill_memory(wanted: dict[str, str], memory: dict[str, dict], args) -> int:
    """Translate the strings that are missing from the memory. Returns a count."""
    todo = [
        (k, text)
        for k, text in wanted.items()
        if args.force or k not in memory or not memory[k].get("fr")
    ]
    if not todo:
        return 0
    if args.engine == "none":
        print(f"{len(todo)} strings are not translated yet (--engine none)")
        return 0
    glossary = load_json(GLOSSARY, {})
    engine = ENGINES[args.engine]

    def one(item: tuple[str, str]) -> tuple[str, dict]:
        k, english = item
        french = engine(english, glossary, args.model)
        status = "machine" if checked(english, french) else "check"
        if status == "check":
            # one retry, with the pieces it dropped spelled out
            reminder = (
                english
                + "\n\n[Reproduce exactly, in the same order: "
                + " ".join(protected(english))
                + "]"
            )
            second = engine(reminder, glossary, args.model)
            if checked(english, second):
                french, status = second, "machine"
        label = f"claude:{args.model}" if args.engine == "claude" else args.engine
        return k, {"en": english, "fr": french, "status": status, "engine": label}

    print(f"translating {len(todo)} strings with {args.engine}")
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for i, (k, entry) in enumerate(pool.map(one, todo), start=1):
            memory[k] = entry
            flag = "" if entry["status"] == "machine" else "  <- check by hand"
            first = entry["fr"].strip().splitlines()[0][:60] if entry["fr"].strip() else ""
            print(f"  [{i}/{len(todo)}] {k} {first}{flag}")
    return len(todo)


def main() -> None:
    parser = argparse.ArgumentParser(description="French twin of the course material")
    parser.add_argument("selection", nargs="*", help="only these files (substring)")
    parser.add_argument(
        "--engine",
        choices=[*ENGINES, "none"],
        default="google",
        help="google and argos are free; deepl and claude need an API key",
    )
    parser.add_argument("--model", default=CLAUDE_MODEL, help="claude engine only")
    parser.add_argument("--workers", type=int, default=WORKERS)
    parser.add_argument("--force", action="store_true", help="translate again")
    parser.add_argument("--prune", action="store_true", help="drop the unused entries")
    parser.add_argument("--status", action="store_true", help="report, change nothing")
    args = parser.parse_args()

    paths = sources(args.selection)
    if not paths:
        raise SystemExit("no file matched")
    memory = load_json(MEMORY, {})
    wanted = strings_of(paths)

    if args.status:
        have = sum(1 for k in wanted if memory.get(k, {}).get("fr"))
        check = [k for k in wanted if memory.get(k, {}).get("status") == "check"]
        human = sum(1 for k in wanted if memory.get(k, {}).get("status") == "human")
        decks = sum(1 for p in paths if p.suffix == ".md")
        print(f"{len(paths) - decks} notebooks and {decks} decks, "
              f"{len(wanted)} distinct strings")
        print(f"  translated   {have}/{len(wanted)}")
        print(f"  read by hand {human}")
        print(f"  to check     {len(check)}")
        print(f"  unused in the memory {len([k for k in memory if k not in wanted])}")
        return

    added = fill_memory(wanted, memory, args)
    if args.prune:
        for k in [k for k in memory if k not in wanted]:
            del memory[k]
    if added or args.prune:
        save_json(MEMORY, memory)

    total_missing = 0
    for path in paths:
        out, done, missing = write_french(path, memory)
        total_missing += missing
        where = out.relative_to(ROOT) if out else f"{path.relative_to(ROOT)} (not written)"
        print(f"{where}  {done} in French, {missing} still English")
    if total_missing:
        print(f"\n{total_missing} strings are still English: run again with an engine",
              file=sys.stderr)


if __name__ == "__main__":
    main()
