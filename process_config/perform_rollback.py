import couchdb_config_parser
from couchdbkit import *


def perform_rollback(timestamp):
    db = couchdb_config_parser.get_db()
    vr = db.view('homework-remote/events')
    vra = vr.all()
    return vra
