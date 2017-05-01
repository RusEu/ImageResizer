FROM ubuntu:16.04

MAINTAINER bidstopper@gmail.com

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
        git \
        python-dev \
        python-setuptools \
        python-pip \
        nginx \
        supervisor

RUN pip install uwsgi

COPY app /home/docker/code/thumbnailer/

RUN pip install -r /home/docker/code/thumbnailer/requirements.txt

RUN echo "daemon off;" >> /etc/nginx/nginx.conf

COPY configuration/uwsgi/thumbnailer.ini /home/docker/code/thumbnailer/uwsgi.ini
COPY configuration/nginx/thumbnailer.conf /etc/nginx/sites-available/default
COPY configuration/supervisor/supervisor.conf /etc/supervisor/conf.d/supervisor.conf

CMD ["supervisord", "-n"]
