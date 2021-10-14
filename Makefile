clean:
	-rm -rf build dist
	-find -name '*.pyc' -exec rm {} \;
	-find -name '__pycache__' -exec rm -rf {} \;
	-find -name 'rstconverter.egg-info' -exec rm -rf {} \;

install:
	pip install -r requirements.txt
	python setup.py install

test:
	pytest

coverage:
	coverage run --source=rstconverter,./tests -m pytest
	coverage report --sort=cover

docker-build:
	docker build -t rst-converter-service .

docker-run:
	docker run -p 5000:5000 -ti rst-converter-service

docker-exec:
	docker run -p 5000:5000 --entrypoint=bash -ti rst-converter-service

docker-test:
	docker run --entrypoint=pytest rst-converter-service --cov=rstconverter
