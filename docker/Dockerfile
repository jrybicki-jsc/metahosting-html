FROM debian:wheezy
MAINTAINER jj
RUN DEBIAN_FRONTEND=noninteractive \
   apt-get update && \
   apt-get install python \ 
                   python-pip \
                   git \
                   wget -y && \
   apt-get clean autoclean && \
   apt-get autoremove && \
   rm -rf /var/lib/{apt,dpkg,cache,log}
ENV LC_CTYPE  en_US.utf-8
RUN wget -q -O -  --no-check-certificate https://github.com/httpPrincess/metahosting-html/archive/master.tar.gz | tar zxf - && \
   ln -s metahosting-html-master/ /app && \
   pip install -r /app/requirements.txt && \
   pip install git+https://github.com/httpPrincess/metahosting && \
   cd /app && ./create_users.sh && \
   useradd meta && chown -R meta:meta /app/
EXPOSE 5000
VOLUME /app/myapp/data/
WORKDIR /app/
USER meta
CMD ./run.py
