.PHONY: pypi-build pypi-test pypi-upload test

pypi-build:
	rm -rf dist/*
	python setup.py sdist bdist_wheel
	twine check dist/*

pypi-test:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

pypi-upload:
	twine upload dist/*

test:
	python tests/test.py