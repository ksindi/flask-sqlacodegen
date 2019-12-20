.PHONY: clean-pyc clean-build docs clean build install install-all version

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "release - package and upload a release"
	@echo "dist - package"

clean: clean-build clean-pyc

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

version:
	python setup.py --version

release: clean build
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: clean build
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist
