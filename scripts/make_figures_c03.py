#!/usr/bin/env python3
"""Render the illustration figures used by the Programming01 Session03 slides.

Same contract as the NYU Paris decks: every figure is synthetic, seeded and
self-contained, so `make figures` reproduces the same output anywhere without
touching `data/`. Figures land in `Programming01/Session03/img/`.

Usage: make_figures_c03.py [outdir]   (default: Programming01/Session03/img)
"""

from __future__ import annotations

import sys
from pathlib import Path

from matplotlib.patches import FancyBboxPatch

from slidefig import (
    AMBER,
    BLUE,
    FAINT,
    GREEN,
    GREY,
    INK,
    MONO,
    PURPLE,
    RED,
    SLIDE_ASPECT,
    WIDE,
    arrow,
    blank,
    box,
    plt,
    save,
    terminal,
)


# ============================================================ 1. why the shell
def fig_gui_vs_cli(out: Path) -> None:
    """The same job done twice: 40 clicks nobody can replay vs one line anyone can."""
    fig, axes = plt.subplots(1, 2, figsize=WIDE)

    ax = axes[0]
    blank(ax)
    ax.set_title("Point and click", color=RED, fontsize=14)
    ax.add_patch(
        FancyBboxPatch(
            (0.06, 0.30),
            0.88,
            0.52,
            boxstyle="round,pad=0.01,rounding_size=0.02",
            facecolor="white",
            edgecolor=GREY,
            linewidth=1.6,
        )
    )
    for i in range(4):
        for j in range(6):
            ax.add_patch(
                FancyBboxPatch(
                    (0.11 + j * 0.135, 0.36 + i * 0.115),
                    0.10,
                    0.075,
                    boxstyle="round,pad=0.004,rounding_size=0.01",
                    facecolor=FAINT,
                    edgecolor=GREY,
                    linewidth=0.8,
                )
            )
    ax.plot(
        [0.30, 0.55, 0.44, 0.72, 0.36, 0.66],
        [0.42, 0.55, 0.68, 0.48, 0.60, 0.72],
        "-",
        color=RED,
        lw=1.2,
        alpha=0.8,
        marker="o",
        ms=5,
    )
    ax.text(
        0.5,
        0.20,
        "open · scroll · select · rename · repeat  × 137",
        ha="center",
        fontsize=11,
        color=RED,
    )
    ax.text(
        0.5,
        0.09,
        "nobody can tell you what you did",
        ha="center",
        fontsize=11.5,
        color=RED,
        style="italic",
    )

    ax = axes[1]
    blank(ax)
    ax.set_title("Type a command", color=GREEN, fontsize=14)
    terminal(
        ax,
        (0.5, 0.56),
        0.88,
        0.52,
        [
            ("$ ls data/*.csv | wc -l", INK),
            ("137", GREY),
            ("$ grep -c 'ICU' data/*.csv > counts.txt", INK),
            ("$", INK),
        ],
    )
    ax.text(
        0.5,
        0.20,
        "one line · re-runnable · pasteable in a methods section",
        ha="center",
        fontsize=11,
        color=GREEN,
    )
    ax.text(
        0.5,
        0.09,
        "the command is the documentation",
        ha="center",
        fontsize=11.5,
        color=GREEN,
        style="italic",
    )

    fig.tight_layout()
    save(fig, out, "gui_vs_cli")


# ====================================================== 2. terminal vs shell
def fig_terminal_shell(out: Path) -> None:
    """Four words students use interchangeably, and what each one actually is."""
    fig, ax = plt.subplots(figsize=WIDE)
    blank(ax)

    ys = 0.62
    box(ax, (0.13, ys), 0.20, 0.30, "Terminal\n(window)", ec=BLUE)
    box(ax, (0.38, ys), 0.20, 0.30, "Shell\nbash / zsh", ec=PURPLE)
    box(ax, (0.63, ys), 0.20, 0.30, "Programs\nls, grep, python", ec=GREEN)
    box(ax, (0.88, ys), 0.20, 0.30, "Kernel\nfiles, processes", ec=AMBER)

    for a, b in ((0.23, 0.28), (0.48, 0.53), (0.73, 0.78)):
        arrow(ax, (a, ys), (b, ys), color=GREY)

    ax.text(
        0.13,
        0.30,
        "shows text,\ntakes keystrokes",
        ha="center",
        fontsize=10,
        color=BLUE,
    )
    ax.text(
        0.38,
        0.30,
        "reads your line,\nfinds the program,\nruns it",
        ha="center",
        fontsize=10,
        color=PURPLE,
    )
    ax.text(
        0.63,
        0.30,
        "one job each,\ntext in / text out",
        ha="center",
        fontsize=10,
        color=GREEN,
    )
    ax.text(
        0.88,
        0.30,
        "does the actual\nwork on disk",
        ha="center",
        fontsize=10,
        color=AMBER,
    )

    ax.text(
        0.5,
        0.08,
        "The shell is a programming language you happen to type one line at a time.",
        ha="center",
        fontsize=12.5,
        color=INK,
    )
    save(fig, out, "terminal_shell")


