#!/usr/bin/env python3
"""Render the illustration figures used by the Programming01 Session02 slides.

Session02 is the control flow and object part of the language: conditions, loops,
functions and classes. Same contract as the other decks: every figure is synthetic,
seeded and self-contained, so `make figures` reproduces the same output anywhere.

Usage: make_figures_c02.py [outdir]   (default: Programming01/Session02/img)
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
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


# ===================================================== 1. the elif ladder
def fig_branching(out: Path) -> None:
    """if / elif / else: the first true test wins, and the order is the logic."""
    fig, axes = plt.subplots(1, 2, figsize=WIDE)

    tests = [("sbp < 90", '"low"'), ("sbp < 120", '"normal"'),
             ("sbp < 130", '"elevated"'), ("else", '"high"')]
    for ax, order, title, colour in ((axes[0], [0, 1, 2, 3], "the tests in order", GREEN),
                                     (axes[1], [2, 1, 0, 3], "one test moved up", RED)):
        blank(ax)
        ax.set_title(title, fontsize=13, color=colour)
        y = 0.86
        for k, i in enumerate(order):
            test, result = tests[i]
            kw = {"ec": GREY, "fc": "white"} if test == "else" else {"ec": BLUE}
            box(ax, (0.30, y), 0.42, 0.14, test, fs=12, mono=True, **kw)
            arrow(ax, (0.52, y), (0.68, y), color=GREEN)
            ax.text(0.72, y, result, fontsize=12, family=MONO, color=INK, va="center")
            ax.text(0.545, y + 0.045, "True", fontsize=8.5, color=GREEN)
            if k < 3:
                arrow(ax, (0.30, y - 0.07), (0.30, y - 0.14), color=GREY)
                ax.text(0.325, y - 0.105, "False", fontsize=8.5, color=GREY)
            y -= 0.21
        verdict = ("sbp = 125  ->  \"elevated\"" if colour is GREEN
                   else "sbp = 125  ->  \"elevated\"   but sbp = 100  ->  \"elevated\" too")
        ax.text(0.5, 0.06, verdict, ha="center", fontsize=11, family=MONO, color=colour)

    fig.text(0.5, 0.015, "Python stops at the first test that is True: a wider test "
             "placed first hides every test below it",
             ha="center", fontsize=12, color=INK)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    save(fig, out, "branching")


# ===================================================== 2. combining conditions
def fig_boolean(out: Path) -> None:
    """and / or / not on a real inclusion criterion."""
    fig, axes = plt.subplots(1, 2, figsize=WIDE, gridspec_kw={"width_ratios": [1, 1.1]})

    ax = axes[0]
    blank(ax)
    ax.set_title("age > 65 and (smoker or diabetic)", fontsize=13, family=MONO)
    box(ax, (0.26, 0.76), 0.34, 0.15, "age > 65", ec=BLUE, mono=True, fs=12)
    box(ax, (0.26, 0.52), 0.34, 0.15, "smoker", ec=PURPLE, mono=True, fs=12)
    box(ax, (0.26, 0.32), 0.34, 0.15, "diabetic", ec=PURPLE, mono=True, fs=12)
    box(ax, (0.60, 0.42), 0.16, 0.13, "or", ec=PURPLE, fs=12, mono=True)
    box(ax, (0.83, 0.59), 0.16, 0.13, "and", ec=GREEN, fs=12, mono=True)
    arrow(ax, (0.43, 0.52), (0.52, 0.45), color=PURPLE)
    arrow(ax, (0.43, 0.32), (0.52, 0.39), color=PURPLE)
    arrow(ax, (0.68, 0.42), (0.77, 0.54), color=PURPLE)
    arrow(ax, (0.43, 0.76), (0.77, 0.64), color=BLUE)
    ax.text(0.83, 0.47, "at risk", ha="center", fontsize=11.5, color=GREEN)
    ax.text(0.5, 0.12, "the brackets are the clinical definition: without them,\n"
            "`and` binds tighter than `or` and the rule changes",
            ha="center", fontsize=10.5, color=RED)

    ax = axes[1]
    blank(ax)
    ax.set_title("the three operators", fontsize=13)
    rows = [("A", "B", "A and B", "A or B"),
            ("True", "True", "True", "True"),
            ("True", "False", "False", "True"),
            ("False", "True", "False", "True"),
            ("False", "False", "False", "False")]
    xs = (0.12, 0.30, 0.55, 0.82)
    for r, row in enumerate(rows):
        y = 0.82 - r * 0.125
        for x, cell in zip(xs, row):
            colour = INK if r == 0 else (GREEN if cell == "True" else GREY)
            ax.text(x, y, cell, ha="center", va="center", fontsize=11.5, family=MONO,
                    color=colour)
        if r == 0:
            ax.plot([0.04, 0.95], [y - 0.055, y - 0.055], color=GREY, lw=1)
    ax.text(0.5, 0.10, "not True  ->  False        `and` needs both, `or` needs one",
            ha="center", fontsize=11, family=MONO, color=INK)
    ax.text(0.5, 0.02, "Python is lazy: in `a and b`, b is not even evaluated when a "
            "is False", ha="center", fontsize=10.5, color=AMBER)
    fig.tight_layout()
    save(fig, out, "boolean")


# ===================================================== 3. anatomy of a for loop
def fig_for_anatomy(out: Path) -> None:
    """The body runs once per item, with the name bound to the current item."""
    fig, ax = plt.subplots(figsize=WIDE)
    blank(ax)
    fig.canvas.draw()
    r = fig.canvas.get_renderer()

    def underline(x, y, before, part, colour, label, ly):
        """Underline `part` of a code line, measuring the rendered width."""
        h = ax.text(x, y, before, fontsize=18, family=MONO, alpha=0)
        bb = h.get_window_extent(r).transformed(ax.transAxes.inverted())
        x0 = bb.x1
        h2 = ax.text(x, y, before + part, fontsize=18, family=MONO, alpha=0)
        x1 = h2.get_window_extent(r).transformed(ax.transAxes.inverted()).x1
        ax.plot([x0, x1], [y - 0.045, y - 0.045], color=colour, lw=2.5)
        ax.text((x0 + x1) / 2, ly, label, ha="center", fontsize=10.5, color=colour)

    ax.text(0.04, 0.88, "for hr in heart_rates:", fontsize=18, family=MONO, color=INK)
    ax.text(0.04, 0.60, "    print(hr)", fontsize=18, family=MONO, color=INK)
    underline(0.04, 0.88, "for ", "hr", PURPLE, "the name", 0.78)
    underline(0.04, 0.88, "for hr in ", "heart_rates", BLUE, "the iterable", 0.78)
    underline(0.04, 0.60, "    ", "print(hr)", GREEN, "the body, indented", 0.50)

    values = [72, 85, 64, 90, 78]
    for i, v in enumerate(values):
        x = 0.46 + i * 0.105
        box(ax, (x, 0.74), 0.085, 0.16, str(v), ec=BLUE, mono=True, fs=13)
        arrow(ax, (x, 0.64), (x, 0.52), color=GREY)
        box(ax, (x, 0.42), 0.095, 0.17, f"hr = {v}\nprint", ec=PURPLE, mono=True, fs=10)
    ax.text(0.715, 0.90, "heart_rates", ha="center", fontsize=12, family=MONO,
            color=BLUE)
    ax.text(0.715, 0.26, "the body runs 5 times, once per item",
            ha="center", fontsize=11.5, color=PURPLE)

    ax.text(0.04, 0.12, "No counter, no index, no length: a for loop walks the items "
            "themselves.", fontsize=12.5, color=INK)
    ax.text(0.04, 0.03, "The indentation is the loop: what is indented runs every "
            "time, what is not runs once, at the end.",
            fontsize=11.5, color=GREY)
    save(fig, out, "for_anatomy")


# ===================================================== 4. range, enumerate, zip, items
PANELS = {
    "counted": ("the counted loop", BLUE,
                ["# no list: range generates the numbers"],
                "for i in range(0, 10, 2):",
                ["0", "2", "4", "6", "8"]),
    "enumerate": ("position and value", PURPLE,
                  ["hrs = [72, 85, 64]"],
                  "for i, hr in enumerate(hrs):",
                  ["(0, 72)", "(1, 85)", "(2, 64)"]),
    "zip": ("two lists in step", GREEN,
            ['ids   = ["P1", "P2", "P3"]', "temps = [36.8, 38.9, 37.2]"],
            "for id, t in zip(ids, temps):",
            ['("P1", 36.8)', '("P2", 38.9)', '("P3", 37.2)']),
    "items": ("key and value", AMBER,
              ['doses = {"aspirin": 100, "insulin": 10,', '         "metformin": 500}'],
              "for drug, mg in doses.items():",
              ['("aspirin", 100)', '("insulin", 10)', '("metformin", 500)']),
}


def _loop_helpers(out: Path, keys, name: str) -> None:
    """Two ways to feed a for loop, side by side: source, call, items produced."""
    fig, axes = plt.subplots(1, len(keys), figsize=WIDE)
    for ax, key in zip(axes, keys):
        what, colour, source, call, items = PANELS[key]
        blank(ax)
        ax.set_title(what, fontsize=20, color=colour)
        for i, line in enumerate(source):
            ax.text(0.5, 0.94 - i * 0.085, line, ha="center", fontsize=14.5,
                    family=MONO, color=GREY)
        ax.text(0.5, 0.74, call, ha="center", fontsize=16, family=MONO, color=colour)
        # the stack of produced items, spread over the room below the call
        pitch = 0.58 / len(items)
        for i, item in enumerate(items):
            box(ax, (0.5, 0.60 - i * pitch), 0.86, pitch * 0.8, item, ec=colour,
                mono=True, fs=16)
    fig.text(0.5, 0.03, "loops alway get one item per turn", ha="center", fontsize=15, color=INK)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    save(fig, out, name)


def fig_loop_helpers_a(out: Path) -> None:
    """range and enumerate."""
    _loop_helpers(out, ("counted", "enumerate"), "loop_helpers_a")


def fig_loop_helpers_b(out: Path) -> None:
    """zip and .items()."""
    _loop_helpers(out, ("zip", "items"), "loop_helpers_b")


# ===================================================== 5. while
def fig_while_loop(out: Path) -> None:
    """A for loop knows how many turns; a while loop asks a question each turn."""
    fig, axes = plt.subplots(1, 2, figsize=WIDE, gridspec_kw={"width_ratios": [1, 1.2]})

    ax = axes[0]
    blank(ax)
    ax.set_title("while: repeat until the condition fails", fontsize=13)
    box(ax, (0.52, 0.82), 0.44, 0.14, "c = 100, t = 0", ec=GREY, mono=True, fs=11.5)
    box(ax, (0.52, 0.58), 0.44, 0.15, "c >= 5 ?", ec=BLUE, mono=True, fs=12)
    box(ax, (0.52, 0.32), 0.44, 0.16, "c = c / 2\nt = t + 6", ec=PURPLE, mono=True,
        fs=11.5)
    arrow(ax, (0.52, 0.75), (0.52, 0.66), color=GREY)
    arrow(ax, (0.52, 0.50), (0.52, 0.41), color=GREEN)
    ax.text(0.55, 0.455, "True", fontsize=9.5, color=GREEN)
    # back to the test, around the left of the boxes
    ax.plot([0.30, 0.16, 0.16], [0.32, 0.32, 0.58], color=PURPLE, lw=1.8)
    arrow(ax, (0.16, 0.58), (0.29, 0.58), color=PURPLE)
    ax.text(0.17, 0.46, "and test again", fontsize=9.5, color=PURPLE)
    arrow(ax, (0.74, 0.58), (0.88, 0.58), color=GREY)
    ax.text(0.76, 0.63, "False", fontsize=9.5, color=GREY)
    ax.text(0.90, 0.58, "done", fontsize=10.5, color=GREY, ha="left", va="center")
    ax.text(0.5, 0.12, "forget to change `c` in the body and the loop never ends",
            ha="center", fontsize=10.5, color=RED)

    ax = axes[1]
    t = np.arange(0, 42, 6)
    c = 100 * 0.5 ** (t / 6)
    ax.step(t, c, where="post", color=PURPLE, lw=1.8)
    ax.plot(t, c, "o", color=PURPLE, ms=6)
    ax.axhline(5, color=RED, ls="--", lw=1.2)
    ax.text(41, 6.5, "5 mg/L", ha="right", fontsize=10, color=RED)
    stop = t[c < 5][0]
    ax.axvline(stop, color=GREEN, ls=":", lw=1.4)
    ax.text(stop + 0.8, 70, f"the loop stops\nafter {stop} h", fontsize=11, color=GREEN)
    ax.set_xlabel("time (h)")
    ax.set_ylabel("concentration (mg/L)")
    ax.set_title("half-life 6 h: how many hours below 5 mg/L?", fontsize=12)
    fig.tight_layout()
    save(fig, out, "while_loop")


# ===================================================== 6. break and continue
def fig_break_continue(out: Path) -> None:
    """Two ways out of a turn: leave the loop, or skip to the next item."""
    fig, axes = plt.subplots(2, 1, figsize=WIDE)

    glucose = [5.1, 5.8, 6.3, 12.4, 5.5, 4.9]
    ax = axes[0]
    blank(ax)
    ax.set_title("break: leave the loop at the first value above 11", fontsize=12.5,
                 color=RED)
    for i, v in enumerate(glucose):
        x = 0.10 + i * 0.14
        hit = v > 11
        box(ax, (x, 0.58), 0.095, 0.38, str(v), ec=RED if hit else BLUE, mono=True,
            fs=12, fc=FAINT if i > 3 else "white",
            tc=GREY if i > 3 else INK)
        if i < 3:
            arrow(ax, (x + 0.050, 0.58), (x + 0.088, 0.58), color=GREEN)
    ax.text(0.52, 0.12, "found it: stop here", fontsize=11, color=RED, ha="center")
    ax.text(0.80, 0.12, "never looked at", fontsize=11, color=GREY, ha="center")

    values = [72, None, 85, None, 64]
    ax = axes[1]
    blank(ax)
    ax.set_title("continue: skip this item, go on with the next", fontsize=12.5,
                 color=AMBER)
    for i, v in enumerate(values):
        x = 0.10 + i * 0.14
        skip = v is None
        box(ax, (x, 0.58), 0.095, 0.38, str(v), ec=AMBER if skip else BLUE, mono=True,
            fs=12, tc=GREY if skip else INK)
        ax.text(x, 0.16, "skipped" if skip else "counted", ha="center", fontsize=10,
                color=AMBER if skip else GREEN)
        if i < 4:
            arrow(ax, (x + 0.050, 0.58), (x + 0.088, 0.58), color=GREY)
    fig.tight_layout()
    save(fig, out, "break_continue")


# ===================================================== 7. comprehensions
def fig_comprehension(out: Path) -> None:
    """The same loop, written as one expression."""
    fig, ax = plt.subplots(figsize=WIDE)
    blank(ax)

    ax.text(0.03, 0.86, "fevers = []", fontsize=14, family=MONO, color=GREY)
    ax.text(0.03, 0.74, "for t in temps:", fontsize=14, family=MONO, color=BLUE)
    ax.text(0.06, 0.62, "if t >= 38:", fontsize=14, family=MONO, color=PURPLE)
    ax.text(0.09, 0.50, "fevers.append(t)", fontsize=14, family=MONO, color=GREEN)

    arrow(ax, (0.36, 0.66), (0.46, 0.66), color=GREY)

    ax.text(0.50, 0.74, "fevers = [", fontsize=14, family=MONO, color=GREY)
    ax.text(0.62, 0.74, "t", fontsize=14, family=MONO, color=GREEN)
    ax.text(0.53, 0.62, "for t in temps", fontsize=14, family=MONO, color=BLUE)
    ax.text(0.53, 0.50, "if t >= 38]", fontsize=14, family=MONO, color=PURPLE)

    for y, colour, label in ((0.74, GREEN, "what to keep"),
                             (0.62, BLUE, "where it comes from"),
                             (0.50, PURPLE, "which ones (optional)")):
        ax.text(0.76, y, label, fontsize=11, color=colour, va="baseline")

    ax.text(0.03, 0.28, "Same three pieces, same order, one line: build a new list "
            "from an old one.", fontsize=12.5, color=INK)
    ax.text(0.03, 0.17, "Use it when the loop only builds a list. A loop that prints, "
            "counts or calls an API stays a loop.",
            fontsize=11.5, color=GREY)
    ax.text(0.03, 0.06, "[bmi(w, h) for w, h in zip(weights, heights)]          "
            "{id: t for id, t in zip(ids, temps)}",
            fontsize=11.5, family=MONO, color=AMBER)
    save(fig, out, "comprehension")


# ===================================================== 8. functions
def fig_function_anatomy(out: Path) -> None:
    """def, parameters, return, and the call that uses them."""
    fig, ax = plt.subplots(figsize=WIDE)
    blank(ax)

    fig.canvas.draw()
    r = fig.canvas.get_renderer()

    def underline(x, y, before, part, colour, label, ly):
        h = ax.text(x, y, before, fontsize=17, family=MONO, alpha=0)
        x0 = h.get_window_extent(r).transformed(ax.transAxes.inverted()).x1
        h2 = ax.text(x, y, before + part, fontsize=17, family=MONO, alpha=0)
        x1 = h2.get_window_extent(r).transformed(ax.transAxes.inverted()).x1
        ax.plot([x0, x1], [y - 0.045, y - 0.045], color=colour, lw=2.5)
        ax.text((x0 + x1) / 2, ly, label, ha="center", fontsize=10.5, color=colour)

    ax.text(0.04, 0.88, "def bmi(weight, height):", fontsize=17, family=MONO,
            color=INK)
    ax.text(0.04, 0.62, "    return weight / height ** 2", fontsize=17, family=MONO,
            color=INK)
    underline(0.04, 0.88, "def ", "bmi", BLUE, "the name you call", 0.78)
    underline(0.04, 0.88, "def bmi(", "weight, height", PURPLE, "parameters", 0.78)
    underline(0.04, 0.62, "    ", "return", GREEN, "what comes back", 0.52)

    box(ax, (0.70, 0.78), 0.28, 0.14, "bmi(70, 1.75)", ec=BLUE, mono=True, fs=13)
    arrow(ax, (0.70, 0.70), (0.70, 0.60), color=PURPLE)
    ax.text(0.715, 0.655, "arguments go in", fontsize=10, color=PURPLE)
    box(ax, (0.70, 0.52), 0.28, 0.14, "22.86", ec=GREEN, mono=True, fs=13)
    ax.text(0.86, 0.52, "the value comes back", fontsize=10.5, color=GREEN, va="center")

    ax.text(0.04, 0.40, "def mean(values, skip_none=True):", fontsize=15, family=MONO,
            color=INK)
    ax.text(0.04, 0.31, "default argument: callers may omit it", fontsize=11,
            color=AMBER)
    ax.text(0.04, 0.11, "No `return` means the function returns `None`",
            fontsize=11.5, color=RED)
    # ax.text(0.04, 0.02, "Names created inside stay inside (local); the function only "
    #         "talks to the outside through arguments and the return value.",
    #         fontsize=11.5, color=GREY)
    save(fig, out, "function_anatomy")


# ===================================================== 9. class = blueprint
def fig_class_anatomy(out: Path) -> None:
    """One class, many independent objects, each with its own attributes."""
    fig, axes = plt.subplots(1, 2, figsize=WIDE, gridspec_kw={"width_ratios": [1.1, 1]})

    ax = axes[0]
    blank(ax)
    ax.set_title("class: a blueprint", fontsize=13, color=BLUE)
    ax.add_patch(FancyBboxPatch((0.06, 0.12), 0.88, 0.74,
                                boxstyle="round,pad=0.012,rounding_size=0.02",
                                facecolor="white", edgecolor=BLUE, linewidth=1.8))
    lines = [("class Patient:", INK),
             ("    def __init__(self, id, age, ...):", PURPLE),
             ("        self.id = id        # attributes", GREY),
             ("        self.heart_rates = []", GREY),
             ("    def bmi(self):          # a method", GREEN),
             ("        return self.weight / self.height ** 2", GREY),
             ("    def __repr__(self):     # how it prints", AMBER),
             ("        return f\"Patient {self.id}\"", AMBER)]
    for i, (txt, colour) in enumerate(lines):
        ax.text(0.09, 0.82 - i * 0.095, txt, fontsize=11.5, family=MONO, color=colour)
    ax.text(0.5, 0.04, "`self` is the object the method was called on",
            ha="center", fontsize=11, color=PURPLE)

    ax = axes[1]
    blank(ax)
    ax.set_title("objects: instances of the blueprint", fontsize=13, color=GREEN)
    for i, (name, vals, colour) in enumerate((
            ("p", 'id   "P001"\nage  54\nweight 81.5', GREEN),
            ("q", 'id   "P002"\nage  37\nweight 62.0', PURPLE))):
        x = 0.28 + i * 0.44
        box(ax, (x, 0.52), 0.36, 0.42, vals, ec=colour, mono=True, fs=11)
        ax.text(x, 0.80, name, ha="center", fontsize=13, family=MONO, color=colour)
        arrow(ax, (x, 0.30), (x, 0.22), color=colour)
        ax.text(x, 0.16, f"{name}.bmi()", ha="center", fontsize=11.5, family=MONO,
                color=colour)
    ax.text(0.5, 0.04, "changing q.weight leaves p untouched: separate objects, "
            "separate data", ha="center", fontsize=11, color=INK)
    fig.tight_layout()
    save(fig, out, "class_anatomy")


# ===================================================== 10. inheritance
def fig_inheritance(out: Path) -> None:
    """Inpatient is a Patient with a room: everything else is inherited."""
    fig, ax = plt.subplots(figsize=WIDE)
    blank(ax)

    box(ax, (0.30, 0.74), 0.34, 0.30,
        "Patient\n\nid, age, weight, height\nbmi()   add_heart_rate()", ec=BLUE, fs=11.5)
    box(ax, (0.30, 0.30), 0.34, 0.30,
        "InPatient(Patient)\n\n+ room\nsuper().__init__(...)", ec=GREEN, fs=11.5)
    arrow(ax, (0.30, 0.45), (0.30, 0.59), color=GREEN)
    ax.text(0.33, 0.51, "inherits everything above", fontsize=10.5, color=GREEN)

    lines = [("i = InPatient(\"P003\", 71, 95.2, 1.70, room=12)", INK),
             ("i.bmi()                  # 32.9   defined on Patient", GREY),
             ("i.room                   # 12     defined on InPatient", GREY),
             ("isinstance(i, Patient)   # True   an InPatient is a Patient", GREEN),
             ("isinstance(p, InPatient) # False  the reverse is not true", RED)]
    for i, (txt, colour) in enumerate(lines):
        ax.text(0.54, 0.84 - i * 0.11, txt, fontsize=10.5, family=MONO, color=colour)

    ax.text(0.5, 0.06, "Write the shared part once, add only what differs: a ward has "
            "inpatients, outpatients, and the same bmi().",
            ha="center", fontsize=12, color=INK)
    save(fig, out, "inheritance")


# ===================================================== 11. the mini use case
def fig_ward_model(out: Path) -> None:
    """Composition: a Ward holds Patients, each holding its own measurements."""
    fig, ax = plt.subplots(figsize=WIDE)
    blank(ax)

    ax.add_patch(FancyBboxPatch((0.04, 0.22), 0.92, 0.60,
                                boxstyle="round,pad=0.012,rounding_size=0.02",
                                facecolor="white", edgecolor=AMBER, linewidth=2))
    ax.text(0.07, 0.75, "Ward(\"Cardiology\", capacity=3)", fontsize=13, family=MONO,
            color=AMBER)
    ax.text(0.07, 0.67, "patients = [ ... ]      admit()     __len__()     alerts()",
            fontsize=11, family=MONO, color=GREY)

    people = [("P001", "HR 73.7", GREEN), ("P002", "HR 111.0", RED),
              ("P003", "no HR", RED)]
    for i, (pid, hr, colour) in enumerate(people):
        x = 0.19 + i * 0.21
        box(ax, (x, 0.42), 0.19, 0.26, f"Patient\n{pid}\n{hr}", ec=colour, fs=11)
    box(ax, (0.84, 0.42), 0.18, 0.26, "P004\nrefused:\nward full", ec=GREY, fs=11,
        fc=FAINT, tc=GREY)

    ax.text(0.5, 0.12, "alerts()  ->  [\"P002\", \"P003\"]      len(ward)  ->  3",
            ha="center", fontsize=13, family=MONO, color=INK)
    ax.text(0.5, 0.04, "Objects inside objects: the code now reads like the ward round.",
            ha="center", fontsize=12, color=INK)
    save(fig, out, "ward_model")


FIGURES = (
    fig_branching,
    fig_boolean,
    fig_for_anatomy,
    fig_loop_helpers_a,
    fig_loop_helpers_b,
    fig_while_loop,
    fig_break_continue,
    fig_comprehension,
    fig_function_anatomy,
    fig_class_anatomy,
    fig_inheritance,
    fig_ward_model,
)


def main() -> None:
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "Programming01/Session02/img")
    out.mkdir(parents=True, exist_ok=True)
    for fn in FIGURES:
        fn(out)
        print(f"{out / (fn.__name__.removeprefix('fig_') + '.png')}")


if __name__ == "__main__":
    main()
