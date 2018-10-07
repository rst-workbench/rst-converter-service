FROM alpine:3.8

RUN apk update && \
    apk add git python2 py2-pip gcc libxml2-dev libxslt-dev \
            graphviz graphviz-dev python2-dev musl-dev && \
    pip install flask flask_restplus pathlib2

WORKDIR /opt
RUN git clone https://github.com/arne-cl/discoursegraphs.git

WORKDIR /opt/discoursegraphs

RUN pip install -r requirements.txt && \
    apk del gcc musl-dev graphviz-dev python2-dev libxml2-dev libxslt-dev && \
    apk add libxslt && \
    pip uninstall -y gvmagic pygraphviz pydot2 pydotplus

WORKDIR /opt/rst-converter-service
ADD app.py .

EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["app.py"]
