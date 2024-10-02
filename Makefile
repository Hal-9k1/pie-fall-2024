eq = $(and $(findstring $(1),$(2)),$(findstring $(2),$(1)))

all: main-build.py
test:
	py -c '\
	import time\
	import main-build\
	main-build.autonomous_setup()\
	while True:\
		#time.sleep(1 / 1000)\
		main-build.autonomous_main()\
	'
flash:



ifeq (,$(wildcard tmp/Makefile.depends))
tmp/Makefile.depends:
	py preprocessor.py main.py --dependencies > Makefile.depends
endif

ifeq (,$(call eq,clean,$(MAKECMDGOALS)))
include tmp/Makefile.depends
endif
