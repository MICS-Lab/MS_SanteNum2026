#!/usr/bin/env python3
"""Generate the Programming01 Session01 practical notebook, blank and solved.

Both notebooks are built from the single list of cells below, so the exercise and
its answer can never drift apart: an `answer` is spliced in for the solutions
notebook and replaced by a `# TODO` stub in the student one.

Run from the repository root:
  make_notebook_c01.py [outdir]      (default: Programming01/Session01)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

STUB = "# TODO: write your command here\n"


def md(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": text.strip("\n") + "\n"}


def code(source: str) -> dict:
    return {"cell_type": "code", "execution_count": None, "metadata": {},
            "outputs": [], "source": source.strip("\n") + "\n"}


def ex(answer: str, given: str = "", cd: str = "../data") -> tuple[dict, dict]:
    """An exercise cell: `given` is scaffolding kept in both notebooks.

    `cd` is the folder the shell starts in: `../data` for the exploration parts
    (the export is shared by every session, one level up), and `.` for Part 8,
    which works on a script sitting next to the notebook.
    """
    head = "%%bash\n" + (f"cd {cd}\n" if cd != "." else "")
    blank = code(head + given + STUB)
    solved = code(head + given + answer.strip("\n") + "\n")
    return blank, solved


CELLS: list[dict | tuple[dict, dict]] = [
    md("""
# Session 1. Practical: a whole analysis without leaving the shell

**Digital Health, Mastère Spécialisé · 2026**

You have just been handed `../data/`, one level up from this notebook: a synthetic
export from a hospital ward, shared by every session of this course.
Nobody has told you what is in it. By the end of this notebook you will have
described the cohort, found the broken files, and produced a small summary table,
without opening a single file in an editor, and with a written record of every step.

### How this notebook works

Every code cell starts with `%%bash`, which means *run these lines in a shell*.
Two things to know before you start:

- **`cd` does not persist between cells.** Each `%%bash` cell is a fresh shell that
  starts in this notebook's folder. That is why every cell below begins with
  `cd ../data`. Keep that line when you write your own answers.
- **Run the cell to see the output.** If nothing prints, the command probably
  succeeded and simply had nothing to say. Silence is success in the shell.
- **A failing command shows a `CalledProcessError`.** Every command returns an exit
  code (`0` for success, anything else for failure), and Jupyter turns a non zero
  one into a traceback. Read the output above it: that is where the real message is.

Cells marked **Exercise** contain a `# TODO`. Replace it. The expected shape of the
answer is described just above.
"""),

    md("""
---
## Part 1. Where am I, and what is here?

Three commands answer 90% of "I am lost": `pwd` (where), `ls` (what), `cd` (go).
"""),
    code("""
%%bash
pwd
"""),
    md("""
`ls` lists a folder. On its own it is terse; the flags are what make it useful:

- `-l` one file per line, with size, date and permissions
- `-h` human-readable sizes (`4.0K` instead of `4096`)
- `-a` show hidden files (anything starting with `.`)
- `-t` newest first · `-S` biggest first · `-R` recurse into sub-folders
"""),
    code("""
%%bash
cd ../data
ls
echo "--- and now with details ---"
ls -lh
"""),
    md("""
**Exercise 1.1.** List everything inside `../data/ecg/`, biggest file first, with
human-readable sizes. Only the first 5 lines should print (pipe into `head -5`).
"""),
    ex("ls -lhS ecg/ | head -5"),

    md("""
**Exercise 1.2.** How many files are there in `../data/ecg/`?

`ls` prints one name per line when its output is not a terminal, and `wc -l`
counts lines. Connect them with a pipe.
"""),
    ex("ls ecg/ | wc -l"),

    md("""
---
## Part 2. Looking inside a file without opening it

`cat` prints the whole file, which is fine for 10 lines and terrible for 100 000.
Use `head -n` and `tail -n` instead, and `wc -l` to ask how big the thing is first.
"""),
    code("""
%%bash
cd ../data
wc -l patients.csv
echo "--- first 3 rows ---"
head -3 patients.csv
echo "--- last row ---"
tail -1 patients.csv
"""),
    md("""
Note that `wc -l` counts **241** lines for **240** patients: the header is a line
too. Off-by-one errors in this course will almost always be a header.

**Exercise 2.1.** Print only the header line of `patients.csv`, and nothing else.
"""),
    ex("head -1 patients.csv"),

    md("""
**Exercise 2.2.** `../data/export.log` is the recorder's log. Print its **last 5**
lines to see how the export ended.
"""),
    ex("tail -5 export.log"),

    md("""
---
## Part 3. Filtering and counting: the shell as a query language

`grep PATTERN file` keeps the lines that contain `PATTERN`. Its useful flags:

