#!/usr/bin/env python3
"""Render the illustration figures used by the Programming01 Session01 slides.

Session01 is Python types: what a variable is, the single values (numbers, booleans,
strings, None), the four containers (list, tuple, dict, set), how they nest into
a patient record, and the numpy array that replaces lists for numbers. Every figure is synthetic and self contained, so `make figures`
reproduces the same output anywhere.

Usage: make_figures_c01.py [outdir]   (default: Programming01/Session01/img)
"""

from __future__ import annotations

import sys
from pathlib import Path

from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, FancyBboxPatch

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


def _cell(ax, x, y, w, h, text, ec=BLUE, fc="white", fs=11, tc=INK):
    """A square cell holding one value, used for lists, strings and tuples."""
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="square,pad=0",
            facecolor=fc,
            edgecolor=ec,
            linewidth=1.4,
        )
    )
    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=fs,
        family=MONO,
        color=tc,
    )


def _object(ax, xy, w, h, value, kind, colour):
    """A value in memory: the value itself, with its type written on the box."""
    box(ax, xy, w, h, value, ec=colour, fs=12, mono=True)
    ax.text(
        xy[0] + w / 2 - 0.01,
        xy[1] + h / 2 + 0.035,
        kind,
        ha="right",
        va="center",
        fontsize=10,
        color=colour,
        family=MONO,
    )


# ===================================================== 1. a name and a value
def fig_names(out: Path) -> None:
    """A variable is a label stuck on a value; the value carries the type."""
    fig, axes = plt.subplots(
        1, 2, figsize=WIDE, gridspec_kw={"width_ratios": [1.25, 1]}
    )

    ax = axes[0]
    blank(ax)
    ax.set_title("Names point to values", fontsize=13)
    ax.text(0.12, 0.95, "names", ha="center", fontsize=10.5, color=GREY)
    ax.text(0.68, 0.95, "values (in memory)", ha="center", fontsize=10.5, color=GREY)
    rows = [
        ("age", "54", "int", BLUE),
        ("temp", "38.4", "float", PURPLE),
        ("fever", "True", "bool", GREEN),
        ("name", '"Ada"', "str", AMBER),
    ]
    for i, (name, value, kind, colour) in enumerate(rows):
        y = 0.78 - i * 0.21
        box(ax, (0.12, y), 0.18, 0.11, name, ec=GREY, fs=12, mono=True)
        _object(ax, (0.68, y), 0.34, 0.13, value, kind, colour)
        arrow(ax, (0.22, y), (0.50, y), color=GREY)

    ax = axes[1]
    blank(ax)
    ax.set_title("Ask a value for its type", fontsize=13)
    ax.add_patch(
        FancyBboxPatch(
            (0.02, 0.18),
            0.96,
            0.70,
            boxstyle="round,pad=0.01,rounding_size=0.03",
            facecolor="#fbfbfb",
            edgecolor=GREY,
            linewidth=1.4,
        )
    )
    lines = [
        (">>> age = 54", INK),
        (">>> type(age)", INK),
        ("<class 'int'>", BLUE),
        (">>> type(38.4)", INK),
        ("<class 'float'>", PURPLE),
        ('>>> type("Ada")', INK),
        ("<class 'str'>", AMBER),
    ]
    for i, (line, colour) in enumerate(lines):
        ax.text(
            0.07,
            0.81 - i * 0.087,
            line,
            fontsize=11,
            family=MONO,
            color=colour,
            va="center",
            ha="left",
        )
    ax.text(
        0.5,
        0.06,
        "No declaration: the type comes with the value",
        ha="center",
        fontsize=11,
        color=INK,
    )

    fig.tight_layout()
    save(fig, out, "names")


# ====================================================== 1b. the type family
def fig_type_map(out: Path) -> None:
    """Five single values, four containers: the whole of this session."""
    fig, axes = plt.subplots(
        1, 2, figsize=WIDE, gridspec_kw={"width_ratios": [1, 1.15]}
    )

    ax = axes[0]
    blank(ax)
    ax.set_title("Single values", fontsize=13, color=BLUE)
    singles = [
        ("int", "54", "age, heart rate, count"),
        ("float", "38.4", "temperature, weight"),
        ("bool", "True", "fever?  smoker?"),
        ("str", '"P001"', "id, name, diagnosis"),
        ("None", "None", "a missing measurement"),
    ]
    for i, (kind, example, what) in enumerate(singles):
        y = 0.86 - i * 0.18
        box(ax, (0.12, y), 0.20, 0.12, kind, ec=BLUE, fs=12, mono=True)
        ax.text(0.27, y, example, fontsize=11.5, family=MONO, color=INK, va="center")
        ax.text(0.56, y, what, fontsize=10.5, color=GREY, va="center")

    ax = axes[1]
    blank(ax)
    ax.set_title("Containers (hold other values)", fontsize=13, color=GREEN)
    containers = [
        ("list", "[72, 85, 64]", "heart rates over time"),
        ("tuple", "(120, 80)", "a blood pressure"),
        ("dict", '{"age": 54}', "a patient record"),
        ("set", '{"aspirin"}', "distinct medications"),
    ]
    for i, (kind, example, what) in enumerate(containers):
        y = 0.86 - i * 0.18
        box(ax, (0.12, y), 0.18, 0.12, kind, ec=GREEN, fs=12, mono=True)
        ax.text(0.25, y, example, fontsize=11.5, family=MONO, color=INK, va="center")
        ax.text(0.62, y, what, fontsize=10.5, color=GREY, va="center")
    ax.text(
        0.5,
        0.06,
        "and containers can hold containers",
        ha="center",
        fontsize=11,
        color=INK,
    )

    fig.tight_layout()
    save(fig, out, "type_map")


