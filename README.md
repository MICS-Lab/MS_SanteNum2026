# Digital Health, Mastère Spécialisé 2026

Course materials for the *Digital Health* specialised master, 2026.

Everything comes in two languages. The English file is the original, the `-fr` one is
its French twin, rebuilt from `translations/fr.json` (see [BUILDME.md](BUILDME.md)).
The French is a machine first pass, corrected by hand in that file, so report a clumsy
sentence as a bug rather than editing a `-fr` file, which the next build overwrites.

### Sessions

**Session 0: Libraries, environments, and uv**

- Slides: [md](Programming01/Session00/slides.md), [pptx](Programming01/Session00/slides.pptx)
- Slides (fr): [md](Programming01/Session00/slides-fr.md), [pptx](Programming01/Session00/slides-fr.pptx)

**Session 1: Python types**

- Slides: [md](Programming01/Session01/slides.md), [pptx](Programming01/Session01/slides.pptx)
- Slides (fr): [md](Programming01/Session01/slides-fr.md), [pptx](Programming01/Session01/slides-fr.pptx)
- Notebook: [exercises](Programming01/Session01/python_types.ipynb), [solutions](Programming01/Session01/python_types-solutions.ipynb)
- Notebook (fr): [exercices](Programming01/Session01/python_types-fr.ipynb), [corrigé](Programming01/Session01/python_types-solutions-fr.ipynb)

**Session 2: Conditions, loops and classes**

- Slides: [md](Programming01/Session02/slides.md), [pptx](Programming01/Session02/slides.pptx)
- Slides (fr): [md](Programming01/Session02/slides-fr.md), [pptx](Programming01/Session02/slides-fr.pptx)
- Notebook: [exercises](Programming01/Session02/python_basics.ipynb), [solutions](Programming01/Session02/python_basics-solutions.ipynb), [class version](Programming01/Session02/python_basics-class.ipynb)
- Notebook (fr): [exercices](Programming01/Session02/python_basics-fr.ipynb), [corrigé](Programming01/Session02/python_basics-solutions-fr.ipynb), [version cours](Programming01/Session02/python_basics-class-fr.ipynb)

**Session 3: The command line, and NumPy arrays**

- Slides: [md](Programming01/Session03/slides.md), [pptx](Programming01/Session03/slides.pptx)
- Slides (fr): [md](Programming01/Session03/slides-fr.md), [pptx](Programming01/Session03/slides-fr.pptx)
- Command line: [exercises](Programming01/Session03/command_line.ipynb), [solutions](Programming01/Session03/command_line-solutions.ipynb)
- Command line (fr): [exercices](Programming01/Session03/command_line-fr.ipynb), [corrigé](Programming01/Session03/command_line-solutions-fr.ipynb)
- NumPy arrays: [exercises](Programming01/Session03/numpy_arrays.ipynb), [solutions](Programming01/Session03/numpy_arrays-solutions.ipynb)
- NumPy arrays (fr): [exercices](Programming01/Session03/numpy_arrays-fr.ipynb), [corrigé](Programming01/Session03/numpy_arrays-solutions-fr.ipynb)

**Session 4: Tables with pandas, plots with Matplotlib**

- Slides: [md](Programming01/Session04/slides.md), [pptx](Programming01/Session04/slides.pptx)
- Slides (fr): [md](Programming01/Session04/slides-fr.md), [pptx](Programming01/Session04/slides-fr.pptx)
- pandas: [exercises](Programming01/Session04/pandas.ipynb), [solutions](Programming01/Session04/pandas-solutions.ipynb)
- pandas (fr): [exercices](Programming01/Session04/pandas-fr.ipynb), [corrigé](Programming01/Session04/pandas-solutions-fr.ipynb)
- Matplotlib: [exercises](Programming01/Session04/matplotlib.ipynb), [solutions](Programming01/Session04/matplotlib-solutions.ipynb)
- Matplotlib (fr): [exercices](Programming01/Session04/matplotlib-fr.ipynb), [corrigé](Programming01/Session04/matplotlib-solutions-fr.ipynb)

### Data

The synthetic ward export the notebooks work on lives in `Programming01/data/`,
one level up from the sessions, because every session shares it. It is not in the
repository: the first cell of each notebook rebuilds it (`scripts/make_data_c01.py`),
and it is seeded, so everybody gets the same 240 patients.

### Building

Slides, figures and the French notebooks are generated: see [BUILDME.md](BUILDME.md).
