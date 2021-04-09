release:
	pip install -U twine
	pip install -U setuptools
	pip install -U pip
	make clean
	python setup.py sdist
	python -m twine upload --verbose dist/*

clean :
	rm -rf dist
	rm -rf build
	rm -rf docker_ops.egg-info
	rm -rf .tox

install: clean
	pip uninstall docker-ops
	python setup.py build
	python setup.py install

build-docs:
	pip install sphinx sphinx_rtd_theme pip setuptools -U
	mkdir -p /tmp/docs
	rm -rf /tmp/docs/*
	sphinx-build -b html docs/ /tmp/docs

run-tests:
	PYTHONPATH='.' pytest tess_enumerator_tests

sync-datacube:
	mkdir -p tess_enumerator_test_data
	aws s3 cp s3://stpubdata/tess/public/mast/tess-s0022-4-4-cube.fits ./tess_enumerator_test_data
	# tess2020061235921-s0022-4-4-0174-s_ffic.fits
