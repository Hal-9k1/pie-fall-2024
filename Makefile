eq = $(and $(findstring $(1),$(2)),$(findstring $(2),$(1)))

.PHONY: all test copy clean
all: mainbuild.py
test: mainbuild.py
	python simulateauto.py $<
copy: mainbuild.py
	vim -c 'normal ggvG$$"+y' -c ':q' $<
clean:
	rm -f Makefile.depends mainbuild.py

# Makefile.depends contains a rule to remake itself, if it exists
ifeq (,$(wildcard Makefile.depends))
Makefile.depends:
	python preprocessor.py main.py --dependencies --build-file-name=mainbuild.py > Makefile.depends
endif

ifeq (,$(call eq,clean,$(MAKECMDGOALS)))
include Makefile.depends
endif
