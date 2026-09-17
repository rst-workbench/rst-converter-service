FROM python:3.14-slim

RUN apt-get update && apt-get upgrade -y

WORKDIR /opt/rst-converter
COPY requirements.txt /opt/rst-converter/
RUN pip install -r requirements.txt

COPY setup.py /opt/rst-converter/
COPY src /opt/rst-converter/src
COPY tests /opt/rst-converter/tests

RUN pip install .

EXPOSE 5000

ENTRYPOINT ["rst-converter-service"]