# ====================================================== 2. int and float
def fig_numbers(out: Path) -> None:
    """int is exact and unbounded; float is approximate and bounded."""
    fig, axes = plt.subplots(1, 2, figsize=WIDE)

    ax = axes[0]
    blank(ax)
    ax.set_title("int: exact, no maximum", fontsize=13, color=BLUE)
    rows = [
        (">>> 2 ** 100", INK),
        ("1267650600228229401496703205376", BLUE),
        (">>> 7 // 2,  7 % 2", INK),
        ("(3, 1)", BLUE),
    ]
    for i, (line, colour) in enumerate(rows):
        ax.text(
            0.04,
            0.85 - i * 0.11,
            line,
            fontsize=11,
            family=MONO,
            color=colour,
            va="center",
            ha="left",
        )
    ax.text(0.04, 0.10, "counts, ages, indices", fontsize=10.5, color=GREY, ha="left")

    ax = axes[1]
    blank(ax)
    ax.set_title("float: approximate, 15-16 digits", fontsize=13, color=PURPLE)
    rows = [
        (">>> 0.1 + 0.2", INK),
        ("0.30000000000000004", RED),
        (">>> 0.1 + 0.2 == 0.3", INK),
        ("False", RED),
        (">>> math.isclose(0.1 + 0.2, 0.3)", INK),
        ("True", GREEN),
    ]
    for i, (line, colour) in enumerate(rows):
        ax.text(
            0.04,
            0.85 - i * 0.11,
            line,
            fontsize=11,
            family=MONO,
            color=colour,
            va="center",
            ha="left",
        )
    ax.text(
        0.04,
        0.10,
        "0.1 has no exact binary form, like 1/3 in decimal",
        fontsize=10.5,
        color=GREY,
        ha="left",
    )

    fig.text(
        0.5,
        0.04,
        "Never compare two floats with ==",
        ha="center",
        fontsize=11.5,
        color=INK,
    )
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    save(fig, out, "numbers")


