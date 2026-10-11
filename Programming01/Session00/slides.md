---
title: |
  Session 0\
  Libraries, Environments, and uv
subtitle: "Digital Health, Mastère Spécialisé · 2026"
author: "Paul Dubois"
date: "Week 1, Primer"
---

# 0. Why Python?

## Low level, high level

![](img/levels.png)

::: notes
A language is a level of description. Machine code is what the processor runs: numbers.
Assembly is the same thing with names, one instruction per line. C, C++ and Rust let you
write expressions, but you still decide where every byte lives. Python lets you write the
thing you meant, and decides the rest for you.
Low level buys control and speed, and costs lines of code and bugs (every buffer and every
pointer is yours to get right). High level buys time, and costs some control.
Nothing here is "better": they sit at different points of the same trade.
:::

## Python

![](img/why_python.png)

::: notes
Three reasons, in order of how much they matter to you this year.
1. Popular: it is the most used language in data and in health research. Practically every
   question you will have has been asked and answered already, and every library you need
   has a Python interface.
2. High level: little syntax to learn, so the time goes into the data and not into the
   language. You will be productive in weeks, not years.
3. Still fast: the heavy loops are not run by Python. numpy, pandas and torch are thin
   Python surfaces over compiled C, Fortran, Rust and CUDA. You write the 20 lines that
   describe the computation, and compiled code performs the billion operations.
The honest limit: pure Python loops over millions of rows are slow. The whole skill is
letting the libraries do the loop.
:::

# 1. Libraries

## Shared tasks in many projects

![](img/common_tasks.png)

::: notes
Read a table, draw a figure, multiply two matrices: every project in the room needs these,
and none of them is as simple as it looks. Reading a CSV means separators, quoting,
encodings, missing values and dates. Drawing a figure means axes, ticks, labels and an
export. Multiplying matrices means cache blocking, threads and vector instructions.
Because everybody needs them, they are written once, by people who specialise in exactly
that, and tested by millions of users. That is what a library is.
:::

## Reusing code

![](img/library_value.png)


## Libraries

- Standard libraries
  - `tkinter` (basic GUI)
  - `re` (regular expressions)
  - `json` (reading json files)
- Installed libraries:
  - `numpy` (arrays)
  - `matplotlib`/`seaborn` (plots)
  - `pandas` (data)
  - `scikit-learn` (machine learning)
  - `pytorch` (neurale networks)
  - `pydicom`, `nibabel` (DICOM/NifTi images)  
- Your own files
  - e.g.: a neural network architecture you want to reuse

# 2. Versions, and why environments exist

## Libraries move

![](img/versions.png)

## Projects versions clash 

![](img/conflict.png)

## Virtual environment is a folder

![](img/venv_anatomy.png)

## Making a virtual environment

```bash
python3 -m venv .venv          # create it
source .venv/bin/activate      # Windows: .venv\Scripts\activate

which python3                  # my-project/.venv/bin/python3
python3 -m pip install pandas  # into .venv, not into the system

deactivate
```

## pip

![](img/pip_flow.png)

## Freezing an environment

```bash
python3 -m pip freeze > requirements.txt    # pandas==2.2.3, numpy==2.1.3, ...

# on another machine, in a fresh environment:
python3 -m pip install -r requirements.txt
```

# 3. uv

## What is uv?

![](img/uv_tools.png)

::: notes
`uv` is a single program, written in Rust by Astral (the people behind `ruff`), first
released in 2024. It does the jobs of five separate tools with one command and one
mental model.
Important reassurance: the commands are the ones they already learned. `uv pip
install pandas` does what `pip install pandas` does.
:::

## Speed

![](img/uv_why.png)

## uv in practice
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# no Python required

uv venv
uv pip install pandas

uv add pandas # adds library to lock file
uv sync # install dependencies in the lock file
uv run analysis.py # uses uv venv
```
