#!/usr/bin/env python3
"""Render the illustration figures used by the Programming01 Session03 slides.

Session03 is matplotlib: why we plot, the anatomy of a figure, the figure/axes model,
one plot type per question (line, scatter, histogram, bar, box, image), colour maps,
and what makes a figure readable. Every figure is synthetic and seeded, so
`make figures` reproduces the same output anywhere.

Usage: make_figures_c03.py [outdir]   (default: Programming01/Session03/img)
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


def _vitals(seed: int = 3):
    """48 hours of hourly temperature and heart rate for one febrile patient."""
    rng = np.random.default_rng(seed)
    t = np.arange(48)
    fever = 1.6 * np.exp(-((t - 20) / 7.0) ** 2)
    temp = 36.9 + fever + rng.normal(0, 0.12, t.size)
    hr = 74 + 14 * fever + rng.normal(0, 3, t.size)
    return t, temp, hr


def _cohort(n: int = 200, seed: int = 42):
    """Heights (m), weights (kg) and sexes, as in the numpy notebook."""
    rng = np.random.default_rng(seed)
    sex = rng.integers(0, 2, n)  # 0 = F, 1 = M
    height = rng.normal(1.63, 0.07, n) + 0.13 * sex
    weight = 22 * height ** 2 + rng.normal(0, 9, n) + 4 * sex
    return height, weight, sex


# ===================================================== 1. look before you compute
def fig_anscombe(out: Path) -> None:
    """Anscombe's quartet: four datasets, same statistics, different stories."""
    x = np.array([10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5], float)
    ys = [
        [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68],
        [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74],
        [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73],
        [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89],
    ]
    xs = [x, x, x, np.array([8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8], float)]

    fig, axes = plt.subplots(1, 4, figsize=WIDE, sharey=True)
    for i, (ax, xx, yy) in enumerate(zip(axes, xs, ys)):
        yy = np.array(yy)
        ax.scatter(xx, yy, color=BLUE, s=28, zorder=3)
        slope, intercept = np.polyfit(xx, yy, 1)
        grid = np.array([3, 20])
        ax.plot(grid, slope * grid + intercept, color=RED, lw=1.4)
        ax.set_xlim(2, 21)
        ax.set_ylim(2, 14)
        ax.set_title(f"dataset {i + 1}", fontsize=12)
        ax.text(0.04, 0.96, f"mean y {yy.mean():.2f}\nvar y  {yy.var(ddof=1):.2f}\n"
                f"r      {np.corrcoef(xx, yy)[0, 1]:.2f}", transform=ax.transAxes,
                fontsize=9.5, family=MONO, va="top", color=GREY)
    fig.text(0.5, 0.02, "Same mean, variance, correlation and fitted line: only the "
             "plot tells them apart", ha="center", fontsize=11.5, color=INK)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    save(fig, out, "anscombe")


