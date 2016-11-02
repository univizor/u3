############################################################
# Dockerfile to run https://github.com/univizor/u3
# Based on Alpine
############################################################

# Set the base image to Alpine
FROM python:3.5-alpine

# File Author / Maintainer
MAINTAINER Jozko Skrablin

################## BEGIN INSTALLATION ######################

# Update apk index, base image and install u3 dependecies.
RUN apk update; apk upgrade; apk add libffi gcc postgresql-dev musl-dev bash libffi-dev libffi-dev libxslt-dev zlib libjpeg-turbo-dev

# Add a user to run app
RUN adduser -D u3

# Add some app directory
RUN mkdir -p /home/u3

# Add the codez
ADD . /home/u3

# Set ownership of teh codez
RUN chown -R u3:u3 /home/u3

ADD ./run-scrapy.sh /usr/local/bin/run-scrapy.sh
RUN chmod +x /usr/local/bin/run-scrapy.sh

# Run pip install
RUN pip install --upgrade -r /home/u3/requirements.txt

# Set workdir
WORKDIR /home/u3

# Add persistent volume for scrapped files
VOLUME /home/u3/data/files

# Set ownership of the home dir
RUN chown -R u3:u3 /home/u3

# ENV vars for running crawler
ENV U3_USER u3
ENV U3_HOME /home/u3
ENV U3_REPO rul
ENV CONCURRENT_REQUESTS 32
ENV DOWNLOAD_DELAY 3
ENV FILES_STORE /home/u3/data/files

# ENV default vars for Pg connection
# and file hashing algorithm
ENV DATABASE_URL postgresql://u3:u3pass@localhost:5432/u3
ENV HASHING_ALGORITHM sha256

USER u3
ENTRYPOINT ["/usr/local/bin/run-scrapy.sh"]

##################### INSTALLATION END #####################
