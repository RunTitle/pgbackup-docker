FROM python:2.7
MAINTAINER Stephen Durham <stephen.durham@gmail.com>
# Copied devcron setup from MAINTAINER Hamilton Turner <hamiltont@gmail.com>

# Install s3cmd to copy over file
RUN pip install s3cmd

# Install postgres client
ENV PG_MAJOR 9.4
RUN apt-key adv --keyserver ha.pool.sks-keyservers.net --recv-keys B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8
RUN echo 'deb http://apt.postgresql.org/pub/repos/apt/ jessie-pgdg main' $PG_MAJOR > /etc/apt/sources.list.d/pgdg.list

RUN apt-get update \
    && apt-get install -y postgresql-client-$PG_MAJOR mercurial

# Yay devcron
RUN pip install -e hg+https://bitbucket.org/dbenamy/devcron#egg=devcron

# Setup defaults
ADD ./cron /cron

RUN mkdir /data

VOLUME ['/cron','/data']

CMD ["devcron.py", "/cron/crontab"]
