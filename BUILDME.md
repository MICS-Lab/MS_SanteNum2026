# Building

```bash
make figures            # regenerate the slide illustrations (matplotlib)
make data               # regenerate the synthetic ward export, shared by the sessions
make slides             # slides.md -> slides.pptx (pandoc, then a post-processing pass)
make fr                 # the French twin of every notebook and deck
make fr slides          # and turn every slides-fr.md into a .pptx
make translation-status # how much of the French is done
```

Slides are written in Markdown and converted with `pandoc --slide-level=2`, so every
`##` heading is one slide and every `::: notes` block becomes speaker notes.
`scripts/fit_pptx.py` then patches the result: it enables autofit (pandoc leaves it
off, so long slides silently overflow) and centres `>` blockquotes, which is how a
deck asks the room a question.

The notebooks are written by hand, one per topic, each with a `-solutions` twin that
holds the same Markdown and the filled in code cells. Keep the two in step when you
edit an exercise.

## The French twins

Every `*.ipynb` gets a `*-fr.ipynb` next to it, and every `slides.md` gets a
`slides-fr.md`, built by `scripts/translate_fr.py`. The English file stays the only
source: nothing is ever edited in a French file, because the next build overwrites it.

The French decks are built by the same pandoc rule as the English ones, since
`SLIDE_SOURCES` matches `slides*.md`, so `make fr slides` gives you
`slides-fr.pptx` next to `slides.pptx`.

The translations live in **`translations/fr.json`**, one entry per Markdown cell and
per slide, keyed by a hash of the English text:

```json
"3fd0b1c9a4e7": {
  "en": "Run the cell below: it builds the synthetic ward export ...",
  "fr": "Exécutez la cellule ci-dessous : elle construit l'export ...",
  "status": "machine",
  "engine": "google"
}
```

That file, not the notebooks, is where you correct the French. Set `"status"` to
`"human"` on an entry you have read and fixed: the script never touches an entry that
already has a translation, so your wording survives every rebuild. Because the key is
a hash of the English text, editing an English cell invalidates only that cell, and
the next `make fr` retranslates it alone.

`translations/glossary.fr.json` pins the vocabulary (array, Series, ward, string and
so on) so the same term does not come back three ways in three sessions.

```bash
make fr                                         # translate what changed, rebuild
python3 scripts/translate_fr.py --engine none   # rebuild from the memory, no call
python3 scripts/translate_fr.py --status        # counts, including the cells to check
python3 scripts/translate_fr.py --force Session04   # translate those cells again
python3 scripts/translate_fr.py --prune         # drop the entries no notebook uses
```

What the script does **not** translate: code cells and code fences (identifiers,
strings and outputs stay English, which is what the students see in their own
terminal), the SVG header cells, the cells that are only an image, and the `author`
of a deck. In a `slides.md` the unit is one `##` slide, speaker notes included, and
the `::: notes` fences are protected like code. After each translation it checks that
every backtick span, every `$...$` formula and every link target came back unchanged;
if one did not, it asks the engine once more, and otherwise marks the entry
`"status": "check"` for you to read.

Four engines are available, and they all read and write the same memory:

| engine | cost | what it needs |
|---|---|---|
| `google` (the default) | free | nothing, it is the endpoint the web page calls |
| `argos` | free | `uv pip install argostranslate`, then runs offline, open source |
| `deepl` | free tier | `DEEPL_API_KEY` (500k characters a month, this repository is 34k) |
| `claude` | paid | `ANTHROPIC_API_KEY` |

Only `claude` is told in a prompt what to leave alone. For the other three the script
hides the code spans, the formulas and the link targets behind numbered slots
(`⟦0⟧`) before translating, and puts them back afterwards, so a plain engine
cannot touch them. Everything is called over plain HTTPS, so no engine adds a
dependency, except `argos` which you install yourself.

`translations/fixups.fr.json` is applied to every machine answer: a plain string to
string map for the mistakes an engine keeps making ("trame de données" for DataFrame
and so on). Add an entry when you correct the same word for the third time.

The French files are committed, like `slides.pptx`, so that a student clones
the repository and opens them, with nothing to install and nothing to run.

## Requirements

`pandoc`, and Python with `matplotlib`, `pillow`, `numpy` and `pandas`. The notebooks
need a Jupyter Python kernel, and the Session 3 command line notebook needs a `bash`
on `PATH`. `scripts/translate_fr.py` needs only the standard library, and no account: its
default engine is free.

The French in the repository today is a machine first pass (the `google` engine) with
a handful of entries corrected by hand. `python3 scripts/translate_fr.py --status`
counts what has been read (`"status": "human"`) and what has not.