# ==================================================== 3. anatomy of a command
def fig_anatomy(out: Path) -> None:
    """command · options · arguments: the grammar every command obeys."""
    fig, ax = plt.subplots(figsize=WIDE)
    blank(ax)

    parts = [
        ("ls", 0.16, BLUE, "command\nwhat to run"),
        ("-l -h", 0.38, PURPLE, "options (flags)\nhow to run it"),
        ("data/ecg/", 0.66, GREEN, "arguments\nwhat to run it on"),
    ]
    ax.text(0.045, 0.72, "$", fontsize=26, family=MONO, color=GREY, va="center")
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    for text, x, colour, label in parts:
        h = ax.text(
            x,
            0.72,
            text,
            fontsize=26,
            family=MONO,
            color=colour,
            va="center",
            ha="left",
        )
        # underline exactly as wide as the rendered text, in axes coordinates
        bb = h.get_window_extent(r).transformed(ax.transAxes.inverted())
        ax.plot([bb.x0, bb.x1], [0.60, 0.60], color=colour, lw=2.5)
        mid = (bb.x0 + bb.x1) / 2
        ax.plot([mid, mid], [0.60, 0.52], color=colour, lw=1.5)
        ax.text(mid, 0.44, label, ha="center", va="center", fontsize=11.5, color=colour)

    ax.text(
        0.045,
        0.25,
        "separated by spaces  ·  order: command first, then flags, then targets",
        fontsize=12,
        color=INK,
        ha="left",
    )
    ax.text(
        0.045,
        0.14,
        "-h  short flag        --human-readable  long flag        -lh  flags can stack",
        fontsize=11.5,
        family=MONO,
        color=GREY,
        ha="left",
    )
    ax.text(
        0.045,
        0.04,
        "a space is a separator: a file called  my notes.csv  needs "
        "quotes or a backslash",
        fontsize=11,
        color=RED,
        ha="left",
    )
    save(fig, out, "anatomy")


# ======================================================== 4. the filesystem
def fig_filesystem(out: Path) -> None:
    """A tree, one working directory, and the two ways to name the same file."""
    fig, axes = plt.subplots(
        1, 2, figsize=WIDE, gridspec_kw={"width_ratios": [1.15, 1]}
    )

    ax = axes[0]
    blank(ax)
    ax.set_title("One tree, one root", fontsize=13)
    nodes = [
        ("/", 0.10, 0.88, INK),
        ("home/", 0.22, 0.74, INK),
        ("paul/", 0.34, 0.60, INK),
        ("project/", 0.46, 0.46, PURPLE),
        ("data/", 0.58, 0.32, GREEN),
        ("ecg_001.csv", 0.70, 0.18, GREEN),
        ("notes.md", 0.58, 0.60, GREY),
    ]
    for name, x, y, colour in nodes:
        ax.text(x, y, name, fontsize=13, family=MONO, color=colour, va="center")
    for (x0, y0), (x1, y1) in (
        ((0.13, 0.84), (0.21, 0.75)),
        ((0.25, 0.70), (0.33, 0.61)),
        ((0.37, 0.56), (0.45, 0.47)),
        ((0.49, 0.42), (0.57, 0.33)),
        ((0.61, 0.28), (0.69, 0.19)),
        ((0.49, 0.51), (0.57, 0.60)),
    ):
        ax.plot([x0, x1], [y0, y1], color=GREY, lw=1.2)
    ax.text(
        0.64,
        0.46,
        "← you are here (pwd)",
        fontsize=11,
        color=PURPLE,
        va="center",
        ha="left",
    )

    ax = axes[1]
    blank(ax)
    ax.set_title("Two ways to name the same file", fontsize=13)
    box(
        ax,
        (0.5, 0.78),
        0.94,
        0.22,
        "/home/paul/project/data/ecg_001.csv",
        ec=BLUE,
        fs=12,
        mono=True,
    )
    ax.text(
        0.5,
        0.61,
        "absolute: from the root, always works",
        ha="center",
        fontsize=11.5,
        color=BLUE,
    )
    box(ax, (0.5, 0.42), 0.94, 0.22, "data/ecg_001.csv", ec=GREEN, fs=12, mono=True)
    ax.text(
        0.5,
        0.25,
        "relative: from where you are, shorter, portable",
        ha="center",
        fontsize=11.5,
        color=GREEN,
    )
    ax.text(
        0.5,
        0.09,
        ".  here      ..  one level up      ~  your home",
        ha="center",
        fontsize=12,
        family=MONO,
        color=INK,
    )

    fig.tight_layout()
    save(fig, out, "filesystem")


