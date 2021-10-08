FROM alpine:3.8

RUN apk update && \
    apk add coreutils python2 py2-pip gcc libxml2-dev libxslt-dev \
            graphviz graphviz-dev python2-dev musl-dev \
            ghostscript git && \
    pip install -U pip && pip install wheel

WORKDIR /opt/rst-converter
ADD requirements.txt /opt/rst-converter/
RUN pip install -r requirements.txt
RUN pip install lxml
RUN pip install pytest
RUN pip install svgling

ADD setup.py /opt/rst-converter/
ADD src /opt/rst-converter/src
ADD tests /opt/rst-converter/tests

RUN python setup.py install

EXPOSE 5000


ENTRYPOINT ["rst-converter-service"]
