MAKEFLAGS += --no-builtin-rules

eq = $(and $(findstring $(1),$(2)),$(findstring $(2),$(1)))

.PHONY: all test copy clean
all: mainbuild.py
test: mainbuild.py
	python simulate_auto.py $<
copy: mainbuild.py
	vim -c 'normal ggvG$$"+y' -c ':q' $<
clean:
	rm -f Makefile.depends mainbuild.py

# Makefile.depends contains a rule to remake itself, if it exists
ifeq (,$(wildcard Makefile.depends))
Makefile.depends:
	python preprocessor.py main.py --dependency-file=Makefile.depends --build-file=mainbuild.py
endif

ifeq (,$(call eq,clean,$(MAKECMDGOALS)))
include Makefile.depends
endif
