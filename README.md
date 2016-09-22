# u3

[u3] is scraper and feeder for univizor project.

## Setup

Prepare Python3 with virtualenv wrapper.

```bash
mkvirtualenv --no-site-packages --python=/usr/local/Cellar/python3/3.5.2_1/bin/python3 u3

env LDFLAGS="-L$(brew --prefix openssl)/lib" CFLAGS="-I$(brew --prefix openssl)/include" \
  pip install --upgrade -r requirements.txt
```

Initialize PostgreSQL database

```bash
initdb -E utf8 db/pg-data -U postgres
psql -U postgres -c "CREATE DATABASE u3_dev;"
```

## Supported scrapers

|   Scraper                     |   Homepage                                                                     | State  |
|-------------------------------|--------------------------------------------------------------------------------|--------|
| [rul](feeder/spiders/rul.py)  | [repozitorij.uni-lj.si](https://repozitorij.uni-lj.si/info/index.php/slo/)     | Done   |
| [dkum](feeder/spiders/dkum.py)| [dk.um.si](https://dk.um.si)                                                   | Done   |
| [bf](feeder/spiders/bf.py)    | [digitalna-knjiznica.bf.uni-lj.si](http://www.digitalna-knjiznica.bf.uni-lj.si)| Done   |

## Scripts and tools

- [refresh.sh](./refresh.sh) - Script that starts scraping in parallel fashion. New items will be added to collection.
This script should be ran on periodic intervals via `cron`.
- [recreate_database.py](./recreate_database.py) - Drops all existing tables, and creates new tables with up-to-date structure.
- [first_pages.sh](./tools/first_pages.sh) - Creates picture of first pages from all PDFs.

[u3]: https://github.com/univizor/u3
