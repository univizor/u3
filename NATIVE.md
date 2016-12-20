# u3 natively

## Setup

Prepare Python3 with virtualenv wrapper.

```bash
PYTHON_PATH=/usr/local/Cellar/python3/3.5.2_1/bin/python3
mkvirtualenv --no-site-packages --python=$PYTHON_PATH u3
env LDFLAGS="-L$(brew --prefix openssl)/lib" \
  CFLAGS="-I$(brew --prefix openssl)/include" \
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