- `-c` count the matches instead of printing them
- `-i` ignore case · `-v` **invert**: keep the lines that do *not* match
- `-n` show line numbers · `-r` search a whole folder recursively
"""),
    code("""
%%bash
cd ../data
grep -c 'ICU' patients.csv
echo "--- three example rows ---"
grep 'ICU' patients.csv | head -3
"""),
    md("""
**Exercise 3.1.** How many stays ended with `deceased`? And how many did **not**?
(Two commands; remember the header will be counted in the second one.)
"""),
    ex("grep -c 'deceased' patients.csv\ngrep -vc 'deceased' patients.csv"),

    md("""
`cut` keeps columns. You must tell it the separator (`-d,`) and which fields
(`-f4`). Fields are numbered from 1.

`sort` orders lines; `uniq -c` collapses *adjacent* identical lines and counts
them, which is why it is almost always used right after `sort`.
Together, `sort | uniq -c` is the shell's `value_counts()`.
"""),
    code("""
%%bash
cd ../data
cut -d, -f4 patients.csv | sort | uniq -c | sort -rn
"""),
    md("""
**Exercise 3.2.** Produce the same kind of table for the **outcome** column
(field 7), most frequent first. The header row will appear as a count of 1;
leave it, we will remove it in the next exercise.
"""),
    ex("cut -d, -f7 patients.csv | sort | uniq -c | sort -rn"),

    md("""
**Exercise 3.3.** Same table, but drop the header first.

`tail -n +2` means "start at line 2": it is the standard way to skip a CSV header
in a pipeline.
"""),
    ex("tail -n +2 patients.csv | cut -d, -f7 | sort | uniq -c | sort -rn"),

    md("""
**Exercise 3.4.** How many **ICU** stays ended as `deceased`?

Chain two `grep`s: the first narrows to ICU, the second filters what is left.
"""),
    ex("grep 'ICU' patients.csv | grep -c 'deceased'"),

    md("""
**Exercise 3.5.** A few percent of the rows are missing an age, which in a CSV looks
like two commas with nothing between them: `P0007,,F,ICU,...`.

Count those rows. The pattern you want is `,,`.
"""),
    ex("grep -c ',,' patients.csv"),

    md("""
---
## Part 4. Finding files, and filenames that fight back

`find` walks a tree looking for files that match a test:

```bash
find . -name '*.csv'        # by name, recursively, from here down
find . -type f -empty       # files that are zero bytes
find . -size +1k            # bigger than 1 kB
```

Quote the pattern (`'*.csv'`): otherwise the shell expands it *before* `find` sees
it, and you get a confusing error.
"""),
    code("""
%%bash
cd ../data
find . -name '*.csv' | head -5
echo "--- how many in total ---"
find . -name '*.csv' | wc -l
"""),
    md("""
**Exercise 4.1.** One ECG trace arrived empty from the recorder. Find it.

Use `find` with `-type f` and `-empty`.
"""),
    ex("find . -type f -empty"),

    md("""
**Exercise 4.2.** There are 240 patients but far fewer ECG traces. How many
patients have **no** trace?

Count the traces, count the patients (careful: the header is a line too), and
subtract. Two commands and some arithmetic in your head is a perfectly
good answer here.
"""),
    ex("echo \"traces: $(ls ecg/ | wc -l)\"\necho \"patients: $(( $(wc -l < patients.csv) - 1 ))\""),

    md("""
**Exercise 4.3.** `../data/exports/` contains a file whose name has **spaces** in it.

`cat ../data/exports/Patient Records 2024.csv` fails, because the shell splits that
into three arguments. Print its first two lines, quoting the path correctly.

(Try it without quotes first, and read the error: it names the file it looked for.)
"""),
    ex("head -2 'exports/Patient Records 2024.csv'"),

    md("""
**Exercise 4.4.** `grep -r` searches inside every file of a folder.

Which ward-round notes in `../data/notes/` mention `sepsis`? Print the filenames only
(`-l` gives you names instead of matching lines).
"""),
    ex("grep -rli 'sepsis' notes/"),

    md("""
---
## Part 5. Writing results down

- `>` sends stdout to a file, **overwriting** it
- `>>` **appends** to it
- errors (stderr) are not redirected by `>`, which is deliberate, so a failure is
  never silently written into your results

A result that only exists in a notebook output is not a result. Write it to a file.
"""),
    code("""
%%bash
cd ../data
mkdir -p ../results
tail -n +2 patients.csv | cut -d, -f4 | sort | uniq -c | sort -rn > ../results/wards.txt
cat ../results/wards.txt
"""),
    md("""
**Exercise 5.1.** Write the ICU rows of `patients.csv` (header included) into
`../results/icu.csv`, then check the file has the number of lines you expect.