# ============================================================ 5. streams & pipes
def fig_pipeline(out: Path) -> None:
    """stdin / stdout / stderr, and what the pipe actually connects."""
    fig, axes = plt.subplots(
        2,
        1,
        figsize=(12.6, 12.6 / SLIDE_ASPECT),
        gridspec_kw={"height_ratios": [1, 1.25]},
    )

    ax = axes[0]
    blank(ax)
    box(ax, (0.5, 0.55), 0.26, 0.46, "a command", ec=INK, fs=12)
    arrow(ax, (0.16, 0.55), (0.36, 0.55), color=BLUE)
    ax.text(0.16, 0.72, "stdin", ha="center", fontsize=11.5, family=MONO, color=BLUE)
    arrow(ax, (0.64, 0.66), (0.86, 0.66), color=GREEN)
    ax.text(
        0.90,
        0.66,
        "stdout",
        ha="left",
        va="center",
        fontsize=11.5,
        family=MONO,
        color=GREEN,
    )
    arrow(ax, (0.64, 0.42), (0.86, 0.42), color=RED)
    ax.text(
        0.90,
        0.42,
        "stderr",
        ha="left",
        va="center",
        fontsize=11.5,
        family=MONO,
        color=RED,
    )
    ax.text(
        0.02,
        0.10,
        "results go to stdout, errors go to stderr",
        fontsize=11,
        color=GREY,
        ha="left",
    )

    ax = axes[1]
    blank(ax)
    ax.text(
        0.02,
        0.90,
        "$ cat patients.csv | grep ICU | cut -d, -f3 | sort | uniq -c > icu.txt",
        fontsize=13.5,
        family=MONO,
        color=INK,
        ha="left",
        va="center",
    )
    stages = [
        ("cat", 0.11, "read the file"),
        ("grep ICU", 0.29, "keep ICU rows"),
        ("cut -f3", 0.47, "keep column 3"),
        ("sort", 0.63, "group equals"),
        ("uniq -c", 0.79, "count them"),
    ]
    for name, x, label in stages:
        box(ax, (x, 0.55), 0.125, 0.24, name, ec=PURPLE, fs=11.5, mono=True)
        ax.text(x, 0.33, label, ha="center", fontsize=10, color=GREY)
    for x0, x1 in zip([s[1] for s in stages], [s[1] for s in stages][1:]):
        arrow(ax, (x0 + 0.068, 0.55), (x1 - 0.068, 0.55), color=PURPLE)
    arrow(ax, (0.858, 0.55), (0.93, 0.55), color=GREEN)
    ax.text(0.945, 0.55, "file", ha="left", va="center", fontsize=11, color=GREEN)
    ax.text(
        0.5,
        0.08,
        "|  sends stdout into the next stdin        "
        ">  sends it to a file (overwrites)        >>  appends",
        ha="center",
        fontsize=11.5,
        family=MONO,
        color=INK,
    )

    fig.tight_layout()
    save(fig, out, "pipeline")


