FROM debian:wheezy
MAINTAINER jj
RUN useradd meta
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install wget python python-pip -y && \
   apt-get clean autoclean && apt-get autoremove && \
   rm -rf /var/lib/{apt,dpkg,cache,log}
RUN wget -O -  --no-check-certificate https://github.com/httpPrincess/meta-html/archive/master.tar.gz | tar zxf - && ln -s meta-html-master/ /app 
EXPOSE 5000
WORKDIR /app/
RUN pip install -r /app/requirements.txt && chown -R meta:meta /app/
VOLUME /app/myapp/data/
USER meta
CMD /app/run.py 
