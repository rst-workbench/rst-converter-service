FROM alpine:3.8

RUN apk update && \
    apk add git python2 py2-pip gcc libxml2-dev libxslt-dev \
            graphviz graphviz-dev python2-dev musl-dev \
            python2-tkinter xvfb ghostscript && \
    pip install flask flask_restplus pathlib2 requests pexpect pytest discoursegraphs==0.4.0

WORKDIR /opt/rst-converter-service

ADD app.py test_api.py /opt/rst-converter-service/
ADD xvfb-run /usr/bin/

EXPOSE 5000
ENTRYPOINT ["xvfb-run"]
CMD ["python", "app.py"]

