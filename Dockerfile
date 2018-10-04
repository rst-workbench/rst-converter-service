FROM alpine:3.8

RUN apk update && \
    apk add git python2 py2-pip && \
    pip install flask flask_restplus

WORKDIR /opt
RUN git clone https://github.com/arne-cl/discoursegraphs.git

WORKDIR /opt/discoursegraphs
RUN apk add gcc
RUN apk add libxml2-dev libxslt-dev graphviz graphviz-dev
RUN apk add python2-dev
RUN apk add musl-dev
#RUN apk add linux-headers
RUN pip2 install -r requirements.txt

WORKDIR /opt/rst-converter-service
RUN pip install pathlib2
ADD app.py .

EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["app.py"]