# ====================================================== 6. why it matters here
def fig_reproducible(out: Path) -> None:
    """The health-data argument: a script is a protocol a reviewer can re-run."""
    fig, ax = plt.subplots(figsize=WIDE)
    blank(ax)

    ax.text(0.25, 0.93, "Clicking", ha="center", fontsize=14, color=RED)
    ax.text(0.75, 0.93, "Scripting", ha="center", fontsize=14, color=GREEN)
    ax.plot([0.5, 0.5], [0.05, 0.88], color=FAINT, lw=2)

    rows = [
        ("Six months later", "what did I click?", "read the script"),
        ("A reviewer asks", '"trust me"', "here is the command"),
        ("1 file → 4 000 files", "hire an intern", "same command, one loop"),
        ("A colleague repeats it", "a screen recording", "git clone && ./run.sh"),
        ("Data must stay on-site", "no GUI on the server", "ssh, and you are in"),
    ]
    for i, (topic, bad, good) in enumerate(rows):
        y = 0.76 - i * 0.145
        ax.text(0.02, y, topic, fontsize=11.5, color=INK, va="center", ha="left")
        ax.text(0.47, y, bad, fontsize=11.5, color=RED, va="center", ha="right")
        ax.text(0.53, y, good, fontsize=11.5, color=GREEN, va="center", ha="left")
        if i:
            ax.plot([0.0, 1.0], [y + 0.072, y + 0.072], color=FAINT, lw=0.8)

    save(fig, out, "reproducible")


# ================================================== 7. bash vs python
def fig_python_vs_bash(out: Path) -> None:
    """Two languages, one boundary: gluing files vs computing on data."""
    fig, ax = plt.subplots(figsize=WIDE)
    blank(ax)

    ax.text(0.25, 0.93, "bash", ha="center", fontsize=17, family=MONO, color=PURPLE)
    ax.text(0.75, 0.93, "python", ha="center", fontsize=17, family=MONO, color=BLUE)
    ax.plot([0.5, 0.5], [0.11, 0.86], color=FAINT, lw=2)

    rows = [
        (
            "What it manipulates",
            "files, processes, other programs",
            "values, tables, models",
        ),
        ("Its natural unit", "a line of text", "an object"),
        ("Great at", "find / filter / move / launch", "compute / model / plot"),
        ("Painful at", "arithmetic, anything nested", "renaming 4 000 files"),
        ("You write", "a few lines, interactively", "a program you keep"),
    ]
    for i, (topic, b, py) in enumerate(rows):
        y = 0.76 - i * 0.145
        ax.text(0.02, y, topic, fontsize=11.5, color=INK, va="center", ha="left")
        ax.text(0.47, y, b, fontsize=11.5, color=PURPLE, va="center", ha="right")
        ax.text(0.53, y, py, fontsize=11.5, color=BLUE, va="center", ha="left")
        if i:
            ax.plot([0.0, 1.0], [y + 0.072, y + 0.072], color=FAINT, lw=0.8)

    ax.text(
        0.5,
        0.03,
        "Not rivals: bash decides which files Python runs on.",
        ha="center",
        fontsize=12.5,
        color=INK,
    )
    save(fig, out, "python_vs_bash")


# ================================================ 8. how the two meet
def fig_interop(out: Path) -> None:
    """Every Python program is started by a shell, and can call back into one."""
    fig, ax = plt.subplots(figsize=WIDE)
    blank(ax)

    box(ax, (0.15, 0.68), 0.24, 0.28, "the shell\nbash", ec=PURPLE, fs=12)
    box(
        ax,
        (0.58, 0.68),
        0.30,
        0.28,
        "python\n(an interpreter,\njust another program)",
        ec=BLUE,
        fs=11,
    )
    arrow(ax, (0.28, 0.74), (0.42, 0.74), color=PURPLE)
    ax.text(0.35, 0.90, "starts it", ha="center", fontsize=10.5, color=PURPLE)
    arrow(ax, (0.42, 0.62), (0.28, 0.62), color=BLUE)
    ax.text(0.35, 0.48, "prints, exits 0 or 1", ha="center", fontsize=10.5, color=BLUE)

    box(ax, (0.88, 0.68), 0.16, 0.28, "files\non disk", ec=GREY, fs=11)
    arrow(ax, (0.74, 0.68), (0.79, 0.68), color=GREY)

    lines = [
        ("$ python3 clean.py data/patients.csv", "run a script on a file"),
        ("$ python3 -c 'print(2 ** 10)'", "one throwaway expression"),
        ('$ for f in *.csv; do python3 clean.py "$f"; done', "bash supplies the loop"),
        ('subprocess.run(["ls", "-l"])', "...and Python can call back out"),
    ]
    for i, (cmd, why) in enumerate(lines):
        y = 0.33 - i * 0.090
        ax.text(0.02, y, cmd, fontsize=11.5, family=MONO, color=INK, va="center")
        ax.text(0.98, y, why, fontsize=10.5, color=GREY, va="center", ha="right")

    save(fig, out, "interop")


