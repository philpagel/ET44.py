RELEASE="0.1"

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
	@echo "Please follow these steps:\n"
	@echo "    1. edit 'src/tests/testconfig.py' so it matches your USB device"
	@echo "    2. Turn on the device\n"
	@echo "Hit ENTER to start the test suite"
	@read RESPONSE
	pytest -v src/tests/ET44_test.py
.Phoney: test


dep-dev:
	python3 -m pip install -r requirements-dev.txt --upgrade
.PHONEY: dep-dev

build: 
	python3 -m build
.PHONEY: build


install: 
	python3 -m pip install dist/et44-$(RELEASE).tar.gz
.PHONEY: install


pypi:
	twine upload dist/*
.PHONEY: pypi


clean:
	rm -rf dist
	rm -rf src/ET44.egg-info
	rm -rf src/ET44/__pycache__
	rm -rf src/tests/__pycache__
.PHONEY: clean
