FROM python:3.5

ENV CONCURRENT_REQUESTS=32 \
  DOWNLOAD_DELAY=3 \
  FILES_STORE="./data/files" \
  HASHING_ALGORITHM="sha256"

RUN mkdir /home/u3
ADD . /home/u3
WORKDIR /home/u3

RUN pip install --quiet --upgrade -r requirements.txt

VOLUME /home/u3/data

ENTRYPOINT ["scrapy"]