# ===================================================== 2. anatomy
def fig_anatomy(out: Path) -> None:
    """A real plot, with every part named the way matplotlib names it."""
    t, temp, _ = _vitals()
    fig = plt.figure(figsize=WIDE)
    ax = fig.add_axes((0.08, 0.14, 0.52, 0.72))
    ax.plot(t, temp, color=RED, lw=1.8, marker="o", ms=3, label="temperature")
    ax.axhline(38, color=GREY, lw=1.2, ls="--", label="fever threshold")
    ax.set_xlabel("time since admission (h)")
    ax.set_ylabel("temperature (°C)")
    ax.set_title("Patient P0001")
    ax.legend(loc="upper right", fontsize=9)

    # (name, call, what it points at, in axes fraction or data coordinates, label y)
    notes = [
        ("title", "ax.set_title", (0.62, 1.03), "axes fraction", 0.86, INK),
        ("legend", "ax.legend", (0.97, 0.90), "axes fraction", 0.75, INK),
        ("Axes", "one plot area: ax", (1.0, 0.62), "axes fraction", 0.62, BLUE),
        ("line", "ax.plot", (27, 37.45), "data", 0.50, RED),
        ("ticks", "ax.set_xticks", (40, 36.45), "data", 0.34, GREY),
        ("axis labels", "ax.set_xlabel", (0.78, -0.11), "axes fraction", 0.20, INK),
    ]
    for name, call, xy, coords, ty, colour in notes:
        fig.text(0.66, ty, name, fontsize=12, color=colour, va="center")
        ax.annotate("", xy=xy, xycoords=coords, xytext=(0.655, ty),
                    textcoords="figure fraction", annotation_clip=False,
                    arrowprops={"arrowstyle": "-", "color": GREY, "lw": 1.0,
                                "shrinkA": 4, "shrinkB": 2})
        fig.text(0.79, ty, call, fontsize=10.5, family=MONO, color=GREY, va="center")
    fig.text(0.66, 0.95, "Figure", fontsize=12, color=INK, va="center")
    fig.text(0.79, 0.95, "the whole canvas: fig", fontsize=10.5, family=MONO,
             color=GREY, va="center")
    fig.patches.append(FancyBboxPatch((0.005, 0.005), 0.99, 0.99,
                                      boxstyle="square,pad=0", fill=False,
                                      edgecolor=GREY, lw=1.2, ls="--",
                                      transform=fig.transFigure, figure=fig))
    save(fig, out, "anatomy")


# ===================================================== 3. figure and axes
def fig_subplots_grid(out: Path) -> None:
    """plt.subplots(2, 3): one Figure, an array of Axes indexed like numpy."""
    fig, axes = plt.subplots(1, 2, figsize=WIDE, gridspec_kw={"width_ratios": [1.2, 1]})

    ax = axes[0]
    blank(ax)
    ax.set_title("fig, axes = plt.subplots(2, 3)", fontsize=12, family=MONO)
    ax.add_patch(FancyBboxPatch((0.02, 0.06), 0.96, 0.82,
                                boxstyle="round,pad=0.005,rounding_size=0.02",
                                facecolor="white", edgecolor=GREY, lw=1.4, ls="--"))
    ax.text(0.04, 0.84, "fig", fontsize=11, family=MONO, color=GREY)
    for r in range(2):
        for c in range(3):
            hot = (r, c) == (1, 2)
            box(ax, (0.19 + c * 0.31, 0.62 - r * 0.36), 0.26, 0.28,
                f"axes[{r}, {c}]", ec=(RED if hot else BLUE),
                fc=("#fbeaea" if hot else "white"), fs=11, mono=True)

    ax = axes[1]
    blank(ax)
    ax.set_title("Each Axes is drawn on separately", fontsize=12)
    lines = [("axes[0, 0].plot(t, temp)", INK),
             ("axes[1, 2].hist(bmi)", RED),
             ("axes[1, 2].set_title(\"BMI\")", RED),
             ("", INK),
             ("for ax in axes.flat:", INK),
             ("    ax.grid(alpha=0.3)", INK),
             ("", INK),
             ("fig.suptitle(\"Ward report\")", GREY),
             ("fig.tight_layout()", GREY)]
    for i, (line, colour) in enumerate(lines):
        ax.text(0.02, 0.86 - i * 0.095, line, fontsize=11, family=MONO, color=colour,
                ha="left", va="center")
    fig.tight_layout()
    save(fig, out, "subplots_grid")