# ================================================ 9. virtual environments
def fig_environments(out: Path) -> None:
    """One machine, several projects, incompatible pins."""
    fig, axes = plt.subplots(1, 2, figsize=WIDE)

    ax = axes[0]
    blank(ax)
    ax.set_title("One shared Python", color=RED, fontsize=13)
    box(ax, (0.5, 0.30), 0.7, 0.24, "system python3\npandas 2.2", ec=RED, fs=11)
    for x, name, need in (
        (0.22, "cohort study", "needs pandas 1.5"),
        (0.5, "imaging pipeline", "needs pandas 2.2"),
        (0.78, "old thesis code", "needs pandas 0.25"),
    ):
        box(ax, (x, 0.80), 0.24, 0.22, name, ec=GREY, fs=10)
        ax.text(x, 0.62, need, ha="center", fontsize=9.5, color=INK)
        arrow(ax, (x, 0.55), (x if abs(x - 0.5) < 0.01 else 0.5, 0.43), color=RED)
    ax.text(
        0.5,
        0.10,
        "one install wins; the other two break",
        ha="center",
        fontsize=11.5,
        color=RED,
        style="italic",
    )

    ax = axes[1]
    blank(ax)
    ax.set_title("One environment per project", color=GREEN, fontsize=13)
    for x, name, ver in (
        (0.22, "cohort study", "pandas 1.5"),
        (0.5, "imaging pipeline", "pandas 2.2"),
        (0.78, "old thesis code", "pandas 0.25"),
    ):
        box(ax, (x, 0.80), 0.24, 0.22, name, ec=GREY, fs=10)
        arrow(ax, (x, 0.68), (x, 0.50), color=GREEN)
        box(ax, (x, 0.36), 0.24, 0.26, ".venv/\n" + ver, ec=GREEN, fs=10)
    ax.text(
        0.5,
        0.10,
        "a folder in the project, deletable, re-creatable",
        ha="center",
        fontsize=11.5,
        color=GREEN,
        style="italic",
    )

    fig.tight_layout()
    save(fig, out, "environments")


# ================================================ 10. the packaging toolchain
def fig_toolchain(out: Path) -> None:
    """Four tools and a lock file, or one tool: what uv replaces."""
    fig, axes = plt.subplots(1, 2, figsize=WIDE)

    ax = axes[0]
    blank(ax)
    ax.set_title("The classic stack", fontsize=13)
    items = [
        ("pyenv", "install Python itself"),
        ("venv", "make an environment"),
        ("pip", "install packages"),
        ("pip-tools", "pin them to a lock file"),
    ]
    for i, (name, what) in enumerate(items):
        y = 0.80 - i * 0.20
        box(ax, (0.22, y), 0.30, 0.15, name, ec=GREY, fs=11.5, mono=True)
        ax.text(0.42, y, what, fontsize=11, color=GREY, va="center", ha="left")
    ax.text(
        0.5,
        0.05,
        "four tools, four failure modes",
        ha="center",
        fontsize=11.5,
        color=AMBER,
    )

    ax = axes[1]
    blank(ax)
    ax.set_title("One tool that does all four", fontsize=13, color=GREEN)
    box(ax, (0.5, 0.87), 0.44, 0.16, "uv", ec=GREEN, fs=22, mono=True)
    cmds = [
        ("uv python install 3.12", "the interpreter"),
        ("uv venv", "the environment"),
        ("uv pip install pandas", "the packages"),
        ("uv lock  /  uv sync", "the lock file"),
    ]
    for i, (cmd, what) in enumerate(cmds):
        y = 0.62 - i * 0.135
        ax.text(0.02, y, cmd, fontsize=11.5, family=MONO, color=INK, va="center")
        ax.text(0.98, y, what, fontsize=10.5, color=GREEN, va="center", ha="right")
    ax.text(
        0.5,
        0.03,
        "one binary, 10 to 100x faster, installs without a Python",
        ha="center",
        fontsize=11.5,
        color=GREEN,
    )

    fig.tight_layout()
    save(fig, out, "toolchain")