Two redirections: `>` for the header, then `>>` to append the matching rows.
"""),
    ex("head -1 patients.csv > ../results/icu.csv\ngrep 'ICU' patients.csv >> ../results/icu.csv\nwc -l ../results/icu.csv"),

    md("""
---
## Part 6. A loop: the step from one file to all of them

Everything so far was one command on one target. A loop applies it to every file,
and that is the entire difference between an afternoon and a second.

```bash
for f in ecg/*.csv; do      # for every matching file...
  echo "$f"                 # ...do this, with $f standing for the filename
done
```

Always quote `"$f"`: filenames contain spaces, and an unquoted variable is split on
them.
"""),
    code("""
%%bash
cd ../data
for f in $(ls ecg/*.csv | head -3); do
  echo "$f has $(wc -l < "$f") lines"
done
"""),
    md("""
**Exercise 6.1.** Write a loop over **all** files in `ecg/` that prints
`filename,line_count` for each, and sends the whole thing to
`../results/ecg_rows.csv`.

Then print the first 5 lines of that file to check it.
"""),
    ex("""
for f in ecg/*.csv; do
  echo "$f,$(wc -l < "$f")"
done > ../results/ecg_rows.csv
head -5 ../results/ecg_rows.csv
"""),

    md("""
---
## Part 7. Putting it together

**Exercise 7.1 (the one that matters).** In a single pipeline, produce the count of
stays per ward **for ICU patients over 80 only**.

Suggested shape: skip the header, keep ICU rows, keep rows where the age field is
80 or more, then count. Getting a numeric comparison out of `grep` alone is awkward
`awk -F, '$2 >= 80'` does it directly, and is worth meeting now:

```bash
awk -F, '$2 >= 80'      # keep rows whose 2nd comma-separated field is >= 80
```
"""),
    ex("tail -n +2 patients.csv | grep 'ICU' | awk -F, '$2 >= 80' | wc -l"),

    md("""
**Exercise 7.2.** The log at `../data/export.log` records one line per trace written,
and an `ERROR` line whenever a trace could not be read.

How many errors? And for which patients? (The patient id is the last field of the
line, and `awk '{print $NF}'` prints the last field of each line.)
"""),
    ex("grep -c 'ERROR' export.log\ngrep 'ERROR' export.log | awk '{print $NF}'"),

    md("""
**Exercise 7.3, free form.** Write one command that answers a question *you* find
interesting about this cohort, and one sentence saying what it tells you.

Some ideas: the sex ratio per ward; the number of admissions per month (field 5 is
`2024-MM-DD`, and `cut -c1-7` keeps the first 7 characters); the longest stay.
"""),
    ex("""
# admissions per month
tail -n +2 patients.csv | cut -d, -f5 | cut -c1-7 | sort | uniq -c
"""),

    md("""
---
## Part 8. Where Python fits

Everything above was bash. Bash is good at *files*: finding them, filtering them,
moving them, and starting programs. It is deliberately bad at arithmetic and at
anything with a nested structure, which is exactly what Python is for.

They are not rivals. **bash decides which files Python runs on**, and the two
exchange work through files on disk.

`python3` is not special: it is a program the shell finds and starts, like `ls`.
"""),
    code("""
%%bash
which python3          # where the program lives
python3 --version      # which one it is
python3 -c 'print("hello from python, started by bash")'
"""),
    md("""
**Exercise 8.1.** Ask Python for something bash is bad at: print `2 ** 64`.

Use `python3 -c '...'` with single quotes, so the shell hands the whole expression
to Python untouched.
"""),
    ex("python3 -c 'print(2 ** 64)'", cd="."),

    md("""
### Writing a script from the shell

`cat > file << 'EOF' ... EOF` is a **heredoc**: it writes everything up to `EOF`
into a file. Handy here; in real life you would use an editor.

The script below is deliberately imperfect: we come back to it in 8.4.
"""),
    code('''
%%bash
cat > clean.py << 'EOF'
import os
import sys


def summarise(path):
    rows = open(path).read().splitlines()
    header = rows[0]
    n = len(rows) - 1
    print(f"{path},{n}")


for p in sys.argv[1:]:
    summarise(p)
EOF
python3 clean.py ../data/patients.csv
'''),
    md("""
**Exercise 8.2.** Now let bash supply the files. Run `clean.py` on the first three
ECG traces, using a loop.

The script accepts several filenames at once, so a loop is not strictly necessary.
Try `python3 clean.py ../data/ecg/*.csv` too, and notice that the shell expands the
`*` into 60 arguments before Python ever starts.
"""),
    ex('''
for f in $(ls ../data/ecg/*.csv | head -3); do
  python3 clean.py "$f"
done
''', cd="."),

    md("""
---
### Environments

An environment is a **folder with its own Python and its own packages**. Nothing
more. Activating one just puts that folder first on your `PATH`, which is why
`which python3` is the command that tells you where you really are.

One per project, inside the project, disposable. Never install into the system
Python: on a managed workstation you usually cannot, and the error you get reads
`externally-managed-environment`.
"""),
    code("""
%%bash
python3 -m venv .venv               # create it  (uv venv does the same, faster)
echo "before:  $(which python3)"
source .venv/bin/activate           # activate it, for this cell only
echo "after:   $(which python3)"
"""),
    md("""
The activation did **not** survive into the next cell, because each `%%bash` cell is
a new shell. In a terminal it lasts until you type `deactivate` or close the window.

**Exercise 8.3.** In a single cell: activate `.venv`, list what is installed in it
with `python3 -m pip list`, then write that list to `requirements.txt`.

Use `python3 -m pip freeze > requirements.txt` for the last part: `freeze` prints
exact pinned versions, which is the format another machine can reinstall from.
"""),
    ex("""
source .venv/bin/activate
python3 -m pip list
python3 -m pip freeze > requirements.txt
""", cd="."),

    md("""
### pip and uv

- **`pip`** is the standard installer. It ships with Python and does one job:
  install packages into the environment that is active right now.
- **`uv`** is a single fast binary that does that job *and* the ones around it:
  installing Python itself, creating environments, locking versions.

| Task | pip / venv | uv |
|---|---|---|
| create an environment | `python3 -m venv .venv` | `uv venv` |
| install a package | `python3 -m pip install pandas` | `uv pip install pandas` |
| record what you have | `python3 -m pip freeze > requirements.txt` | `uv pip freeze > requirements.txt` |
| install a Python | (pyenv, or your OS) | `uv python install 3.12` |
| run a tool once | (no equivalent) | `uvx ruff check .` |

Installing them:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh   # uv, macOS/Linux, no Python needed
# Windows: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

python3 -m ensurepip --upgrade                    # pip, if a Python somehow lacks it
```

Prefer `python3 -m pip` over a bare `pip`: it can only install into *that*
interpreter, which removes an entire class of confusion.
"""),
    code("""
%%bash
command -v uv && uv --version || echo "uv is not installed here, the pip column works too"
"""),

    md("""
### ruff

`ruff` is a **linter** (finds mistakes) and a **formatter** (fixes layout) in one
binary, fast enough to run on every save.

```bash
uv tool install ruff          # install it for good
uvx ruff check .              # or run it once, installing nothing
python3 -m pip install ruff   # the pip route, inside an activated .venv
```

**Exercise 8.4.** Run `ruff` on `clean.py` and read what it says.

Use `uvx ruff check clean.py`. It should find three things.

One catch: a program that finds problems **exits non-zero**, and a `%%bash` cell
turns a non-zero exit into a `CalledProcessError` traceback. That exit code is a
feature (it is how a build server knows to reject a commit), but here it hides the
output, so end the line with `|| true` to say "I expected that".
"""),
    ex("uvx ruff check clean.py || true", cd="."),

    md("""
Three catches, and none of them is about style:

- `os` is imported and never used, left over from an earlier version
- `header` is assigned and never used, and nine times out of ten that line was
  *meant* to do something
- the file is opened and never closed, which is fine once and a leak in a loop over
  4 000 files

**Exercise 8.5.** Ask `ruff` to fix what it can automatically, then look at the top
of the file to see what changed.
"""),
    ex("uvx ruff check --fix clean.py || true\necho '--- the file now starts with ---'\nhead -3 clean.py", cd="."),

    md("""
**Exercise 8.6.** `ruff format` rewrites layout to one house style. Run it on
`clean.py`.

Formatting looks cosmetic, and it is, but a diff full of whitespace changes hides
the one line that actually changed, which is a real problem when a colleague has to
review what you did to a cohort.
"""),
    ex("uvx ruff format clean.py", cd="."),

    md("""
---
## What you have just done

You described a cohort, found two data-quality problems (an empty file and some
failed exports), produced three result files, and then set up an isolated Python
environment and had a linter read your code back to you.

Every step is a line of text you could paste into a methods section, or re-run on a
bigger export tomorrow. That is the whole argument for the command line.

**Next session:** globs and quoting in depth, `sed` and `awk`, and turning a
notebook like this one into a script that runs unattended.
"""),
]


def build(cells, solved: bool) -> dict:
    out = []
    for c in cells:
        out.append(c[1] if solved else c[0]) if isinstance(c, tuple) else out.append(c)
    return {
        "cells": out,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python",
                           "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def main() -> None:
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "Programming01/Session01")
    out.mkdir(parents=True, exist_ok=True)
    for name, solved in (("notebook.ipynb", False),
                         ("notebook_solutions.ipynb", True)):
        (out / name).write_text(json.dumps(build(CELLS, solved), indent=1) + "\n")
        print(out / name)


if __name__ == "__main__":
    main()
