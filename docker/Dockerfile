FROM debian:wheezy
MAINTAINER jj
RUN useradd meta
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install wget python python-pip -y && \
   apt-get clean autoclean && apt-get autoremove && \
   rm -rf /var/lib/{apt,dpkg,cache,log}
   locale-gen en_US.UTF-8 
ENV LC_CTYPE  en_US.utf-8
RUN wget -q -O -  --no-check-certificate https://github.com/httpPrincess/meta-html/archive/master.tar.gz | tar zxf - && \
   ln -s meta-html-master/ /app && \
   pip install -r /app/requirements.txt && \
   chown -R meta:meta /app/
EXPOSE 5000
VOLUME /app/myapp/data/
USER meta
CMD /app/run.py 
