from couchdbkit import *
import ConfigParser


def getDB():
    config = ConfigParser.ConfigParser()
    path = "/home/homeuser/couchdb.conf"
    config.read(path)
    user = config.get('DEFAULT', 'ADMIN')
    password = config.get('DEFAULT', 'ADMIN_PASSWORD')
    port = config.get('DEFAULT', 'PORT')
    db_name = config.get('DEFAULT', 'DB')
    server_name = config.get('DEFAULT', 'SERVER_NAME')
    s = Server('http://%s:%s@%s:%s' % (user, password, server_name, port))
    db = s[db_name]
    return db
