#!/usr/bin/env python3
"""Shared drawing helpers for the slide illustrations of every session.

The decks are built with pandoc, which cannot express a diagram, so every
illustration ships as a figure rendered here: one palette, one slide aspect, and
a handful of primitives (a rounded box, an arrow, a mock terminal window) that
the per-session `make_figures_*.py` scripts compose.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

INK = "#1b1b1b"
GREY = "#9aa0a6"
BLUE = "#2b6cb0"
RED = "#c53030"
GREEN = "#00ab0e"
AMBER = "#b7791f"
PURPLE = "#6b46c1"
FAINT = "#e8eaed"
MONO = "DejaVu Sans Mono"

plt.rcParams.update(
    {
        "figure.dpi": 160,
        "savefig.dpi": 300,
        "font.size": 12,
        "axes.titlesize": 13,
        "axes.labelsize": 11,
        "axes.edgecolor": GREY,
        "axes.labelcolor": INK,
        "text.color": INK,
        "xtick.color": INK,
        "ytick.color": INK,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "figure.facecolor": "white",
        "savefig.bbox": "tight",
        # this deck has no equations, but plenty of "$" prompts and "$f" variables
        "text.parse_math": False,
    }
)

# the .pptx content placeholder is 9.00in x 3.71in; pad every saved figure up to
# that aspect so pandoc does not shrink it and leave the slide two-thirds empty
SLIDE_ASPECT = 9.00 / 3.71
WIDE = (12.6, 12.6 / SLIDE_ASPECT)


def pad_to_aspect(path: Path, aspect: float = SLIDE_ASPECT) -> None:
    """Pad a saved figure with white so it exactly fills the slide placeholder."""
    from PIL import Image

    im = Image.open(path).convert("RGB")
    w, h = im.size
    if w / h < aspect:
        tw, th = int(round(h * aspect)), h
    else:
        tw, th = w, int(round(w / aspect))
    if (tw, th) == (w, h):
        return
    canvas = Image.new("RGB", (tw, th), "white")
    canvas.paste(im, ((tw - w) // 2, (th - h) // 2))
    canvas.save(path)


def save(fig, out: Path, name: str) -> None:
    path = out / f"{name}.png"
    fig.savefig(path)
    plt.close(fig)
    pad_to_aspect(path)


def blank(ax, xlim=(0, 1), ylim=(0, 1)):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)


def box(ax, xy, w, h, text, fc="white", ec=BLUE, fs=11, lw=1.8, tc=INK, mono=False):
    """A rounded label box, used by the flow diagrams."""
    ax.add_patch(
        FancyBboxPatch(
            (xy[0] - w / 2, xy[1] - h / 2),
            w,
            h,
            boxstyle="round,pad=0.012,rounding_size=0.02",
            facecolor=fc,
            edgecolor=ec,
            linewidth=lw,
        )
    )
    ax.text(
        xy[0], xy[1], text, ha="center", va="center", fontsize=fs, color=tc,
        family=(MONO if mono else None),
    )


def arrow(ax, a, b, color=GREY, lw=1.8, style="-|>", ls="-"):
    ax.add_patch(
        FancyArrowPatch(
            a, b, arrowstyle=style, mutation_scale=14, color=color, lw=lw,
            linestyle=ls, shrinkA=2, shrinkB=2,
        )
    )


def terminal(ax, xy, w, h, lines, title="Terminal", ec=INK):
    """A little mock terminal window: dark title bar, monospace body."""
    x, y = xy[0] - w / 2, xy[1] - h / 2
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.004,rounding_size=0.015",
                                facecolor="#fbfbfb", edgecolor=ec, linewidth=1.6))
    ax.add_patch(FancyBboxPatch((x, y + h - 0.075), w, 0.075,
                                boxstyle="square,pad=0",
                                facecolor="#33373d", edgecolor="none"))
    ax.text(x + 0.018, y + h - 0.037, title, ha="left", va="center",
            fontsize=9, color="white")
    for i, (txt, colour) in enumerate(lines):
        ax.text(x + 0.018, y + h - 0.135 - i * 0.058, txt, ha="left", va="center",
                fontsize=10.5, family=MONO, color=colour)

