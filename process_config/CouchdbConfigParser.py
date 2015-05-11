from couchdbkit import *
import ConfigParser


def getDB():
    config = ConfigParser.ConfigParser({"ADMIN": "",
                                        "ADMIN_PASSWORD": "",
                                        "PORT": "5984",
                                        "DB": "config",
                                        "SERVER_NAME": "localhost"})
    path = "/home/homeuser/couchdb.conf"
    config.read(path)
    user = config.get('DEFAULT', 'ADMIN')
    password = config.get('DEFAULT', 'ADMIN_PASSWORD')
    port = config.get('DEFAULT', 'PORT')
    db_name = config.get('DEFAULT', 'DB')
    server_name = config.get('DEFAULT', 'SERVER_NAME')
    addr = 'http://%s:%s@%s:%s' % (user, password, server_name, port) if len(user) > 0 else 'http://%s:%s' % (server_name, port)
    print addr
    s = Server(addr)
    db = s[db_name]
    return db