# ================================================ 11. why version control
def fig_git_why(out: Path) -> None:
    """A folder of final_v2_REALLY copies vs one file and a readable history."""
    fig, axes = plt.subplots(1, 2, figsize=WIDE)

    ax = axes[0]
    blank(ax)
    ax.set_title("Copies", color=RED, fontsize=14)
    files = [
        "analysis.py",
        "analysis_v2.py",
        "analysis_v2_paul.py",
        "analysis_final.py",
        "analysis_final_OK.py",
        "analysis_final_OK_2024-03.py",
        "analysis_final_REALLY.py",
    ]
    for i, name in enumerate(files):
        y = 0.86 - i * 0.095
        ax.text(0.08, y, "▤", fontsize=13, color=GREY, va="center")
        ax.text(0.15, y, name, fontsize=11.5, family=MONO, color=INK, va="center")
    ax.text(
        0.5,
        0.12,
        "which one produced Table 2?",
        ha="center",
        fontsize=11.5,
        color=RED,
        style="italic",
    )

    ax = axes[1]
    blank(ax)
    ax.set_title("One file, a history", color=GREEN, fontsize=14)
    ax.text(0.08, 0.86, "▤", fontsize=13, color=GREY, va="center")
    ax.text(
        0.15, 0.86, "analysis.py", fontsize=11.5, family=MONO, color=INK, va="center"
    )
    terminal(
        ax,
        (0.5, 0.52),
        0.92,
        0.42,
        [
            ("$ git log --oneline", INK),
            ("e41c9d2 Exclude patients under 18", AMBER),
            ("7a0b3f1 Table 2: add BMI column", AMBER),
            ("c93e5a8 Fix unit: weight in kg", AMBER),
            ("1f2d6b0 First cleaning script", AMBER),
        ],
        title="Terminal",
    )
    ax.text(
        0.5,
        0.12,
        "who changed what, when, and why",
        ha="center",
        fontsize=11.5,
        color=GREEN,
        style="italic",
    )

    fig.tight_layout()
    save(fig, out, "git_why")


# ================================================ 12. the three areas
def fig_git_areas(out: Path) -> None:
    """Working folder, staging area, repository: what add and commit move."""
    fig, ax = plt.subplots(figsize=WIDE)
    blank(ax)

    cols = [
        (0.16, "Working folder", "the files you edit", BLUE),
        (0.50, "Staging area", "what goes in the\nnext snapshot", AMBER),
        (0.84, "Repository (.git/)", "every snapshot,\nforever", GREEN),
    ]
    for x, name, what, colour in cols:
        box(ax, (x, 0.62), 0.26, 0.34, "", ec=colour, lw=2.2)
        ax.text(x, 0.74, name, ha="center", fontsize=13, color=colour)
        ax.text(x, 0.58, what, ha="center", va="center", fontsize=11, color=INK)

    arrow(ax, (0.30, 0.66), (0.36, 0.66), color=AMBER, lw=2.2)
    ax.text(0.33, 0.90, "git add", ha="center", fontsize=13, family=MONO, color=AMBER)
    ax.plot([0.33, 0.33], [0.86, 0.70], color=AMBER, lw=1, ls=":")
    arrow(ax, (0.64, 0.66), (0.70, 0.66), color=GREEN, lw=2.2)
    ax.text(
        0.67, 0.90, "git commit", ha="center", fontsize=13, family=MONO, color=GREEN
    )
    ax.plot([0.67, 0.67], [0.86, 0.70], color=GREEN, lw=1, ls=":")

    ax.text(
        0.16,
        0.34,
        "git status\ngit diff",
        ha="center",
        fontsize=11.5,
        family=MONO,
        color=GREY,
    )
    ax.text(
        0.50,
        0.34,
        "git diff --staged",
        ha="center",
        fontsize=11.5,
        family=MONO,
        color=GREY,
    )
    ax.text(
        0.84,
        0.34,
        "git log\ngit show",
        ha="center",
        fontsize=11.5,
        family=MONO,
        color=GREY,
    )

    ax.text(
        0.5,
        0.10,
        "A commit is a snapshot of the whole project, with an author, "
        "a date and a message.",
        ha="center",
        fontsize=12.5,
        color=INK,
    )
    save(fig, out, "git_areas")


