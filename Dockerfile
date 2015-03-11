FROM debian:wheezy
MAINTAINER jj
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install git python python-pip -y && \
   apt-get clean autoclean && apt-get autoremove && \
   rm -rf /var/lib/{apt,dpkg,cache,log}
RUN mkdir /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt && pip install git+https://github.com/httpPrincess/metahosting && pip install gunicorn
ADD . /app/
ENV LC_CTYPE  en_US.utf-8
EXPOSE 8080
VOLUME /app/myapp/data/
WORKDIR /app/
CMD gunicorn -w 4 -b 0.0.0.0:8080  myapp:app


