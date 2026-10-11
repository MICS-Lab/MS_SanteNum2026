#!/usr/bin/env python3
"""Render the illustration figures used by the Programming01 Session00 slides.

Session00 is the primer: why Python, what a library is, why versions collide, and
what `uv` does about it. Every figure is synthetic and self contained, so `make figures`
reproduces the same output anywhere.

Usage: make_figures_c00.py [outdir]   (default: Programming01/Session00/img)
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
    WIDE,
    arrow,
    blank,
    box,
    plt,
    save,
)


# ================================================= 0. low level vs high level
def fig_levels(out: Path) -> None:
    """A language sits somewhere between the processor and the problem."""
    fig, axes = plt.subplots(1, 2, figsize=WIDE, gridspec_kw={"width_ratios": [1, 1]})

    ax = axes[0]
    blank(ax)
    ax.text(0.34, 0.95, "high level (closer to human understanding)", ha="center",
            fontsize=11, color=GREEN)
    rungs = [
        ("Python, R, MATLAB", 0.76, GREEN, "one line can mean a lot of work"),
        ("C, C++, Rust", 0.56, BLUE, "you manage the memory yourself"),
        ("assembly", 0.36, AMBER, "one processor instruction at a time"),
        ("machine code", 0.16, GREY, "what the processor actually runs"),
    ]
    for name, y, colour, what in rungs:
        box(ax, (0.34, y), 0.56, 0.14, name, ec=colour, fs=12)
        ax.text(0.65, y, what, fontsize=10, color=GREY, va="center", ha="left")
    ax.text(0.34, 0.03, "low level (closer to the machine)", ha="center",
            fontsize=11, color=GREY)

    ax = axes[1]
    blank(ax)
    ax.set_title("Addition on different levels", fontsize=13)
    snippets = [
        ("Python", "c = a + b", GREEN),
        ("C", "int c = a + b;", BLUE),
        ("assembly", "mov eax,[a]  add eax,[b]  mov [c],eax", AMBER),
        ("machine code", "8b 45 fc 03 45 f8 89 45 f4", GREY),
    ]
    for i, (label, line, colour) in enumerate(snippets):
        y = 0.80 - i * 0.22
        ax.text(0.0, y, label, fontsize=10.5, color=colour, va="center", ha="left")
        ax.text(0.24, y, line, fontsize=10.5, family=MONO, color=INK,
                va="center", ha="left")
        if i:
            arrow(ax, (0.12, y + 0.16), (0.12, y + 0.05), color=FAINT, lw=2.2)
    ax.text(0.0, 0.03, "Processor can only run machine code",
            fontsize=10.5, color=INK, ha="left")

    fig.tight_layout()
    save(fig, out, "levels")


# ==================================================== 0b. why Python, here
def fig_why_python(out: Path) -> None:
    """Popular, high level, and fast where the time is actually spent."""
    fig, axes = plt.subplots(1, 3, figsize=WIDE)

    ax = axes[0]
    blank(ax)
    ax.set_title("Popular", fontsize=13, color=BLUE)
    ax.add_patch(FancyBboxPatch((0.02, 0.76), 0.96, 0.16,
                                boxstyle="round,pad=0.01,rounding_size=0.03",
                                facecolor="#fbfbfb", edgecolor=GREY, linewidth=1.4))
    ax.text(0.07, 0.84, "KeyError: 'age'", fontsize=11, family=MONO, color=RED,
            va="center", ha="left")
    for i, hit in enumerate(["Most questions are already answered",
                            "Documentation is up to date"]):
        y = 0.62 - i * 0.13
        ax.text(0.06, y, "\u2713", fontsize=12, color=GREEN, va="center")
        ax.text(0.16, y, hit, fontsize=10.5, color=GREY, va="center", ha="left")

    ax = axes[1]
    blank(ax)
    ax.set_title("High level", fontsize=13, color=PURPLE)
    code = ["for patient in ward:", "    if patient.age > 75:",
            "        elderly.append(patient)"]
    ax.add_patch(FancyBboxPatch((0.02, 0.60), 0.96, 0.32,
                                boxstyle="round,pad=0.01,rounding_size=0.03",
                                facecolor="#fbfbfb", edgecolor=GREY, linewidth=1.4))
    for i, line in enumerate(code):
        ax.text(0.06, 0.84 - i * 0.10, line, fontsize=10.5, family=MONO, color=INK,
                va="center", ha="left")
    ax.text(0.5, 0.44, "No types to declare,\nNo memory to free",
            ha="center", fontsize=10.5, color=GREY)
    ax.text(0.5, 0.08, "quick to learn",
            ha="center", fontsize=10.5, color=INK)

    ax = axes[2]
    blank(ax)
    ax.set_title("Fast", fontsize=13, color=GREEN)
    stack = [("your code (Python)", 0.86, PURPLE, 0.12),
             ("numpy, pandas, torch", 0.69, BLUE, 0.12),
             ("C, Fortran, Rust, CUDA", 0.52, GREEN, 0.12)]
    for name, y, colour, h in stack:
        box(ax, (0.5, y), 0.92, h, name, ec=colour, fs=10.5)
    for y in (0.775, 0.605):
        arrow(ax, (0.5, y + 0.025), (0.5, y - 0.025), color=GREY, lw=1.4)
    ax.text(0.5, 0.33, "Few lines convert to compiled code\nand billion operations",
            ha="center", fontsize=10.5, color=GREY)

    fig.tight_layout()
    save(fig, out, "why_python")


# ============================================= 0c. the jobs everybody has
def _cells(ax, x0, y0, cols, rows, w=0.085, h=0.055, ec=GREY, header=BLUE):
    for r in range(rows):
        for c in range(cols):
            ax.add_patch(FancyBboxPatch((x0 + c * w, y0 - r * h), w * 0.92, h * 0.86,
                                        boxstyle="square,pad=0",
                                        facecolor=("#eef3fa" if r == 0 else "white"),
                                        edgecolor=(header if r == 0 else ec),
                                        linewidth=1.0))


def fig_common_tasks(out: Path) -> None:
    """Three jobs every single project needs, and nobody should write twice."""
    fig, axes = plt.subplots(1, 3, figsize=WIDE)

    ax = axes[0]
    blank(ax)
    ax.set_title("Read a table", fontsize=13)
    _cells(ax, 0.28, 0.86, 4, 4, w=0.11, h=0.075)
    ax.text(0.5, 0.36, 'pd.read_csv("patients.csv")', ha="center", fontsize=11,
            family=MONO, color=BLUE)
#     ax.text(0.5, 0.17, "separators, quoting, encodings,\nmissing values, dates",
#             ha="center", fontsize=10, color=GREY)

    ax = axes[1]
    blank(ax)
    ax.set_title("Draw a figure", fontsize=13)
    xs = [0.16 + i * 0.0733 for i in range(10)]
    ys = [0.64, 0.74, 0.70, 0.83, 0.78, 0.87, 0.72, 0.80, 0.68, 0.76]
    ax.plot(xs, ys, color=RED, lw=1.8, marker="o", ms=3)
    ax.plot([0.14, 0.14, 0.90], [0.90, 0.58, 0.58], color=INK, lw=1.2)
    ax.text(0.5, 0.36, "plt.plot(t, ecg)", ha="center", fontsize=11,
            family=MONO, color=BLUE)
#     ax.text(0.5, 0.17, "axes, ticks, labels, colours,\nand a file you can print",
#             ha="center", fontsize=10, color=GREY)

    ax = axes[2]
    blank(ax)
    ax.set_title("Multiply matrices", fontsize=13)
    _cells(ax, 0.17, 0.86, 3, 3, w=0.095, h=0.075, header=GREY)
    ax.text(0.50, 0.75, "x", fontsize=14, color=INK, ha="center", va="center")
    _cells(ax, 0.545, 0.86, 3, 3, w=0.095, h=0.075, header=GREY)
    ax.text(0.5, 0.36, "A @ B", ha="center", fontsize=11, family=MONO, color=BLUE)
#     ax.text(0.5, 0.17, "blocking, threads, vector units,\nfifty years of Fortran",
#             ha="center", fontsize=10, color=GREY)

    fig.text(0.5, 0.025, "Most project need these.", ha="center", fontsize=11.5, color=INK)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    save(fig, out, "common_tasks")

# ======================================================= 1. what you do not write
def fig_library_value(out: Path) -> None:
    """The same job: four hundred lines you maintain, or one line you import."""
    fig, axes = plt.subplots(1, 2, figsize=WIDE)

    ax = axes[0]
    blank(ax)
    ax.set_title("Writing everything yourself", color=RED, fontsize=14)
    ax.add_patch(FancyBboxPatch((0.06, 0.26), 0.88, 0.58,
                                boxstyle="round,pad=0.01,rounding_size=0.02",
                                facecolor="#fbfbfb", edgecolor=GREY, linewidth=1.4))
    rng_widths = [0.62, 0.74, 0.45, 0.80, 0.55, 0.70, 0.38, 0.66, 0.50, 0.72]
    for i, w in enumerate(rng_widths):
        y = 0.79 - i * 0.052
        ax.plot([0.11, 0.11 + w * 0.78], [y, y], color=FAINT, lw=4,
                solid_capstyle="round")
    ax.text(0.5, 0.17, "Needs to handle quoting, encodings, missing values, dates, ...",
            ha="center", fontsize=10.5, color=GREY)
    ax.text(0.5, 0.06, "many lines, possible bugs", ha="center",
            fontsize=12, color=RED, style="italic")

    ax = axes[1]
    blank(ax)
    ax.set_title("Importing a library", color=GREEN, fontsize=14)
    ax.add_patch(FancyBboxPatch((0.06, 0.26), 0.88, 0.58,
                                boxstyle="round,pad=0.01,rounding_size=0.02",
                                facecolor="#fbfbfb", edgecolor=GREY, linewidth=1.4))
    for i, line in enumerate(["import pandas as pd", "",
                              'df = pd.read_csv("patients.csv")']):
        ax.text(0.11, 0.72 - i * 0.12, line, fontsize=13, family=MONO,
                color=(INK if line else GREY))
    ax.text(0.5, 0.17, "Edge cases are already found and fixed",
            ha="center", fontsize=10.5, color=GREY)
    ax.text(0.5, 0.06, "2 lines, bugs already fixed", ha="center",
            fontsize=12, color=GREEN, style="italic")

    fig.tight_layout()
    save(fig, out, "library_value")


# ============================================================ 2. the stack
def fig_ecosystem(out: Path) -> None:
    """One import sits on four layers and fifty years of numerical work."""
    fig, axes = plt.subplots(1, 2, figsize=WIDE, gridspec_kw={"width_ratios": [1, 1]})

    ax = axes[0]
    blank(ax)
    ax.set_title("What one import stands on", fontsize=13)
    layers = [
        ("your analysis", 0.88, PURPLE, "20 lines you wrote"),
        ("scikit-learn, pandas", 0.68, BLUE, "tables and models"),
        ("numpy", 0.48, GREEN, "arrays, one memory block"),
        ("BLAS, LAPACK (C, Fortran)", 0.28, AMBER, "the actual arithmetic"),
    ]
    for name, y, colour, what in layers:
        box(ax, (0.36, y), 0.64, 0.125, name, ec=colour, fs=11.5)
        ax.text(0.72, y, what, fontsize=10, color=GREY, va="center", ha="left")
    for y in (0.78, 0.58, 0.38):
        arrow(ax, (0.36, y + 0.032), (0.36, y - 0.032), color=GREY, lw=1.4)
    ax.text(0.02, 0.07, "you do not get to be better at matrix multiplication\n"
            "than fifty years of Fortran", fontsize=10.5, color=INK, ha="left")

    ax = axes[1]
    blank(ax)
    ax.set_title("The ones you will meet in health data", fontsize=13)
    rows = [
        ("numpy, pandas", "arrays and tables"),
        ("matplotlib, seaborn", "figures"),
        ("scikit-learn", "classical models"),
        ("statsmodels, lifelines", "statistics, survival"),
        ("pydicom, nibabel", "DICOM and NIfTI images"),
        ("torch", "neural networks"),
    ]
    for i, (lib, what) in enumerate(rows):
        y = 0.86 - i * 0.145
        ax.text(0.02, y, lib, fontsize=11.5, family=MONO, color=BLUE, va="center")
        ax.text(0.98, y, what, fontsize=11, color=GREY, va="center", ha="right")
        if i:
            ax.plot([0.0, 1.0], [y + 0.072, y + 0.072], color=FAINT, lw=0.8)
    ax.text(0.5, 0.02, "none of this ships with Python", ha="center",
            fontsize=11, color=AMBER)

    fig.tight_layout()
    save(fig, out, "ecosystem")


# ======================================================= 3. libraries move
def fig_versions(out: Path) -> None:
    """A library is a moving target, and sometimes it moves out from under you."""
    fig, axes = plt.subplots(2, 1, figsize=WIDE,
                             gridspec_kw={"height_ratios": [1, 1.1]})

    ax = axes[0]
    blank(ax)
    marks = [("1.3", 0.08, 2021, GREY), ("1.5", 0.30, 2022, GREY),
             ("2.0", 0.56, 2023, RED), ("2.2", 0.80, 2024, GREY)]
    ax.plot([0.04, 0.96], [0.52, 0.52], color=GREY, lw=2)
    for name, x, year, colour in marks:
        ax.plot([x], [0.52], "o", color=colour, ms=13, zorder=3)
        ax.text(x, 0.74, name, ha="center", fontsize=13, family=MONO, color=colour)
        ax.text(x, 0.30, str(year), ha="center", fontsize=10, color=GREY)
    ax.annotate("", (0.56, 0.08), (0.56, 0.20),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.6))
    ax.text(0.40, 0.0, "2.0 removed DataFrame.append()", fontsize=11.5, color=RED,
            ha="left", va="center")

    ax = axes[1]
    blank(ax)
    ax.text(0.02, 0.84, "code that worked for three years:", fontsize=11,
            color=GREY, ha="left")
    ax.text(0.02, 0.62, "cohort = cohort.append(new_rows)", fontsize=14,
            family=MONO, color=INK, ha="left")
    ax.text(0.02, 0.34, "AttributeError: 'DataFrame' object has no attribute 'append'",
            fontsize=13, family=MONO, color=RED, ha="left")

    fig.tight_layout()
    save(fig, out, "versions")


# ======================================================= 4. the collision
def fig_conflict(out: Path) -> None:
    """Two projects on one machine, two incompatible pins, one winner."""
    fig, ax = plt.subplots(figsize=WIDE)
    blank(ax)

    box(ax, (0.20, 0.82), 0.34, 0.20, "the 2022 cohort study", ec=GREY, fs=11)
    ax.text(0.20, 0.645, "written against pandas 1.5", ha="center", fontsize=10.5,
            color=INK)
    box(ax, (0.68, 0.82), 0.34, 0.20, "this year's imaging pipeline", ec=GREY, fs=11)
    ax.text(0.68, 0.645, "needs pandas 2.2", ha="center", fontsize=10.5, color=INK)

    arrow(ax, (0.20, 0.58), (0.40, 0.42), color=RED)
    arrow(ax, (0.68, 0.58), (0.48, 0.42), color=RED)
    box(ax, (0.44, 0.30), 0.44, 0.20, "one system python", ec=RED, fs=12)
    ax.text(0.44, 0.13, "pip install pandas==2.2", ha="center", fontsize=12,
            family=MONO, color=INK)
    ax.text(0.44, 0.03, "the 2022 cohort study stops running", ha="center",
            fontsize=11.5, color=RED, style="italic")
    save(fig, out, "conflict")


# ======================================================= 5. what a venv is
def fig_venv_anatomy(out: Path) -> None:
    """A virtual environment is a folder, and activation is a PATH edit."""
    fig, axes = plt.subplots(1, 2, figsize=WIDE, gridspec_kw={"width_ratios": [1, 1.1]})

    ax = axes[0]
    blank(ax)
    ax.set_title("It is just a folder", fontsize=13)
    tree = [
        ("project/", 0.04, 0.88, INK),
        (".venv/", 0.10, 0.74, GREEN),
        ("bin/", 0.17, 0.60, GREY),
        ("python3", 0.24, 0.47, GREEN),
        ("pip", 0.24, 0.35, GREEN),
        ("lib/python3.12/site-packages/", 0.17, 0.22, GREY),
        ("pandas/  numpy/  ...", 0.24, 0.09, GREEN),
    ]
    for name, x, y, colour in tree:
        ax.text(x, y, name, fontsize=12, family=MONO, color=colour, va="center")
    # elbow connectors, so the indentation reads as a tree rather than a list
    for (px, py), (cx, cy) in (((0.04, 0.88), (0.10, 0.74)),
                               ((0.10, 0.74), (0.17, 0.60)),
                               ((0.10, 0.74), (0.17, 0.22)),
                               ((0.17, 0.60), (0.24, 0.47)),
                               ((0.17, 0.60), (0.24, 0.35)),
                               ((0.17, 0.22), (0.24, 0.09))):
        stem = px + 0.016
        ax.plot([stem, stem], [py - 0.035, cy], color=FAINT, lw=1.6)
        ax.plot([stem, cx - 0.008], [cy, cy], color=FAINT, lw=1.6)
    ax.text(0.98, 0.74, "its own interpreter\nand its own packages",
            fontsize=10.5, color=GREEN, ha="right", va="center")

    ax = axes[1]
    blank(ax)
    ax.set_title("Activating it edits one variable", fontsize=13)
    ax.text(0.02, 0.84, "before", fontsize=11, color=GREY, ha="left")
    ax.text(0.02, 0.70, "PATH=/usr/bin:/bin", fontsize=12, family=MONO, color=INK,
            ha="left")
    ax.text(0.02, 0.56, "which python3   ->  /usr/bin/python3", fontsize=11.5,
            family=MONO, color=GREY, ha="left")
    arrow(ax, (0.12, 0.47), (0.12, 0.40), color=GREEN)
    ax.text(0.17, 0.435, "source .venv/bin/activate", fontsize=11, family=MONO,
            color=GREEN, va="center", ha="left")
    ax.text(0.02, 0.29, "after", fontsize=11, color=GREY, ha="left")
    ax.text(0.02, 0.17, "PATH=project/.venv/bin:/usr/bin:/bin", fontsize=12,
            family=MONO, color=GREEN, ha="left")
    ax.text(0.02, 0.04, "which python3   ->  project/.venv/bin/python3",
            fontsize=11.5, family=MONO, color=GREEN, ha="left")

    fig.tight_layout()
    save(fig, out, "venv_anatomy")


# ======================================================= 6. what pip does
def fig_pip_flow(out: Path) -> None:
    """pip install, in four steps, and where the files end up."""
    fig, ax = plt.subplots(figsize=WIDE)
    blank(ax)

    ax.text(0.02, 0.92, "pip install pandas", fontsize=16, family=MONO, color=INK,
            ha="left", va="center")

    stages = [
        ("PyPI", 0.10, "the public index,\n600 000 packages"),
        ("resolve", 0.33, "pandas needs numpy,\npython-dateutil, pytz"),
        ("download", 0.56, "wheels: prebuilt,\nplatform specific"),
        (".venv/", 0.79, "unpacked into\nsite-packages"),
    ]
    for name, x, what in stages:
        box(ax, (x, 0.55), 0.17, 0.20, name, ec=BLUE, fs=12, mono=True)
        ax.text(x, 0.33, what, ha="center", fontsize=10, color=GREY)
    for x0, x1 in zip([s[1] for s in stages], [s[1] for s in stages][1:]):
        arrow(ax, (x0 + 0.095, 0.55), (x1 - 0.095, 0.55), color=BLUE)

    ax.text(0.02, 0.14, "It installs into whichever environment is active right now.",
            fontsize=12, color=INK, ha="left")
    ax.text(0.02, 0.04, "That is the whole job. Nothing else about pip is a feature.",
            fontsize=11.5, color=GREY, ha="left")
    save(fig, out, "pip_flow")


# ======================================================= 7. what uv replaces
def fig_uv_tools(out: Path) -> None:
    """Five tools and their failure modes, or one binary."""
    fig, axes = plt.subplots(1, 2, figsize=WIDE)

    ax = axes[0]
    blank(ax)
    ax.set_title("Classic setup", fontsize=13)
    items = [("pyenv", "install Python itself"),
             ("venv", "create an environment"),
             ("pip", "install packages"),
             ("pipx", "install command line tools")]
    for i, (name, what) in enumerate(items):
        y = 0.84 - i * 0.165
        box(ax, (0.21, y), 0.30, 0.125, name, ec=GREY, fs=11.5, mono=True)
        ax.text(0.40, y, what, fontsize=10.5, color=GREY, va="center", ha="left")
    ax.text(0.5, 0.02, "Multiple tools", ha="center", fontsize=11.5, color=AMBER)

    ax = axes[1]
    blank(ax)
    ax.set_title("With uv", fontsize=13, color=GREEN)
    box(ax, (0.5, 0.88), 0.40, 0.14, "uv", ec=GREEN, fs=20, mono=True)
    cmds = [("uv python install 3.12", "the interpreter"),
            ("uv venv", "the environment"),
            ("uv pip install pandas", "the packages"),
            ("uv lock  /  uv sync", "the lock file"),
            ("uvx ruff check .", "a tool, run once")]
    for i, (cmd, what) in enumerate(cmds):
        y = 0.67 - i * 0.125
        ax.text(0.0, y, cmd, fontsize=11, family=MONO, color=INK, va="center")
        ax.text(1.0, y, what, fontsize=10.5, color=GREEN, va="center", ha="right")
    ax.text(0.5, 0.02, "Single tool", ha="center", fontsize=11.5, color=GREEN)

    fig.tight_layout()
    save(fig, out, "uv_tools")


# ======================================================= 8. why uv is good
def fig_uv_why(out: Path) -> None:
    """Speed is the headline; the lock file is the part that matters for science."""
#     fig, axes = plt.subplots(1, 2, figsize=WIDE, gridspec_kw={"width_ratios": [1, 1.15]})
#     ax = axes[0]
    fig, axes = plt.subplots(1, 1, figsize=WIDE)

    ax = axes
    ax.set_title("Installing pandas, scikit-learn, torch", fontsize=13)
    tools = ["pip", "uv (cold)", "uv (cached)"]
    secs = [52.0, 6.0, 1.1]
    colours = [GREY, GREEN, GREEN]
    ax.barh(range(3), secs, color=colours, height=0.55)
    ax.set_yticks(range(3))
    ax.set_yticklabels(tools, fontsize=11)
    ax.invert_yaxis()
    ax.set_xlabel("seconds (typical)", fontsize=10)
    ax.set_xlim(0, 60)
    for i, v in enumerate(secs):
        ax.text(v + 1.2, i, f"{v:g}s", va="center", fontsize=11, color=INK)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

#     ax = axes[1]
#     blank(ax)
#     ax.set_title("Will it install the same thing next year?", fontsize=13)
#     rows = [
#         ("pandas", RED, "whatever is newest the day you run it"),
#         ("pandas==2.2.1", AMBER, "pinned, but its dependencies are not"),
#         ("uv.lock", GREEN, "every package, every version, every hash"),
#     ]
#     for i, (what, colour, note) in enumerate(rows):
#         y = 0.76 - i * 0.26
#         box(ax, (0.26, y), 0.46, 0.16, what, ec=colour, fs=12, mono=True)
#         ax.text(0.53, y, note, fontsize=10.5, color=colour, va="center", ha="left")
#     ax.text(0.02, 0.06, "A result nobody can reinstall is a result nobody can check.",
#             fontsize=11.5, color=INK, ha="left")

#     fig.tight_layout()
    save(fig, out, "uv_why")


FIGURES = (
    fig_levels,
    fig_why_python,
    fig_common_tasks,
    fig_library_value,
    fig_ecosystem,
    fig_versions,
    fig_conflict,
    fig_venv_anatomy,
    fig_pip_flow,
    fig_uv_tools,
    fig_uv_why,
)


def main() -> None:
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "Programming01/Session00/img")
    out.mkdir(parents=True, exist_ok=True)
    for fn in FIGURES:
        fn(out)
        print(f"{out / (fn.__name__.removeprefix('fig_') + '.png')}")


if __name__ == "__main__":
    main()
