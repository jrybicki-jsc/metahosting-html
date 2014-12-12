FROM debian:wheezy
MAINTAINER jj
RUN useradd meta
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install wget python python-pip -y && \
   apt-get clean autoclean && apt-get autoremove && \
   rm -rf /var/lib/{apt,dpkg,cache,log}
ENV LC_CTYPE  en_US.utf-8
RUN wget -q -O -  --no-check-certificate https://github.com/httpPrincess/metahosting-html/archive/master.tar.gz | tar zxf - && \
   ln -s metahosting-html-master/ /app && \
   pip install -r /app/requirements.txt && \
   cd /app && ./create_users.sh && \
   chown -R meta:meta /app/
EXPOSE 5000
VOLUME /app/myapp/data/
WORKDIR /app/
USER meta
CMD ./run.py 
