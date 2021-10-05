clean:
	-rm *.pyc
	-rm -rf __pycache__

docker-build:
	docker build -t rst-converter-service .

docker-run:
	docker run -p 5000:5000 -ti rst-converter-service

docker-test:
	docker run --entrypoint=pytest rst-converter-service tests/
