eq = $(and $(findstring $(1),$(2)),$(findstring $(2),$(1)))

.PHONY: all test copy clean
all: main-build.py
test: main-build.py
	python -c '\
	import time\
	import main-build\
	main-build.autonomous_setup()\
	while True:\
		#time.sleep(1 / 1000)\
		main-build.autonomous_main()\
	'
copy: main-build.py
	vim -c 'normal ggvG$"+y' -c ':q' <(python preprocessor.py main.py)
clean:
	rm -f Makefile.depends main-build.py

# Makefile.depends contains a rule to remake itself, if it exists
ifeq (,$(wildcard Makefile.depends))
Makefile.depends:
	python preprocessor.py main.py --dependencies > Makefile.depends
endif

ifeq (,$(call eq,clean,$(MAKECMDGOALS)))
include Makefile.depends
endif
