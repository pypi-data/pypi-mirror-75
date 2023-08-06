.PHONY: clean clean-build clean-pyc clean-out docs help
.DEFAULT_GOAL := help

help:

benchmark:
	cd benchmarks; ./benchmark.sh

benchmark-clean:
	rm -fr benchmarks/outputs/

benchmark-report:
	cd benchmarks; ./report.sh

clean: clean-tox clean-build clean-pyc clean-out

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove python file artifacts
	find . -name '__pycache__' -exec rm -fr {} +

clean-out: ## remove hydra outputs
	rm -fr outputs/

clean-tox: ## remove tox cache
	rm -fr .tox

lint: ## check style with flake8
	flake8 boris tests benchmarks

test: ## run tests
	pytest tests

dist: clean # build source and wheel package
	python setup.py sdist bdist_wheel
	ls -l dist

dist-local: clean # build local source and wheel package
	python setup.py sdist bdist_wheel --local
	ls -l dist

install: clean # install the package to active site
	pip install .

install-local: clean # install local package to active site
	python setup.py install --local

uninstall: clean
	pip uninstall borisml