FROM alpine:3.8

RUN apk update && \
    apk add coreutils python2 py2-pip gcc libxml2-dev libxslt-dev \
            graphviz graphviz-dev python2-dev musl-dev \
            ghostscript git && \
    pip install -U pip && pip install wheel && \
    pip install pexpect==4.7.0 requests==2.22.0 pathlib2==2.3.5 \
        Werkzeug==0.16.0 flask==1.1.2 flask_restplus==0.13.0

WORKDIR /opt
# --branch is used to fetch a specific tag (not branch!) here
RUN git clone --branch discoursegraphs-0.4.12 https://arne-cl@github.com/arne-cl/discoursegraphs.git

WORKDIR /opt/discoursegraphs
RUN pip install -r requirements.txt

WORKDIR /opt/rst-converter-service
ADD app.py test_api.py /opt/rst-converter-service/


EXPOSE 5000


ENTRYPOINT ["python"]
CMD ["app.py"]
