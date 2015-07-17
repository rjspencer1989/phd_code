#!/usr/bin/env python

from couchdbkit import *

from process_config import couchdb_config_parser

db = couchdb_config_parser.get_db()
db.flush()