# ===================================================== 4. which plot
def fig_plot_types(out: Path) -> None:
    """Six questions, six plot types, all on synthetic ward data."""
    rng = np.random.default_rng(0)
    t, temp, _ = _vitals()
    height, weight, sex = _cohort()
    bmi = weight / height ** 2

    fig, axes = plt.subplots(2, 3, figsize=WIDE)
    (a, b, c), (d, e, f) = axes

    a.plot(t, temp, color=RED, lw=1.5)
    a.set_title("plot: how does it evolve?", fontsize=11)
    b.scatter(height, weight, s=8, color=BLUE, alpha=0.7)
    b.set_title("scatter: are two things related?", fontsize=11)
    c.hist(bmi, bins=25, color=PURPLE, alpha=0.8, edgecolor="white")
    c.set_title("hist: how is it distributed?", fontsize=11)
    wards = ["ICU", "CARDIO", "ONCO", "PEDIA", "GERIA"]
    d.bar(wards, [76, 64, 39, 35, 26], color=GREEN)
    d.set_title("bar: how many in each group?", fontsize=11)
    d.tick_params(axis="x", labelsize=8)
    los = [rng.gamma(k, 2.0, 40) for k in (3.5, 2.5, 3.0, 1.5, 4.0)]
    e.boxplot(los, tick_labels=wards, widths=0.6)
    e.set_title("boxplot: how do groups compare?", fontsize=11)
    e.tick_params(axis="x", labelsize=8)
    yy, xx = np.mgrid[-1:1:128j, -1:1:128j]
    f.imshow(np.exp(-((xx / 0.8) ** 2 + (yy / 0.6) ** 2) * 2)
             + 0.1 * rng.normal(size=xx.shape), cmap="gray")
    f.set_title("imshow: what does it look like?", fontsize=11)
    f.set_xticks([])
    f.set_yticks([])
    for ax in (a, b, c, d, e):
        ax.tick_params(labelsize=8)
    fig.tight_layout()
    save(fig, out, "plot_types")


# ===================================================== 5. line plot
def fig_line(out: Path) -> None:
    """Two vitals, shared time axis, a normal band and a threshold."""
    t, temp, hr = _vitals()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=WIDE, sharex=True)
    ax1.fill_between(t, 36.5, 37.5, color=GREEN, alpha=0.12, label="normal range")
    ax1.plot(t, temp, color=RED, marker="o", ms=3, lw=1.6, label="temperature")
    ax1.axhline(38, color=GREY, ls="--", lw=1.2, label="fever (38 °C)")
    ax1.set_ylabel("°C")
    ax1.legend(loc="upper right", fontsize=9, ncols=3)
    ax1.set_ylim(36, 39.2)
    ax2.plot(t, hr, color=BLUE, lw=1.6, label="heart rate")
    ax2.set_ylabel("bpm")
    ax2.set_xlabel("time since admission (h)")
    ax2.legend(loc="upper right", fontsize=9)
    fig.suptitle("Patient P0001, first 48 hours", fontsize=13)
    fig.tight_layout()
    save(fig, out, "line")


# ===================================================== 6. scatter
def fig_scatter(out: Path) -> None:
    """Height against weight: colour by a category, then by a number."""
    height, weight, sex = _cohort()
    bmi = weight / height ** 2
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=WIDE)

    for value, name, colour in ((0, "F", PURPLE), (1, "M", AMBER)):
        m = sex == value
        ax1.scatter(height[m], weight[m], s=14, color=colour, alpha=0.75, label=name)
    ax1.set_title("colour = a category (label=, legend)", fontsize=11)
    ax1.legend(title="sex")

    sc = ax2.scatter(height, weight, s=14, c=bmi, cmap="viridis")
    fig.colorbar(sc, ax=ax2, label="BMI (kg/m²)")
    ax2.set_title("colour = a number (c=, cmap, colorbar)", fontsize=11)
    for ax in (ax1, ax2):
        ax.set_xlabel("height (m)")
        ax.set_ylabel("weight (kg)")
    fig.tight_layout()
    save(fig, out, "scatter")


