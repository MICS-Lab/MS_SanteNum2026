# Building

```bash
make figures     # regenerate the slide illustrations (matplotlib)
make data        # regenerate the synthetic ward export the notebook works on
make notebooks   # regenerate notebook.ipynb and notebook_solutions.ipynb
make slides      # slides.md -> slides.pptx (pandoc, then a post-processing pass)
```

Slides are written in Markdown and converted with `pandoc --slide-level=2`, so every
`##` heading is one slide and every `::: notes` block becomes speaker notes.
`scripts/fit_pptx.py` then patches the result: it enables autofit (pandoc leaves it
off, so long slides silently overflow) and centres `>` blockquotes, which is how a
deck asks the room a question.

Both notebooks are generated from `scripts/make_notebook_c01.py`, which holds each
exercise and its answer side by side, so the student version and the solutions can
never drift apart. Edit that script, not the `.ipynb` files.

## Requirements

`pandoc`, and Python with `matplotlib` and `pillow`. The notebook needs a Jupyter
Python kernel and a `bash` on `PATH`; every code cell is a `%%bash` cell.
