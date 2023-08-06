DPATH=${CURDIR}

export DPATH
.PHONY:	clean install build_release publish_release

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	rm -Rf *.egg-info
	rm -Rf dist/
	rm -Rf build/

install:
	pip install -r requirements.txt
	find ./requirements -name '*.tar.gz' -exec pip install {} \;
	pip install dist/*.tar.gz

build_release: clean
	python setup.py sdist bdist_wheel

publish_release: build_release
	twine upload dist/*