# ===================================================== 7. histogram bins
def fig_hist_bins(out: Path) -> None:
    """The same 200 values, three bin counts, three different impressions."""
    height, weight, _ = _cohort()
    bmi = weight / height ** 2
    fig, axes = plt.subplots(1, 3, figsize=WIDE, sharey=False)
    for ax, bins in zip(axes, (5, 20, 100)):
        ax.hist(bmi, bins=bins, color=PURPLE, alpha=0.8, edgecolor="white")
        ax.set_title(f"bins={bins}", fontsize=12, family=MONO)
        ax.set_xlabel("BMI (kg/m²)")
    axes[0].set_ylabel("patients")
    axes[0].text(0.5, -0.2, "too coarse: shape hidden", transform=axes[0].transAxes,
                 ha="center", fontsize=10.5, color=AMBER)
    axes[1].text(0.5, -0.2, "about right", transform=axes[1].transAxes, ha="center",
                 fontsize=10.5, color=GREEN)
    axes[2].text(0.5, -0.2, "too fine: noise", transform=axes[2].transAxes,
                 ha="center", fontsize=10.5, color=AMBER)
    fig.tight_layout()
    save(fig, out, "hist_bins")


# ===================================================== 8. bar and box
def fig_bar_box(out: Path) -> None:
    """A count per group needs a bar; a distribution per group needs a box."""
    rng = np.random.default_rng(1)
    wards = ["ICU", "CARDIO", "ONCO", "PEDIA", "GERIA"]
    counts = [76, 64, 39, 35, 26]
    los = [rng.gamma(k, 2.0, n) for k, n in zip((3.5, 2.5, 3.0, 1.5, 4.0), counts)]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=WIDE)

    bars = ax1.bar(wards, counts, color=GREEN)
    ax1.bar_label(bars, fontsize=10)
    ax1.set_ylabel("patients")
    ax1.set_title("ax.bar: patients per ward", fontsize=11)

    ax2.boxplot(los, tick_labels=wards, widths=0.55,
                medianprops={"color": RED, "lw": 1.6})
    ax2.set_ylabel("length of stay (days)")
    ax2.set_title("ax.boxplot: length of stay per ward", fontsize=11)
    ax2.annotate("median", xy=(1.28, np.median(los[0])), xytext=(0.55, 19),
                 fontsize=10, color=RED, arrowprops={"arrowstyle": "->", "color": RED})
    ax2.annotate("outliers", xy=(2.08, np.max(los[1])), xytext=(2.6, 19), fontsize=10,
                 color=GREY, arrowprops={"arrowstyle": "->", "color": GREY})
    fig.tight_layout()
    save(fig, out, "bar_box")


# ===================================================== 9. images
def _phantom(n: int = 256):
    """A crude CT-like slice in Hounsfield units: air, body, two lungs, a spine."""
    yy, xx = np.mgrid[-1:1:n * 1j, -1:1:n * 1j]
    img = np.full((n, n), -1000.0)
    img[(xx / 0.85) ** 2 + (yy / 0.62) ** 2 < 1] = 40
    for cx in (-0.38, 0.38):
        img[((xx - cx) / 0.28) ** 2 + ((yy + 0.05) / 0.42) ** 2 < 1] = -800
    img[(xx / 0.1) ** 2 + ((yy - 0.42) / 0.1) ** 2 < 1] = 700
    img[(xx + 0.08) ** 2 / 0.03 + (yy + 0.05) ** 2 / 0.05 < 1] = 50
    img += np.random.default_rng(0).normal(0, 25, img.shape)
    return img


def fig_imshow(out: Path) -> None:
    """A 2D array is an image: values become colours through a colormap."""
    img = _phantom()
    fig, axes = plt.subplots(1, 3, figsize=WIDE)
    im = axes[0].imshow(img, cmap="gray")
    fig.colorbar(im, ax=axes[0], fraction=0.046, label="HU")
    axes[0].set_title('cmap="gray"', fontsize=11, family=MONO)
    im = axes[1].imshow(img, cmap="gray", vmin=-160, vmax=240)
    fig.colorbar(im, ax=axes[1], fraction=0.046, label="HU")
    axes[1].set_title("vmin=-160, vmax=240", fontsize=11, family=MONO)
    im = axes[2].imshow(img[150:230, 88:168], cmap="gray", vmin=-1000, vmax=200)
    fig.colorbar(im, ax=axes[2], fraction=0.046, label="HU")
    axes[2].set_title("img[150:230, 88:168]", fontsize=11, family=MONO)
    for ax in axes:
        ax.set_xticks([])
        ax.set_yticks([])
    fig.text(0.5, 0.17, "full range  /  soft-tissue window  /  a slice of the array is "
             "a crop of the image", ha="center", fontsize=11, color=GREY)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    save(fig, out, "imshow")


