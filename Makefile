SLIDE_SOURCES := $(wildcard */Session*/slides*.md)
SLIDE_TARGETS := $(SLIDE_SOURCES:.md=.pptx)

# Programming01/Session00: the libraries and environments primer
C00_STEMS := library_value ecosystem versions conflict venv_anatomy pip_flow \
             uv_tools uv_why
C00_FIGURES := $(foreach f,$(C00_STEMS),Programming01/Session00/img/$(f).png)

# Programming01/Session01: one figure per concept, from scripts/make_figures_c01.py
C01_STEMS := gui_vs_cli terminal_shell anatomy filesystem pipeline reproducible \
             python_vs_bash interop environments toolchain
C01_FIGURES := $(foreach f,$(C01_STEMS),Programming01/Session01/img/$(f).png)

# the synthetic ward export, one level up because every session shares it
C01_DATA := Programming01/data/patients.csv

.PHONY: slides figures data notebooks clean-slides clean-figures
slides: $(SLIDE_TARGETS)

figures: $(C00_FIGURES) $(C01_FIGURES)

data: $(C01_DATA)

$(C00_FIGURES): scripts/make_figures_c00.py scripts/slidefig.py
	python3 scripts/make_figures_c00.py Programming01/Session00/img

$(C01_FIGURES): scripts/make_figures_c01.py scripts/slidefig.py
	python3 scripts/make_figures_c01.py Programming01/Session01/img

$(C01_DATA): scripts/make_data_c01.py
	python3 scripts/make_data_c01.py Programming01/data

Programming01/Session00/slides.pptx: $(C00_FIGURES)
Programming01/Session01/slides.pptx: $(C01_FIGURES)

%.pptx: %.md scripts/fit_pptx.py
	pandoc $< -o $@ --slide-level=2 --resource-path=$(dir $<)
	python3 scripts/fit_pptx.py $@

clean-slides:
	rm -f $(SLIDE_TARGETS)

clean-figures:
	rm -f $(C00_FIGURES) $(C01_FIGURES)

notebooks:
	python3 scripts/make_notebook_c01.py Programming01/Session01
