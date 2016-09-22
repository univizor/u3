#!/usr/bin/env python

from feeder.models import *

Base.metadata.drop_all(db_connect())

Base.metadata.create_all(db_connect())