# ===================================================== 10. colour maps
def fig_colormaps(out: Path) -> None:
    """Sequential, diverging, and why jet lies about the data."""
    grad = np.linspace(0, 1, 256)[None, :]
    rows = [("viridis", "sequential: low to high", GREEN),
            ("gray", "sequential: medical images", GREEN),
            ("RdBu_r", "diverging: below / above a centre", GREEN),
            ("jet", "avoid: false edges, unreadable in grey", RED)]
    fig, axes = plt.subplots(len(rows), 2, figsize=WIDE,
                             gridspec_kw={"width_ratios": [1, 1]})
    for (name, what, colour), (ax_c, ax_l) in zip(rows, axes):
        ax_c.imshow(grad, aspect="auto", cmap=name)
        ax_c.set_xticks([])
        ax_c.set_yticks([])
        ax_c.set_ylabel(name, rotation=0, ha="right", va="center", fontsize=11.5,
                        family=MONO)
        # the same colour map seen in black and white: luminance only
        rgb = plt.get_cmap(name)(grad[0])[:, :3]
        lum = (0.2126 * rgb[:, 0] + 0.7152 * rgb[:, 1] + 0.0722 * rgb[:, 2])[None, :]
        ax_l.imshow(lum, aspect="auto", cmap="gray", vmin=0, vmax=1)
        ax_l.set_xticks([])
        ax_l.set_yticks([])
        ax_l.text(1.03, 0.5, what, transform=ax_l.transAxes, fontsize=10.5,
                  color=colour, va="center")
    axes[0][0].set_title("colour", fontsize=11)
    axes[0][1].set_title("printed in black and white", fontsize=11)
    fig.tight_layout(rect=(0.04, 0, 0.78, 1))
    save(fig, out, "colormaps")


# ===================================================== 10b. one image, eight colour maps
def _smooth_field(n: int = 256):
    """A continuous 2D field (think perfusion, mL/100 g/min): no edges, only gradients."""
    yy, xx = np.mgrid[-1:1:n * 1j, -1:1:n * 1j]
    field = (np.exp(-((xx + 0.45) ** 2 + (yy + 0.35) ** 2) / 0.32)
             + 0.75 * np.exp(-((xx - 0.5) ** 2 + (yy - 0.4) ** 2) / 0.18)
             + 0.35 * (xx + 1) / 2)
    field -= field.min()
    return 80 * field / field.max()


def fig_colormap_choice(out: Path) -> None:
    """One continuous field through eight colour maps, each with its context."""
    img = _smooth_field()
    maps = [
        ("gray", "radiology: the convention", GREEN),
        ("bone", "grey with a cold tint: still monotone", GREEN),
        ("viridis", "any measured quantity: uniform", GREEN),
        ("magma", "same, more contrast in the dark values", GREEN),
        ("RdBu_r", "only for a difference from a centre", AMBER),
        ("coolwarm", "same: centre must mean something", AMBER),
        ("jet", "avoid: false edges, brightness jumps", RED),
        ("nipy_spectral", "avoid: colours with no order", RED),
    ]
    fig, axes = plt.subplots(2, 4, figsize=WIDE)
    for (name, what, colour), ax in zip(maps, axes.flat):
        im = ax.imshow(img, cmap=name, vmin=0, vmax=80)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(f'cmap="{name}"', fontsize=10.5, family=MONO, color=colour)
        ax.text(0.5, -0.06, what, transform=ax.transAxes, ha="center", va="top",
                fontsize=9.5, color=colour)
        bar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
        bar.ax.tick_params(labelsize=7.5)
    fig.text(0.5, 0.015, "The same smooth field, the same vmin/vmax: every band or edge "
             "you see below comes from the colour map, not from the data",
             ha="center", fontsize=11, color=INK)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, out, "colormap_choice")


