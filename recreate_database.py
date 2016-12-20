#!/usr/bin/env python
from os import getenv
from feeder.models import *

drop = getenv("DROP", "False")

if "True" in drop:
    print("Droping,..")
    Base.metadata.drop_all(db_connect())

Base.metadata.create_all(db_connect())

print("Done.")
