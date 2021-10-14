FROM python:3.9-slim

RUN apt-get update && apt-get upgrade -y

WORKDIR /opt/rst-converter
ADD requirements.txt /opt/rst-converter/
RUN pip install -r requirements.txt

ADD setup.py /opt/rst-converter/
ADD src /opt/rst-converter/src
ADD tests /opt/rst-converter/tests

RUN python setup.py install

EXPOSE 5000

ENTRYPOINT ["rst-converter-service"]
