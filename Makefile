.PHONY: pypi-build pypi-test pypi-upload test

pypi-build:
	rm -rf dist/*
	python setup.py sdist bdist_wheel
	python -m twine check dist/*

pypi-test:
	python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

pypi-upload:
	python -m twine upload dist/*

test:
	python tests/test.py