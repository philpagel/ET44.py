help:
	@echo "The following make targets are available:\n"
	@echo "   test         run automated test suite. Requires device to be connected."
	@echo "   build        build python package and firmware updater"
	@echo "   clean        clean up package and cruft"
.PHONEY: help

test:
	pytest -v src/tests/ET44_test.py
.PHONEY: test

build: 
	python3 -m build
	make -C tools/fwupdater/ build
.PHONEY: build

clean:
	rm -rf dist
	rm -rf src/ET44.egg-info
	rm -rf src/ET44/__pycache__
	rm -rf src/tests/__pycache__
	make -C tools/fwupdater/ clean
.PHONEY: clean