# ===================================================== 11. before / after
def fig_before_after(out: Path) -> None:
    """The defaults versus five small fixes."""
    t, temp, hr = _vitals()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=WIDE)

    ax1.plot(t, temp)
    ax1.plot(t, hr / 2.1)
    ax1.set_title("default", fontsize=12, color=RED)

    ax2.plot(t, temp, color=RED, lw=2, label="temperature")
    ax2.axhline(38, color=GREY, ls="--", lw=1.2)
    ax2.text(46, 38.05, "fever", ha="right", va="bottom", fontsize=10, color=GREY)
    ax2.set_xlabel("time since admission (h)", fontsize=11)
    ax2.set_ylabel("temperature (°C)", fontsize=11)
    ax2.set_title("Fever peaked at 20 h and resolved by 36 h", fontsize=12,
                  color=GREEN)
    ax2.spines[["top", "right"]].set_visible(False)

    ax1.text(0.5, -0.2, "no units, two scales mixed, no message", ha="center",
             transform=ax1.transAxes, fontsize=10.5, color=GREY)
    ax2.text(0.5, -0.2, "one message, labelled axes with units, threshold named",
             ha="center", transform=ax2.transAxes, fontsize=10.5, color=GREY)
    fig.tight_layout()
    save(fig, out, "before_after")


# ===================================================== 12. a patient summary
def fig_dashboard(out: Path) -> None:
    """The closing example: one figure, four panels, one patient in context."""
    t, temp, hr = _vitals()
    height, weight, _ = _cohort()
    bmi = weight / height ** 2
    fig, axes = plt.subplots(2, 2, figsize=WIDE)
    (a, b), (c, d) = axes

    a.plot(t, temp, color=RED, lw=1.6)
    a.axhline(38, color=GREY, ls="--", lw=1)
    a.set_title("temperature (°C)", fontsize=11)
    b.plot(t, hr, color=BLUE, lw=1.6)
    b.set_title("heart rate (bpm)", fontsize=11)
    c.hist(bmi, bins=25, color=GREY, alpha=0.45, edgecolor="white")
    c.axvline(31.2, color=RED, lw=2)
    c.text(31.6, c.get_ylim()[1] * 0.85, "P0001", color=RED, fontsize=10)
    c.set_title("BMI, patient vs cohort", fontsize=11)
    c.set_xlabel("kg/m²", fontsize=10)
    d.scatter(height, weight, s=6, color=GREY, alpha=0.45)
    d.scatter([1.68], [88], s=40, color=RED, zorder=3)
    d.set_title("height (m) vs weight (kg)", fontsize=11)
    for ax in (a, b):
        ax.set_xlabel("hours", fontsize=10)
    for ax in axes.flat:
        ax.tick_params(labelsize=9)
    fig.suptitle("Patient P0001", fontsize=13)
    fig.tight_layout()
    save(fig, out, "dashboard")


FIGURES = (
    fig_anscombe,
    fig_anatomy,
    fig_subplots_grid,
    fig_plot_types,
    fig_line,
    fig_scatter,
    fig_hist_bins,
    fig_bar_box,
    fig_imshow,
    fig_colormaps,
    fig_colormap_choice,
    fig_before_after,
    fig_dashboard,
)


def main() -> None:
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "Programming01/Session03/img")
    out.mkdir(parents=True, exist_ok=True)
    for fn in FIGURES:
        fn(out)
        print(f"{out / (fn.__name__.removeprefix('fig_') + '.png')}")


if __name__ == "__main__":
    main()
