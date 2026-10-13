SLIDE_SOURCES := $(wildcard */Session*/slides*.md)
SLIDE_TARGETS := $(SLIDE_SOURCES:.md=.pptx)

# Programming01/Session00: the libraries and environments primer
C00_STEMS := levels why_python common_tasks library_value ecosystem versions \
             conflict venv_anatomy pip_flow uv_tools uv_why
C00_FIGURES := $(foreach f,$(C00_STEMS),Programming01/Session00/img/$(f).png)

# Programming01/Session01: Python types, from scripts/make_figures_c01.py
C01_STEMS := names type_map numbers truthy string_index conversions containers \
             aliasing dict_record sets nested \
             list_vs_array ndarray float_bits float_precision \
             dtype_memory array_index broadcasting axes masks bmi_hist
C01_FIGURES := $(foreach f,$(C01_STEMS),Programming01/Session01/img/$(f).png)

# Programming01/Session02: conditions, loops, functions and classes, from
# scripts/make_figures_c02.py
C02_STEMS := branching boolean for_anatomy loop_helpers_a loop_helpers_b while_loop break_continue \
             comprehension function_anatomy class_anatomy inheritance ward_model
C02_FIGURES := $(foreach f,$(C02_STEMS),Programming01/Session02/img/$(f).png)

# Programming01/Session03: one figure per concept, from scripts/make_figures_c03.py
C03_STEMS := gui_vs_cli terminal_shell anatomy filesystem pipeline reproducible \
             python_vs_bash interop environments toolchain \
             git_why git_areas git_history git_remote
C03_FIGURES := $(foreach f,$(C03_STEMS),Programming01/Session03/img/$(f).png)

# Programming01/Session04: matplotlib, from scripts/make_figures_c04.py
C04_STEMS := anscombe anatomy subplots_grid plot_types line scatter hist_bins bar_box \
             imshow colormaps colormap_choice before_after dashboard
C04_FIGURES := $(foreach f,$(C04_STEMS),Programming01/Session04/img/$(f).png)

# Programming01/Session03/img/datacenter.jpg is a public domain photograph, not a
# generated figure: it is committed, and img/CREDITS.md records where it comes from

# the synthetic ward export, one level up because every session shares it
C01_DATA := Programming01/data/patients.csv

.PHONY: slides figures data clean-slides clean-figures
slides: $(SLIDE_TARGETS)

figures: $(C00_FIGURES) $(C01_FIGURES) $(C02_FIGURES) $(C03_FIGURES) $(C04_FIGURES)

data: $(C01_DATA)

$(C00_FIGURES): scripts/make_figures_c00.py scripts/slidefig.py
	python3 scripts/make_figures_c00.py Programming01/Session00/img

$(C02_FIGURES): scripts/make_figures_c02.py scripts/slidefig.py
	python3 scripts/make_figures_c02.py Programming01/Session02/img

$(C03_FIGURES): scripts/make_figures_c03.py scripts/slidefig.py
	python3 scripts/make_figures_c03.py Programming01/Session03/img

$(C01_FIGURES): scripts/make_figures_c01.py scripts/slidefig.py
	python3 scripts/make_figures_c01.py Programming01/Session01/img

$(C04_FIGURES): scripts/make_figures_c04.py scripts/slidefig.py
	python3 scripts/make_figures_c04.py Programming01/Session04/img

$(C01_DATA): scripts/make_data_c01.py
	python3 scripts/make_data_c01.py Programming01/data

Programming01/Session00/slides.pptx: $(C00_FIGURES)
Programming01/Session01/slides.pptx: $(C01_FIGURES)
Programming01/Session02/slides.pptx: $(C02_FIGURES)
Programming01/Session03/slides.pptx: $(C03_FIGURES)
Programming01/Session04/slides.pptx: $(C04_FIGURES)

%.pptx: %.md scripts/fit_pptx.py
	pandoc $< -o $@ --slide-level=2 --resource-path=$(dir $<)
	python3 scripts/fit_pptx.py $@

clean-slides:
	rm -f $(SLIDE_TARGETS)

clean-figures:
	rm -f $(C00_FIGURES) $(C01_FIGURES) $(C02_FIGURES) $(C03_FIGURES) $(C04_FIGURES)
