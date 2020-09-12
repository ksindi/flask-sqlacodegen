.PHONY: clean build install version release dist

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-test - remove Python file artifacts"
	@echo "clean-eggs - remove cached eggs"
	@echo "build - build package"
	@echo "version - get version number"
	@echo "install - install packages"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "release - package and upload a release"
	@echo "dist - package"

clean: clean-build clean-test clean-eggs
	rm -rf htmlcov/

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

.PHONY: clean-test
clean-test:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf
	rm -rf .pytest_cache/

.PHONY: clean-eggs
clean-eggs:
	rm -rf .eggs/

.PHONY: build
build: clean-build clean-eggs
	python3 setup.py build_ext --inplace

install: clean-build
	python3 setup.py install

version:
	python3 setup.py --version

.PHONY: test
test:
	python3 setup.py test

.PHONY: test-all
test-all:
	tox

.PHONY: release
release: clean build
	python3 setup.py sdist bdist_wheel
	twine check dist/*
	twine upload --verbose dist/*

.PHONY: dist
dist: clean build
	python3 setup.py sdist bdist_wheel
	twine check dist/*
