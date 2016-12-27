#!/usr/bin/env python
from os import getenv
from feeder.models import *

drop = getenv("DROP", "False")
connect = db_connect()

if 'True' in drop:
    print("Dropping,..")
    Base.metadata.drop_all(connect)

Base.metadata.create_all(connect)

print("Done.")
