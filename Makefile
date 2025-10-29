help:
	@echo "The following make targets are available:\n"
	@echo "   dep          install dependencies (requirements)"
	@echo "   dep-dev      install dependencies for packaging"
	@echo "   test         run automated test suite. Requires device to be connected."
	@echo "   build        build python package"
	@echo "   install      install python package"
	@echo "   pypi         upload package to pypi"
	@echo "   clean        clean up package and cruft"
.PHONEY: help

dep:
	python3 -m pip install -r requirements.txt
.PHONEY: dep

test:
	pytest -v src/tests/ET44_test.py
.PHONEY: test


build: 
	python3 -m build
.PHONEY: build

clean:
	rm -rf dist
	rm -rf src/ET44.egg-info
	rm -rf src/ET44/__pycache__
	rm -rf src/tests/__pycache__
.PHONEY: clean