# ===================================================== 2b. truthiness
def fig_truthy(out: Path) -> None:
    """Every value can stand in a condition: empty and zero are False."""
    fig, ax = plt.subplots(figsize=WIDE)
    blank(ax)

    ax.text(0.25, 0.92, "falsy:  bool(x) is False", ha="center", fontsize=13, color=RED)
    ax.text(
        0.75, 0.92, "truthy:  everything else", ha="center", fontsize=13, color=GREEN
    )
    falsy = ["0", "0.0", '""', "[]", "{}", "None", "False"]
    truthy = ["1", "-1", "0.5", '"0"', '" "', "[0]", '{"a": 0}']
    for col, (values, colour) in enumerate(((falsy, RED), (truthy, GREEN))):
        x0 = 0.05 + col * 0.50
        for i, v in enumerate(values):
            x = x0 + (i % 4) * 0.115
            y = 0.70 - (i // 4) * 0.22
            box(ax, (x + 0.04, y), 0.085, 0.14, v, ec=colour, fs=12, mono=True)
    ax.plot([0.5, 0.5], [0.30, 0.88], color=FAINT, lw=2)

    ax.text(
        0.02,
        0.16,
        "if heart_rates:",
        fontsize=12,
        family=MONO,
        color=INK,
        ha="left",
        va="center",
    )
    ax.text(
        0.30,
        0.16,
        'means "if the list is not empty"',
        fontsize=11,
        color=GREY,
        ha="left",
        va="center",
    )
    ax.text(
        0.02,
        0.05,
        '"0" is a string with one character: truthy',
        fontsize=11,
        color=AMBER,
        ha="left",
        va="center",
    )
    save(fig, out, "truthy")


# ===================================================== 3. string indexing
def fig_string_index(out: Path) -> None:
    """A string is a sequence of characters, indexed from 0 and from -1."""
    fig, ax = plt.subplots(figsize=WIDE)
    blank(ax)

    s = "Ada Lovelace"
    w, h, x0, y0 = 0.062, 0.16, 0.13, 0.52
    for i, ch in enumerate(s):
        in_slice = i < 3
        _cell(
            ax,
            x0 + i * w,
            y0,
            w,
            h,
            ch if ch != " " else "␣",
            ec=(BLUE if in_slice else GREY),
            fc=("#eef3fa" if in_slice else "white"),
            fs=15,
        )
        ax.text(
            x0 + (i + 0.5) * w,
            y0 + h + 0.05,
            str(i),
            ha="center",
            fontsize=10.5,
            color=BLUE,
            family=MONO,
        )
        ax.text(
            x0 + (i + 0.5) * w,
            y0 - 0.05,
            str(i - len(s)),
            ha="center",
            fontsize=10.5,
            color=PURPLE,
            family=MONO,
        )
    ax.text(x0 - 0.02, y0 + h + 0.05, "index", ha="right", fontsize=10.5, color=BLUE)
    ax.text(
        x0 - 0.02, y0 - 0.05, "from the end", ha="right", fontsize=10.5, color=PURPLE
    )

    examples = [
        ("name[0]", "'A'"),
        ("name[-1]", "'e'"),
        ("name[:3]", "'Ada'"),
        ("len(name)", "12"),
    ]
    for i, (expr, val) in enumerate(examples):
        x = 0.02 + i * 0.25
        ax.text(x, 0.24, expr, fontsize=12.5, family=MONO, color=INK, ha="left")
        ax.text(
            x + 0.125,
            0.24,
            "-> " + val,
            fontsize=12.5,
            family=MONO,
            color=BLUE,
            ha="left",
        )
    ax.text(
        0.5,
        0.07,
        'name[0] = "E"  ->  TypeError: a string cannot be changed, build a new one',
        ha="center",
        fontsize=11,
        color=RED,
    )
    save(fig, out, "string_index")


# ===================================================== 4. conversions
def fig_conversions(out: Path) -> None:
    """Text from a file is text until you convert it; some conversions fail."""
    fig, ax = plt.subplots(figsize=WIDE)
    blank(ax)

    ax.text(0.02, 0.92, "A CSV gives you text:", fontsize=12, color=INK, ha="left")
    ax.text(
        0.27,
        0.92,
        '"54"   "81.5"   ""',
        fontsize=12,
        family=MONO,
        color=AMBER,
        ha="left",
    )

    box(ax, (0.12, 0.55), 0.16, 0.16, "str", ec=AMBER, fs=14, mono=True)
    box(ax, (0.50, 0.75), 0.16, 0.14, "int", ec=BLUE, fs=14, mono=True)
    box(ax, (0.50, 0.35), 0.16, 0.14, "float", ec=PURPLE, fs=14, mono=True)
    arrow(ax, (0.20, 0.60), (0.42, 0.74), color=BLUE)
    arrow(ax, (0.20, 0.50), (0.42, 0.37), color=PURPLE)
    ax.text(0.25, 0.73, 'int("54")', fontsize=11, family=MONO, color=BLUE, ha="left")
    ax.text(
        0.22, 0.38, 'float("81.5")', fontsize=11, family=MONO, color=PURPLE, ha="left"
    )
    arrow(ax, (0.50, 0.68), (0.50, 0.42), color=GREY, style="<|-|>")
    ax.text(
        0.52,
        0.55,
        "float(54)\nint(81.5) -> 81",
        fontsize=10.5,
        family=MONO,
        color=GREY,
        ha="left",
        va="center",
        linespacing=1.6,
    )

    ax.text(0.76, 0.80, "fails loudly", fontsize=11.5, color=RED, ha="left")
    ax.text(0.76, 0.71, 'int("3.5")', fontsize=11, family=MONO, color=INK, ha="left")
    ax.text(0.76, 0.64, "ValueError", fontsize=11, family=MONO, color=RED, ha="left")
    ax.text(0.76, 0.52, '"Age: " + 42', fontsize=11, family=MONO, color=INK, ha="left")
    ax.text(0.76, 0.45, "TypeError", fontsize=11, family=MONO, color=RED, ha="left")
    ax.text(0.76, 0.33, "int() truncates", fontsize=11.5, color=AMBER, ha="left")
    ax.text(
        0.76, 0.24, "int(-3.9) -> -3", fontsize=11, family=MONO, color=INK, ha="left"
    )

    ax.text(0.02, 0.06, "missing value:", fontsize=12, color=INK, ha="left")
    ax.text(
        0.20,
        0.06,
        "glucose = None      if glucose is None: ...",
        fontsize=12,
        family=MONO,
        color=GREEN,
        ha="left",
    )
    save(fig, out, "conversions")


# ===================================================== 5. the four containers
def fig_containers(out: Path) -> None:
    """list, tuple, dict, set: drawn, then their three properties."""
    fig, axes = plt.subplots(1, 4, figsize=WIDE)
    specs = [
        ("list", BLUE, "[72, 85, 64]", "ordered\nchangeable\nduplicates ok"),
        ("tuple", PURPLE, "(120, 80)", "ordered\nfixed\nduplicates ok"),
        (
            "dict",
            GREEN,
            '{"id": "P001",\n "age": 54}',
            "key -> value\nchangeable\nunique keys",
        ),
        (
            "set",
            AMBER,
            '{"aspirin",\n "insulin"}',
            "no order\nchangeable\nno duplicates",
        ),
    ]
    for ax, (kind, colour, literal, props) in zip(axes, specs):
        blank(ax)
        ax.set_title(kind, fontsize=14, color=colour, family=MONO)
        if kind == "list":
            for i, v in enumerate(("72", "85", "64")):
                _cell(ax, 0.10 + i * 0.27, 0.66, 0.27, 0.16, v, ec=colour)
                ax.text(
                    0.235 + i * 0.27,
                    0.86,
                    str(i),
                    ha="center",
                    fontsize=9.5,
                    color=GREY,
                    family=MONO,
                )
        elif kind == "tuple":
            for i, v in enumerate(("120", "80")):
                _cell(ax, 0.16 + i * 0.34, 0.66, 0.34, 0.16, v, ec=colour, fc="#f3effa")
                ax.text(
                    0.33 + i * 0.34,
                    0.86,
                    str(i),
                    ha="center",
                    fontsize=9.5,
                    color=GREY,
                    family=MONO,
                )
        elif kind == "dict":
            for i, (k, v) in enumerate((('"id"', '"P001"'), ('"age"', "54"))):
                y = 0.76 - i * 0.14
                _cell(ax, 0.04, y, 0.42, 0.12, k, ec=colour, fc="#eafaec", fs=10)
                _cell(ax, 0.54, y, 0.42, 0.12, v, ec=colour, fs=10)
                arrow(ax, (0.46, y + 0.06), (0.54, y + 0.06), color=colour, lw=1.2)
        else:
            ax.add_patch(
                Ellipse(
                    (0.5, 0.72),
                    0.70,
                    0.40,
                    facecolor="#fdf6e9",
                    edgecolor=colour,
                    lw=1.4,
                )
            )
            ax.text(0.42, 0.77, "aspirin", fontsize=9.5, family=MONO, ha="center")
            ax.text(0.57, 0.66, "insulin", fontsize=9.5, family=MONO, ha="center")
        ax.text(
            0.5,
            0.43,
            literal,
            ha="center",
            va="center",
            fontsize=10.5,
            family=MONO,
            color=INK,
        )
        ax.text(
            0.5,
            0.12,
            props,
            ha="center",
            va="center",
            fontsize=10.5,
            color=GREY,
            linespacing=1.5,
        )

    fig.tight_layout()
    save(fig, out, "containers")


# ===================================================== 5b. two names, one list
def fig_aliasing(out: Path) -> None:
    """b = a copies the arrow, not the list."""
    fig, axes = plt.subplots(1, 2, figsize=WIDE)

    for ax, title, colour, copy in (
        (axes[0], "b = a", RED, False),
        (axes[1], "b = a.copy()", GREEN, True),
    ):
        blank(ax)
        ax.set_title(title, fontsize=14, color=colour, family=MONO)
        box(ax, (0.12, 0.72), 0.14, 0.12, "a", ec=GREY, fs=13, mono=True)
        box(ax, (0.12, 0.38), 0.14, 0.12, "b", ec=GREY, fs=13, mono=True)
        values_a = ("1", "2", "3") if copy else ("1", "2", "3", "4")
        for i, v in enumerate(values_a):
            _cell(ax, 0.44 + i * 0.11, 0.65, 0.11, 0.14, v, ec=BLUE, fs=12)
        if copy:
            for i, v in enumerate(("1", "2", "3", "4")):
                _cell(
                    ax,
                    0.44 + i * 0.11,
                    0.31,
                    0.11,
                    0.14,
                    v,
                    ec=(GREEN if i == 3 else BLUE),
                    fc=("#eafaec" if i == 3 else "white"),
                    fs=12,
                )
            arrow(ax, (0.20, 0.72), (0.43, 0.72), color=GREY)
            arrow(ax, (0.20, 0.38), (0.43, 0.38), color=GREY)
            ax.text(
                0.5,
                0.12,
                "print(a)  ->  [1, 2, 3]",
                ha="center",
                fontsize=12,
                family=MONO,
                color=GREEN,
            )
        else:
            _cell(
                ax, 0.44 + 3 * 0.11, 0.65, 0.11, 0.14, "4", ec=RED, fc="#fbeaea", fs=12
            )
            arrow(ax, (0.20, 0.72), (0.43, 0.72), color=GREY)
            arrow(ax, (0.20, 0.38), (0.43, 0.66), color=GREY)
            ax.text(
                0.5,
                0.12,
                "print(a)  ->  [1, 2, 3, 4]",
                ha="center",
                fontsize=12,
                family=MONO,
                color=RED,
            )
        ax.text(
            0.5,
            0.24,
            "then  b.append(4)",
            ha="center",
            fontsize=11,
            family=MONO,
            color=GREY,
        )

    fig.text(
        0.5,
        0.02,
        "Assignment never copies: it adds a name to the same value",
        ha="center",
        fontsize=11.5,
        color=INK,
    )
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    save(fig, out, "aliasing")


# ===================================================== 6. a patient record
def fig_dict_record(out: Path) -> None:
    """A dict is a record: look values up by name, not by position."""
    fig, axes = plt.subplots(1, 2, figsize=WIDE, gridspec_kw={"width_ratios": [1, 1.1]})

    ax = axes[0]
    blank(ax)
    ax.set_title("patient", fontsize=14, family=MONO, color=GREEN)
    rows = [
        ('"id"', '"P001"'),
        ('"age"', "54"),
        ('"weight"', "81.5"),
        ('"diagnoses"', '["hypertension"]'),
    ]
    for i, (k, v) in enumerate(rows):
        y = 0.76 - i * 0.17
        _cell(ax, 0.02, y, 0.34, 0.13, k, ec=GREEN, fc="#eafaec", fs=11)
        _cell(ax, 0.44, y, 0.54, 0.13, v, ec=GREEN, fs=11)
        arrow(ax, (0.36, y + 0.065), (0.44, y + 0.065), color=GREEN, lw=1.2)
    ax.text(0.19, 0.92, "keys", ha="center", fontsize=10.5, color=GREY)
    ax.text(0.71, 0.92, "values", ha="center", fontsize=10.5, color=GREY)

    ax = axes[1]
    blank(ax)
    ax.set_title("Look up by key", fontsize=13)
    lines = [
        ('patient["age"]', "54", BLUE),
        ('patient["height"] = 1.78', "adds a key", GREY),
        ('patient["smoker"]', "KeyError", RED),
        ('patient.get("smoker", "unknown")', '"unknown"', GREEN),
        ('"smoker" in patient', "False", BLUE),
    ]
    for i, (expr, res, colour) in enumerate(lines):
        y = 0.82 - i * 0.16
        ax.text(
            0.0, y, expr, fontsize=11, family=MONO, color=INK, ha="left", va="center"
        )
        ax.text(
            0.0,
            y - 0.065,
            "-> " + res,
            fontsize=10.5,
            family=MONO,
            color=colour,
            ha="left",
            va="center",
        )

    fig.tight_layout()
    save(fig, out, "dict_record")


# ===================================================== 7. set operations
def fig_sets(out: Path) -> None:
    """Two medication lists, three questions, three operators."""
    fig, axes = plt.subplots(1, 2, figsize=WIDE, gridspec_kw={"width_ratios": [1, 1]})

    ax = axes[0]
    blank(ax)
    ax.set_aspect("equal")
    ax.add_patch(
        Circle((0.36, 0.50), 0.30, facecolor=BLUE, alpha=0.12, edgecolor=BLUE, lw=1.6)
    )
    ax.add_patch(
        Circle((0.64, 0.50), 0.30, facecolor=GREEN, alpha=0.12, edgecolor=GREEN, lw=1.6)
    )
    ax.text(0.22, 0.86, "a", fontsize=14, family=MONO, color=BLUE, ha="center")
    ax.text(0.78, 0.86, "b", fontsize=14, family=MONO, color=GREEN, ha="center")
    ax.text(0.24, 0.56, "aspirin", fontsize=10.5, family=MONO, ha="center")
    ax.text(0.24, 0.42, "metformin", fontsize=10.5, family=MONO, ha="center")
    ax.text(0.50, 0.50, "insulin", fontsize=10.5, family=MONO, ha="center")
    ax.text(0.77, 0.50, "statin", fontsize=10.5, family=MONO, ha="center")

    ax = axes[1]
    blank(ax)
    ax.set_title("Questions as operators", fontsize=13)
    ops = [
        ("a & b", "{'insulin'}", "taken by both"),
        ("a | b", "{'aspirin', 'insulin',\n 'metformin', 'statin'}", "taken by either"),
        ("a - b", "{'aspirin', 'metformin'}", "only by a"),
    ]
    for i, (op, res, what) in enumerate(ops):
        y = 0.80 - i * 0.25
        ax.text(0.0, y, op, fontsize=13, family=MONO, color=INK, ha="left", va="center")
        ax.text(
            0.22, y, res, fontsize=10.5, family=MONO, color=BLUE, ha="left", va="center"
        )
        ax.text(0.22, y - 0.10, what, fontsize=10.5, color=GREY, ha="left", va="center")
    ax.text(
        0.0,
        0.06,
        'set(["aspirin", "aspirin"])  ->  {"aspirin"}',
        fontsize=10.5,
        family=MONO,
        color=AMBER,
        ha="left",
    )

    fig.tight_layout()
    save(fig, out, "sets")


# ===================================================== 8. nesting
def fig_nested(out: Path) -> None:
    """A ward: a list of dicts, each holding a list. Read the path left to right."""
    fig, ax = plt.subplots(figsize=WIDE)
    blank(ax)

    ax.text(0.02, 0.90, "patients", fontsize=13, family=MONO, color=BLUE, ha="left")
    ax.text(0.16, 0.90, "a list ...", fontsize=10.5, color=GREY, ha="left")
    for i in range(5):
        hot = i == 2
        _cell(
            ax,
            0.02 + i * 0.07,
            0.68,
            0.07,
            0.14,
            "{...}",
            ec=BLUE,
            fc=("#eef3fa" if hot else "white"),
            fs=10,
        )
        ax.text(
            0.055 + i * 0.07,
            0.62,
            str(i),
            ha="center",
            fontsize=9.5,
            color=GREY,
            family=MONO,
        )

    ax.add_patch(
        FancyArrowPatch(
            (0.195, 0.83),
            (0.43, 0.79),
            arrowstyle="-|>",
            mutation_scale=14,
            color=BLUE,
            lw=1.8,
            connectionstyle="arc3,rad=-0.3",
        )
    )
    ax.text(0.44, 0.90, "... of dicts ...", fontsize=10.5, color=GREY, ha="left")
    rows = [('"id"', '"P003"'), ('"age"', "71"), ('"diagnoses"', "[...]")]
    for i, (k, v) in enumerate(rows):
        y = 0.73 - i * 0.12
        hot = i == 2
        _cell(
            ax,
            0.44,
            y,
            0.16,
            0.10,
            k,
            ec=GREEN,
            fc=("#eafaec" if hot else "white"),
            fs=10,
        )
        _cell(ax, 0.60, y, 0.10, 0.10, v, ec=GREEN, fs=10)

    arrow(ax, (0.70, 0.54), (0.76, 0.60), color=GREEN)
    ax.text(0.77, 0.90, "... of lists", fontsize=10.5, color=GREY, ha="left")
    _cell(ax, 0.77, 0.58, 0.20, 0.12, '"diabetes"', ec=AMBER, fc="#fdf6e9", fs=10.5)
    ax.text(0.87, 0.53, "0", ha="center", fontsize=9.5, color=GREY, family=MONO)

    expr = [("patients", BLUE), ("[2]", BLUE), ('["diagnoses"]', GREEN), ("[0]", AMBER)]
    # place each piece right after the previous one, measured once it is drawn
    renderer = fig.canvas.get_renderer()
    x = 0.12
    for piece, colour in expr:
        t = ax.text(
            x,
            0.22,
            piece,
            fontsize=15,
            family=MONO,
            color=colour,
            ha="left",
            va="center",
        )
        right = t.get_window_extent(renderer).x1
        x = ax.transData.inverted().transform((right, 0))[0]
    ax.text(
        x + 0.02,
        0.22,
        '->  "diabetes"',
        fontsize=15,
        family=MONO,
        color=INK,
        ha="left",
        va="center",
    )
    ax.text(
        0.5,
        0.07,
        "one bracket per level, read left to right",
        ha="center",
        fontsize=11,
        color=GREY,
    )
    save(fig, out, "nested")


# ===================================================== 9. list vs array
def fig_list_vs_array(out: Path) -> None:
    """A list holds arrows to scattered objects; an array is one block of numbers."""
    fig, axes = plt.subplots(1, 2, figsize=WIDE, gridspec_kw={"width_ratios": [1.3, 1]})

    ax = axes[0]
    blank(ax)
    ax.text(
        0.0, 0.95, "list", fontsize=13, family=MONO, color=BLUE, ha="left", va="center"
    )
    ax.text(
        0.12,
        0.95,
        "arrows to separate objects, any type",
        fontsize=10.5,
        color=GREY,
        ha="left",
        va="center",
    )
    for i in range(4):
        _cell(ax, 0.02 + i * 0.09, 0.56, 0.09, 0.12, "\u2022", ec=BLUE)
    spots = [
        (0.12, 0.82, "72"),
        (0.34, 0.78, "85"),
        (0.56, 0.83, "64"),
        (0.78, 0.77, '"x"'),
    ]
    for i, (x, y, v) in enumerate(spots):
        box(
            ax,
            (x, y),
            0.10,
            0.08,
            v,
            ec=(AMBER if v == '"x"' else GREY),
            fs=10.5,
            mono=True,
        )
        arrow(ax, (0.065 + i * 0.09, 0.62), (x, y - 0.05), color=GREY, lw=1.2)

    ax.text(0.0, 0.40, "np.ndarray", fontsize=13, family=MONO, color=GREEN, ha="left")
    ax.text(
        0.25,
        0.40,
        "one block of memory, one dtype",
        fontsize=10.5,
        color=GREY,
        ha="left",
    )
    for i, v in enumerate(("72", "85", "64", "90", "78", "101")):
        _cell(ax, 0.02 + i * 0.09, 0.17, 0.09, 0.12, v, ec=GREEN, fc="#eafaec")
    ax.text(
        0.58,
        0.23,
        "int64",
        fontsize=11,
        family=MONO,
        color=GREEN,
        ha="left",
        va="center",
    )
    ax.text(
        0.0,
        0.03,
        "compiled code walks the block without asking Python",
        fontsize=10.5,
        color=INK,
        ha="left",
    )

    ax = axes[1]
    ax.set_title("Sum of squares, 1 000 000 integers", fontsize=12)
    labels = ["Python loop", "NumPy"]
    ms = [36.0, 0.63]
    ax.barh(range(2), ms, color=[GREY, GREEN], height=0.5)
    ax.set_yticks(range(2))
    ax.set_yticklabels(labels, fontsize=11)
    ax.invert_yaxis()
    ax.set_xlabel("milliseconds (measured on a laptop)", fontsize=10)
    ax.set_xlim(0, 45)
    for i, v in enumerate(ms):
        ax.text(v + 0.8, i, f"{v:g} ms", va="center", fontsize=11, color=INK)
    ax.text(22, 1.0, "about 60x faster", va="center", fontsize=11.5, color=GREEN)

    fig.tight_layout()
    save(fig, out, "list_vs_array")


# ===================================================== 9b. shape and dtype
def fig_ndarray(out: Path) -> None:
    """Shape is the size along each axis; dtype is the one type of every cell."""
    fig, axes = plt.subplots(
        1, 3, figsize=WIDE, gridspec_kw={"width_ratios": [1, 1.1, 1]}
    )

    ax = axes[0]
    blank(ax)
    ax.set_title("np.array([1, 2, 3, 4])", fontsize=11, family=MONO)
    for i in range(4):
        _cell(ax, 0.10 + i * 0.2, 0.55, 0.2, 0.14, str(i + 1), ec=BLUE)
    arrow(ax, (0.10, 0.45), (0.90, 0.45), color=BLUE)
    ax.text(0.5, 0.39, "axis 0", ha="center", fontsize=10, color=BLUE, va="top")
    ax.text(
        0.5,
        0.18,
        "shape (4,)   ndim 1\ndtype int64",
        ha="center",
        fontsize=11,
        family=MONO,
        color=INK,
        linespacing=1.6,
    )

    ax = axes[1]
    blank(ax)
    ax.set_title("np.array([[1, 2], [3, 4]])", fontsize=11, family=MONO)
    for r in range(2):
        for c in range(2):
            _cell(
                ax,
                0.30 + c * 0.2,
                0.66 - r * 0.14,
                0.2,
                0.14,
                str(2 * r + c + 1),
                ec=PURPLE,
            )
    arrow(ax, (0.24, 0.80), (0.24, 0.52), color=PURPLE)
    ax.text(
        0.22, 0.66, "axis 0\nrows", ha="right", va="center", fontsize=10, color=PURPLE
    )
    arrow(ax, (0.30, 0.86), (0.70, 0.86), color=AMBER)
    ax.text(
        0.72, 0.86, "axis 1, columns", ha="left", va="center", fontsize=10, color=AMBER
    )
    ax.text(
        0.5,
        0.18,
        "shape (2, 2)   ndim 2\ndtype int64",
        ha="center",
        fontsize=11,
        family=MONO,
        color=INK,
        linespacing=1.6,
    )

    ax = axes[2]
    blank(ax)
    ax.set_title("np.array([1.0, 2, 3, 4])", fontsize=11, family=MONO)
    for i, v in enumerate(("1.", "2.", "3.", "4.")):
        _cell(ax, 0.10 + i * 0.2, 0.55, 0.2, 0.14, v, ec=RED if i else GREY)
    ax.text(
        0.5,
        0.40,
        "one float: every cell\nbecomes a float",
        ha="center",
        fontsize=10.5,
        color=RED,
        va="top",
        linespacing=1.5,
    )
    ax.text(
        0.5,
        0.18,
        "shape (4,)   ndim 1\ndtype float64",
        ha="center",
        fontsize=11,
        family=MONO,
        color=INK,
        linespacing=1.6,
    )

    fig.tight_layout()
    save(fig, out, "ndarray")


# ===================================================== 9c. inside a float
FLOATS = (  # name, exponent bits, mantissa bits, significant digits, largest value
    ("float64", 11, 52, "~16 digits", "1.8e308"),
    ("float32", 8, 23, "~7 digits", "3.4e38"),
    ("float16", 5, 10, "~3 digits", "65 504"),
    ("float8 (e4m3)", 4, 3, "~1 digit", "448"),
)


def fig_float_bits(out: Path) -> None:
    """Sign, exponent, mantissa: fewer bits, fewer digits, smaller range."""
    fig, ax = plt.subplots(figsize=WIDE)
    blank(ax)

    x0, unit = 0.17, 0.0085  # one bit, in axes units: float64 spans 0.54
    ax.text(
        x0 + 64 * unit + 0.03, 0.93, "precision", fontsize=10.5, color=GREY, ha="left"
    )
    ax.text(
        x0 + 64 * unit + 0.17, 0.93, "largest", fontsize=10.5, color=GREY, ha="left"
    )
    for i, (name, nexp, nmant, digits, top) in enumerate(FLOATS):
        y = 0.76 - i * 0.19
        ax.text(
            x0 - 0.02,
            y,
            name,
            ha="right",
            va="center",
            fontsize=12,
            family=MONO,
            color=INK,
        )
        x = x0
        for n, colour, fill in (
            (1, RED, "#fbeaea"),
            (nexp, BLUE, "#eef3fa"),
            (nmant, GREEN, "#eafaec"),
        ):
            ax.add_patch(
                FancyBboxPatch(
                    (x, y - 0.055),
                    n * unit,
                    0.11,
                    boxstyle="square,pad=0",
                    facecolor=fill,
                    edgecolor=colour,
                    linewidth=1.2,
                )
            )
            if n * unit > 0.02:
                ax.text(
                    x + n * unit / 2,
                    y,
                    str(n),
                    ha="center",
                    va="center",
                    fontsize=10,
                    color=colour,
                )
            x += n * unit
        ax.text(
            x0 + 64 * unit + 0.03,
            y,
            digits,
            va="center",
            fontsize=11,
            color=INK,
            ha="left",
        )
        ax.text(
            x0 + 64 * unit + 0.17,
            y,
            top,
            va="center",
            fontsize=11,
            family=MONO,
            color=INK,
            ha="left",
        )

    for i, (label, colour) in enumerate(
        (("sign", RED), ("exponent: the range", BLUE), ("mantissa: the digits", GREEN))
    ):
        x = (0.17, 0.29, 0.54)[i]
        ax.add_patch(
            FancyBboxPatch(
                (x, 0.035),
                0.02,
                0.04,
                boxstyle="square,pad=0",
                facecolor="white",
                edgecolor=colour,
                lw=1.4,
            )
        )
        ax.text(x + 0.03, 0.055, label, fontsize=10.5, color=colour, va="center")
    save(fig, out, "float_bits")


# ===================================================== 9d. what each float stores
def fig_float_precision(out: Path) -> None:
    """The same measurements, stored in four float types (values computed by numpy)."""
    import ml_dtypes
    import numpy as np

    types = (
        ("float64", np.float64),
        ("float32", np.float32),
        ("float16", np.float16),
        ("float8", ml_dtypes.float8_e4m3fn),
    )
    values = (
        ("38.4", "temperature (°C)"),
        ("72.3", "weight (kg)"),
        ("1000.4", "platelets (10⁹/L)"),
        ("3.141592653589793", "pi"),
    )

    fig, ax = plt.subplots(figsize=WIDE)
    blank(ax)
    cols = (0.20, 0.42, 0.62, 0.80)
    for x, (name, _) in zip(cols, types):
        ax.text(x, 0.92, name, ha="left", fontsize=12, family=MONO, color=INK)
    for i, (text, what) in enumerate(values):
        y = 0.74 - i * 0.17
        ax.text(
            0.0,
            y + 0.025,
            text if len(text) < 8 else "3.14159...",
            fontsize=12,
            family=MONO,
            color=INK,
            ha="left",
            va="center",
        )
        ax.text(0.0, y - 0.045, what, fontsize=10, color=GREY, ha="left", va="center")
        exact = float(text)
        for x, (name, t) in zip(cols, types):
            stored = float(np.array(exact).astype(t))
            if np.isnan(stored):
                shown, colour = "nan (too big)", RED
            else:
                shown = f"{stored:.10g}" if name != "float64" else f"{stored:.15g}"
                err = abs(stored - exact) / exact
                colour = GREEN if err < 1e-6 else (AMBER if err < 1e-2 else RED)
            ax.text(
                x,
                y,
                shown,
                fontsize=11.5,
                family=MONO,
                color=colour,
                ha="left",
                va="center",
            )
    ax.text(0.0, 0.03, "error:  ", fontsize=10.5, color=GREY, ha="left")
    for i, (label, colour) in enumerate(
        (("< 1 in a million", GREEN), ("< 1 %", AMBER), ("clinically wrong", RED))
    ):
        ax.text(0.08 + i * 0.18, 0.03, label, fontsize=10.5, color=colour, ha="left")
    save(fig, out, "float_precision")


# ===================================================== 9e. memory
def fig_dtype_memory(out: Path) -> None:
    """One CT volume, 512 x 512 x 300 voxels, in each float type."""
    fig, ax = plt.subplots(figsize=WIDE)
    voxels = 512 * 512 * 300
    names = ["float64", "float32", "float16", "float8"]
    mb = [voxels * b / 1e6 for b in (8, 4, 2, 1)]
    ax.barh(range(4), mb, color=[GREY, BLUE, PURPLE, GREEN], height=0.55)
    ax.set_yticks(range(4))
    ax.set_yticklabels(names, fontsize=11, family=MONO)
    ax.invert_yaxis()
    ax.set_xlim(0, 760)
    ax.set_xlabel("megabytes", fontsize=10)
    for i, v in enumerate(mb):
        ax.text(v + 8, i, f"{v:.0f} MB", va="center", fontsize=11, color=INK)
    ax.set_title("One CT scan: 512 x 512 x 300 voxels", fontsize=13)
    save(fig, out, "dtype_memory")


# ===================================================== 10. 2d indexing
def _grid(ax, x0, y0, rows, cols, hot, w=0.10, h=0.13, colour=BLUE, fill="#eef3fa"):
    """A rows x cols block of arange values, highlighting the (r, c) pairs in hot."""
    for r in range(rows):
        for c in range(cols):
            on = (r, c) in hot
            _cell(
                ax,
                x0 + c * w,
                y0 - r * h,
                w,
                h,
                str(r * cols + c),
                ec=(colour if on else GREY),
                fc=(fill if on else "white"),
                fs=10.5,
            )


def fig_array_index(out: Path) -> None:
    """y[row, col]: one index per axis, and a slice can stand for either."""
    fig, axes = plt.subplots(1, 4, figsize=WIDE)
    cases = [
        ("y[1, 2]", {(1, 2)}, BLUE, "#eef3fa", "one cell: 6"),
        ("y[1]", {(1, c) for c in range(4)}, PURPLE, "#f3effa", "row 1, shape (4,)"),
        (
            "y[:, 2]",
            {(r, 2) for r in range(3)},
            GREEN,
            "#eafaec",
            "column 2, shape (3,)",
        ),
        (
            "y[:2, :2]",
            {(r, c) for r in range(2) for c in range(2)},
            AMBER,
            "#fdf6e9",
            "top-left block, (2, 2)",
        ),
    ]
    for ax, (expr, hot, colour, fill, what) in zip(axes, cases):
        blank(ax)
        ax.set_title(expr, fontsize=13, family=MONO, color=colour)
        _grid(ax, 0.06, 0.66, 3, 4, hot, w=0.22, h=0.15, colour=colour, fill=fill)
        ax.text(0.5, 0.12, what, ha="center", fontsize=10.5, color=GREY)
    fig.text(
        0.5,
        0.03,
        "y = np.arange(12).reshape(3, 4)",
        ha="center",
        fontsize=11.5,
        family=MONO,
        color=INK,
    )
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    save(fig, out, "array_index")


# ===================================================== 10b. broadcasting
def fig_broadcasting(out: Path) -> None:
    """A smaller array is stretched along the missing axis, without a copy."""
    fig, axes = plt.subplots(1, 2, figsize=WIDE)

    for ax, title, vec, along_rows in (
        (axes[0], "y + [10, 20, 30, 40]", ("10", "20", "30", "40"), True),
        (axes[1], "y + [[100], [200], [300]]", ("100", "200", "300"), False),
    ):
        blank(ax)
        ax.set_title(title, fontsize=12, family=MONO)
        w, h = 0.085, 0.12
        _grid(ax, 0.02, 0.66, 3, 4, set(), w=w, h=h)
        ax.text(0.39, 0.60, "+", fontsize=16, ha="center", va="center")
        x0 = 0.43
        for r in range(3):
            for c in range(4):
                real = (r == 0) if along_rows else (c == 0)
                v = vec[c] if along_rows else vec[r]
                _cell(
                    ax,
                    x0 + c * w,
                    0.66 - r * h,
                    w,
                    h,
                    v,
                    ec=(GREEN if real else FAINT),
                    fc=("#eafaec" if real else "white"),
                    fs=9.5,
                    tc=(INK if real else GREY),
                )
        ax.text(
            0.5,
            0.18,
            "shape (3, 4) + (4,)" if along_rows else "shape (3, 4) + (3, 1)",
            ha="center",
            fontsize=11,
            family=MONO,
            color=INK,
        )
        ax.text(
            0.5,
            0.08,
            "the row is repeated down"
            if along_rows
            else "the column is repeated across",
            ha="center",
            fontsize=10.5,
            color=GREY,
        )

    fig.text(
        0.5,
        0.01,
        "shapes are compared from the right: equal, or 1",
        ha="center",
        fontsize=11.5,
        color=INK,
    )
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    save(fig, out, "broadcasting")


# ===================================================== 11. axis
def fig_axes(out: Path) -> None:
    """axis=0 collapses the rows (one result per column), axis=1 the columns."""
    fig, axes = plt.subplots(1, 2, figsize=WIDE)
    for ax, title, axis in (
        (axes[0], "y.sum(axis=0)", 0),
        (axes[1], "y.sum(axis=1)", 1),
    ):
        blank(ax)
        ax.set_title(
            title, fontsize=13, family=MONO, color=(PURPLE if axis == 0 else AMBER)
        )
        w, h = 0.11, 0.12
        _grid(ax, 0.10, 0.76, 3, 4, set(), w=w, h=h)
        if axis == 0:
            for c in range(4):
                x = 0.10 + c * w + 0.8 * w
                arrow(ax, (x, 0.86), (x, 0.44), color=PURPLE, lw=1.4)
                _cell(
                    ax,
                    0.10 + c * w,
                    0.28,
                    w,
                    h,
                    str(12 + 3 * c),
                    ec=PURPLE,
                    fc="#f3effa",
                    fs=10.5,
                )
            ax.text(
                0.33,
                0.12,
                "one sum per column, shape (4,)",
                ha="center",
                fontsize=10.5,
                color=GREY,
            )
        else:
            for r in range(3):
                y = 0.82 - r * h
                arrow(ax, (0.10, y - 0.03), (0.60, y - 0.03), color=AMBER, lw=1.4)
                _cell(
                    ax,
                    0.66,
                    y - h / 2,
                    w,
                    h,
                    str(6 + 16 * r),
                    ec=AMBER,
                    fc="#fdf6e9",
                    fs=10.5,
                )
            ax.text(
                0.40,
                0.12,
                "one sum per row, shape (3,)",
                ha="center",
                fontsize=10.5,
                color=GREY,
            )
    fig.text(
        0.5,
        0.03,
        "the axis you name is the one that disappears",
        ha="center",
        fontsize=11.5,
        color=INK,
    )
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    save(fig, out, "axes")


# ===================================================== 12. boolean masks
def fig_masks(out: Path) -> None:
    """A comparison gives an array of booleans; indexing with it keeps the Trues."""
    fig, ax = plt.subplots(figsize=WIDE)
    blank(ax)
    bmi = [22.1, 31.4, 18.0, 27.5, 35.2, 24.3]
    w, h, x0 = 0.085, 0.13, 0.30
    rows = [
        ("bmi", [f"{v:g}" for v in bmi], BLUE, None),
        ("bmi >= 30", [str(v >= 30) for v in bmi], GREY, [v >= 30 for v in bmi]),
        ("bmi[bmi >= 30]", ["31.4", "35.2"], RED, None),
    ]
    for i, (label, cells, colour, flags) in enumerate(rows):
        y = 0.76 - i * 0.24
        ax.text(
            x0 - 0.03,
            y + h / 2,
            label,
            ha="right",
            va="center",
            fontsize=12.5,
            family=MONO,
            color=INK,
        )
        for j, v in enumerate(cells):
            on = flags[j] if flags else True
            ec = RED if (flags and on) else colour
            fc = "#fbeaea" if (flags and on) or colour == RED else "white"
            _cell(
                ax,
                x0 + j * w,
                y,
                w,
                h,
                v,
                ec=ec,
                fc=fc,
                fs=10.5,
                tc=(INK if on else GREY),
            )
    ax.text(
        x0 + 6 * w + 0.03,
        0.76 + h / 2,
        "float64",
        fontsize=11,
        family=MONO,
        color=BLUE,
        va="center",
    )
    ax.text(
        x0 + 6 * w + 0.03,
        0.52 + h / 2,
        "bool",
        fontsize=11,
        family=MONO,
        color=GREY,
        va="center",
    )
    ax.text(
        x0 + 2 * w + 0.03,
        0.28 + h / 2,
        "only the True positions",
        fontsize=11,
        color=RED,
        va="center",
    )

    ax.text(
        0.02,
        0.10,
        "(bmi >= 30).sum()  ->  2      (bmi >= 30).mean()  ->  0.33",
        fontsize=12,
        family=MONO,
        color=GREEN,
        ha="left",
    )
    ax.text(
        0.02,
        0.01,
        "True counts as 1: a sum counts, a mean is a fraction",
        fontsize=10.5,
        color=GREY,
        ha="left",
    )
    save(fig, out, "masks")


# ===================================================== 13. the cohort
def fig_bmi_hist(out: Path) -> None:
    """The mini use case of the notebook: BMI of 200 simulated patients."""
    import numpy as np

    rng = np.random.default_rng(42)
    height = rng.normal(1.70, 0.09, 200)
    weight = rng.normal(72, 14, 200)
    bmi = weight / height**2

    fig, ax = plt.subplots(figsize=WIDE)
    ax.hist(bmi, bins=30, color=BLUE, alpha=0.75, edgecolor="white")
    for x, colour in ((18.5, AMBER), (25, AMBER), (30, RED)):
        ax.axvline(x, color=colour, lw=1.6, ls="--")
    ax.set_xlabel("BMI (kg/m²)")
    ax.set_ylabel("patients")
    counts = np.bincount(np.digitize(bmi, [18.5, 25, 30]), minlength=4)
    top = ax.get_ylim()[1] * 1.3
    ax.set_ylim(0, top)
    for x, name, n in (
        (14.5, "under", counts[0]),
        (21.7, "normal", counts[1]),
        (27.5, "over", counts[2]),
        (35, "obese", counts[3]),
    ):
        ax.text(
            x,
            top * 0.93,
            f"{name}\n{n}",
            ha="center",
            va="top",
            fontsize=10.5,
            color=INK,
        )
    save(fig, out, "bmi_hist")


FIGURES = (
    fig_names,
    fig_type_map,
    fig_numbers,
    fig_truthy,
    fig_string_index,
    fig_conversions,
    fig_containers,
    fig_aliasing,
    fig_dict_record,
    fig_sets,
    fig_nested,
    fig_list_vs_array,
    fig_ndarray,
    fig_float_bits,
    fig_float_precision,
    fig_dtype_memory,
    fig_array_index,
    fig_broadcasting,
    fig_axes,
    fig_masks,
    fig_bmi_hist,
)


def main() -> None:
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "Programming01/Session01/img")
    out.mkdir(parents=True, exist_ok=True)
    for fn in FIGURES:
        fn(out)
        print(f"{out / (fn.__name__.removeprefix('fig_') + '.png')}")


if __name__ == "__main__":
    main()
