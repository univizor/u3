# u3

[u3] is scraper and feeder for [univizor] project.

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

Run PostgreSQL locally on port 7000:

```bash
postgres -D db/pg-data -p 7000
```

## Supported scrapers

|   Scraper                          |   Homepage                                                                     | State  |
|------------------------------------|--------------------------------------------------------------------------------|--------|
| [rul](feeder/spiders/rul.py)       | [repozitorij.uni-lj.si](https://repozitorij.uni-lj.si/info/index.php/slo/)     | Done   |
| [dkum](feeder/spiders/dkum.py)     | [dk.um.si](https://dk.um.si)                                                   | Done   |
| [bf](feeder/spiders/bf.py)         | [digitalna-knjiznica.bf.uni-lj.si](http://www.digitalna-knjiznica.bf.uni-lj.si)| Done   |
| [famnit](feeder/spiders/famnit.py) | [famnit.upr.si](http://www.famnit.upr.si)                                      | Done   |
| [ung](feeder/spiders/ung.py)       | [sabotin.ung.si](http://sabotin.ung.si)                                        | Done   |

## Scripts and tools

- [refresh.sh](./refresh.sh) - Script that starts scraping in parallel fashion. New items will be added to collection.
This script should be ran on periodic intervals via `cron`.
- [recreate_database.py](./recreate_database.py) - Drops all existing tables, and creates new tables with up-to-date structure.
- [first_pages.sh](./tools/first_pages.sh) - Creates picture of first pages from all PDFs.
- [files_for_domain.sh](./tools/files_for_domain.sh) - List local files for specific scrape domain.
- [list_pdfs.sh](./tools/list_pdfs.sh) - List real local PDFs.
- [list_no_pdfs.sh](./tools/list_pdfs.sh) - List real local non-PDFs.

## File Syncing

```bash
tar -cvzf - data/ | split -b 1000m - "sample-files.tar.gz."
s3cmd put -c s3.conf --no-check-md5 -v --progress sample-files.tar.gz.a* s3://univizor/
cat sample-files.tar.gz.* > sample-files.tar.gz
```

## Configuration

This is default configuration that can be overriden by setting `ENV` variables.

```
CONCURRENT_REQUESTS = 32
DOWNLOAD_DELAY = 3
FILES_STORE = ./data/files
DATABASE_URL = ...
HASHING_ALGORITHM = sha256 
```

[u3]: https://github.com/univizor/u3
[univizor]: http://univizor.si
