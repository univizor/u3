# u3

[u3] is scraper and feeder for [univizor] project.

[![Build status][build-status-badge]][build-status]

[![Docker Pulls][docker-pulls-badge]][docker-hub]

[![Docker Stars][docker-stars-badge]][docker-hub]


## Supported scrapers

|   Scraper                          |   Homepage                                                                     | State  |
|------------------------------------|--------------------------------------------------------------------------------|--------|
| [rul](feeder/spiders/rul.py)       | [repozitorij.uni-lj.si](https://repozitorij.uni-lj.si/info/index.php/slo/)     | Done   |
| [dkum](feeder/spiders/dkum.py)     | [dk.um.si](https://dk.um.si)                                                   | Done   |
| [bf](feeder/spiders/bf.py)         | [digitalna-knjiznica.bf.uni-lj.si](http://www.digitalna-knjiznica.bf.uni-lj.si)| Done   |
| [famnit](feeder/spiders/famnit.py) | [famnit.upr.si](http://www.famnit.upr.si)                                      | Done   |
| [ung](feeder/spiders/ung.py)       | [sabotin.ung.si](http://sabotin.ung.si)                                        | Done   |

## Running with Docker Compose

```bash
docker-compose run u3 bf -a categories=biologija -L INFO
```

If you need to rebuild image

```bash
docker build -t univizor/u3:latest .
```

> Some crawling options can be seen in [refresh.sh](./bin/refresh.sh).

## Running natively

Please read [NATIVE.md](NATIVE.md).


## Scripts and tools

- [refresh.sh](./bin/refresh.sh) - Script that starts scraping in parallel fashion. New items will be added to collection.
This script should be ran on periodic intervals via `cron`.
- [recreate_database.py](./recreate_database.py) - Drops all existing tables, and creates new tables with up-to-date structure.

## Configuration

This is default configuration that can be overwritten by setting `ENV` variables.

```
CONCURRENT_REQUESTS = 16
DOWNLOAD_DELAY = 3
FILES_STORE = ./data/files
HASHING_ALGORITHM = sha256 
DATABASE_URL = ...
PERSIST_STATS_INTERVAL = 10
DOGSTATSD_ADDR = ... 
DOGSTATSD_PORT = ...
```

## Sentry

u3 now supports Sentry integration via [scrapy-sentry](https://github.com/llonchj/scrapy-sentry) library.
To use, set the `SENTRY_DSN` environment variable:

```bash
docker run -ti --rm \
  --name u3 \
  --link pg \
  --env DATABASE_URL="postgresql://postgres:@pg:5432/u3_dev" \
  --env SENTRY_DSN="http://public:secret@sentry.io/12345" \
  univizor/u3:latest bf -a categories=biologija
```

## Contributors

- [Oto Brglez](https://github.com/otobrglez)
- [Jozko Skrablin](https://github.com/jozko)

[u3]: https://github.com/univizor/u3
[univizor]: http://univizor.si
[imagelayers-badge]: https://badge.imagelayers.io/univizor/u3:latest.svg
[imagelayers]: https://imagelayers.io/?images=univizor/u3:latest
[docker-pulls-badge]: https://img.shields.io/docker/pulls/univizor/u3.svg
[docker-stars-badge]: https://img.shields.io/docker/stars/univizor/u3.svg
[docker-hub]: https://hub.docker.com/r/univizor/u3/
[build-status-badge]: https://travis-ci.org/univizor/u3.svg?branch=master
[build-status]: https://travis-ci.org/univizor/u3