# ================================================ 13. history and branches
def fig_git_history(out: Path) -> None:
    """A chain of commits, HEAD, and one branch merged back."""
    fig, ax = plt.subplots(figsize=WIDE)
    blank(ax)

    main = [
        (0.08, "1f2d6b0"),
        (0.24, "c93e5a8"),
        (0.40, "7a0b3f1"),
        (0.72, "b52e0aa"),
        (0.90, "e41c9d2"),
    ]
    side = [(0.50, "4d8c1e7"), (0.62, "90aa3c2")]
    ym, ys = 0.62, 0.30
    xs = [x for x, _ in main]
    ax.plot(xs, [ym] * len(xs), color=BLUE, lw=2.5, zorder=1)
    ax.plot([0.40, 0.50, 0.62, 0.72], [ym, ys, ys, ym], color=PURPLE, lw=2.5, zorder=1)
    for x, h in main:
        ax.plot(x, ym, "o", ms=20, color="white", mec=BLUE, mew=2.5, zorder=2)
        ax.text(x, ym + 0.10, h, ha="center", fontsize=10.5, family=MONO, color=INK)
    for x, h in side:
        ax.plot(x, ys, "o", ms=20, color="white", mec=PURPLE, mew=2.5, zorder=2)
        ax.text(x, ys - 0.11, h, ha="center", fontsize=10.5, family=MONO, color=INK)

    ax.text(
        0.02,
        ym,
        "main",
        ha="left",
        va="center",
        fontsize=12,
        family=MONO,
        color=BLUE,
        fontweight="bold",
    )
    ax.text(
        0.40,
        ys,
        "new-plot",
        ha="right",
        va="center",
        fontsize=12,
        family=MONO,
        color=PURPLE,
        fontweight="bold",
    )
    box(ax, (0.90, 0.92), 0.10, 0.09, "HEAD", ec=RED, fs=11, mono=True, tc=RED)
    arrow(ax, (0.90, 0.87), (0.90, 0.77), color=RED)
    ax.text(0.72, 0.76, "merge", ha="center", fontsize=10.5, color=PURPLE)

    ax.text(
        0.5,
        0.06,
        "each commit points to its parent  ·  a branch is a movable "
        "label  ·  HEAD is where you are",
        ha="center",
        fontsize=12,
        color=INK,
    )
    save(fig, out, "git_history")


# ================================================ 14. local and remote
def fig_git_remote(out: Path) -> None:
    """Your laptop, GitHub, a colleague: clone, push, pull."""
    fig, ax = plt.subplots(figsize=WIDE)
    blank(ax)

    box(ax, (0.50, 0.76), 0.30, 0.26, "GitHub\n(remote: origin)", ec=INK, fs=13)
    box(ax, (0.15, 0.30), 0.24, 0.24, "your laptop\n.git/", ec=BLUE, fs=12)
    box(ax, (0.85, 0.30), 0.24, 0.24, "a colleague\n.git/", ec=PURPLE, fs=12)

    arrow(ax, (0.22, 0.43), (0.38, 0.64), color=GREEN, lw=2.2)
    ax.text(0.24, 0.57, "git push", ha="right", fontsize=12, family=MONO, color=GREEN)
    arrow(ax, (0.42, 0.62), (0.28, 0.42), color=BLUE, lw=2.2)
    ax.text(0.39, 0.48, "git pull", ha="left", fontsize=12, family=MONO, color=BLUE)

    arrow(ax, (0.62, 0.62), (0.78, 0.43), color=PURPLE, lw=2.2, ls="--")
    ax.text(
        0.76,
        0.57,
        "git clone\n(once)",
        ha="left",
        fontsize=12,
        family=MONO,
        color=PURPLE,
    )

    ax.text(
        0.5,
        0.36,
        "every copy holds\nthe full history",
        ha="center",
        fontsize=11,
        color=GREY,
        style="italic",
    )
    ax.text(
        0.5,
        0.07,
        "commit is local and offline  ·  push and pull synchronise  "
        "·  GitHub adds issues, reviews, a web page",
        ha="center",
        fontsize=11.5,
        color=INK,
    )
    save(fig, out, "git_remote")


FIGURES = (
    fig_gui_vs_cli,
    fig_terminal_shell,
    fig_anatomy,
    fig_filesystem,
    fig_pipeline,
    fig_reproducible,
    fig_python_vs_bash,
    fig_interop,
    fig_environments,
    fig_toolchain,
    fig_git_why,
    fig_git_areas,
    fig_git_history,
    fig_git_remote,
)


def main() -> None:
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "Programming01/Session03/img")
    out.mkdir(parents=True, exist_ok=True)
    for fn in FIGURES:
        fn(out)
        print(f"{out / (fn.__name__.removeprefix('fig_') + '.png')}")


if __name__ == "__main__":
    main()
