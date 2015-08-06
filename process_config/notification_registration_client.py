import os
import urllib
import urllib2
import couchdb_config_parser
from add_history import add_history_item

db = couchdb_config_parser.get_db()
base = "https://2-dot-homework-notify.appspot.com/notify/2"

prompts = {
    'growl': 'IP Address',
    'email': 'Email Address',
    'phone': 'Phone Number',
    'twitter': 'Twitter Username'
}


def get_router_id():
    return os.environ['APP_ENGINE_ROUTER_ID']


def edit(doc):
    router = get_router_id()
    data = urllib.urlencode({'service': doc['service'],
                             'userdetails': doc['user'],
                             'suid': doc['suid']})
    hdr = {"Content-type": "application/x-www-form-urlencoded"}
    if len(router) > 0:
        try:
            req = urllib2.Request("%s/%s/edit" % (base, router), data, hdr)
            conn = urllib2.urlopen(req)
            code = conn.getcode()
            if code == 200:
                response = conn.read()
                doc['suid'] = response
                doc['status'] = 'done'
                title = 'Edited notification registration'
                desc = ('Edited %s for %s now identified by %s' %
                        (prompts[doc['service']], doc['name'], doc['user']))
                ts = current_doc['event_timestamp'] if 'event_timestamp' in current_doc else None
                add_history_item(title, desc, doc['_id'], doc['_rev'], True, ts=ts)
                if 'event_timestamp' in doc:
                    del doc['event_timestamp']
        except urllib2.HTTPError, e:
            doc['status'] = 'error'
        except urllib2.URLError, e:
            doc['status'] = 'error'
        finally:
            db.save_doc(doc)


def delete(doc):
    router = get_router_id()
    data = urllib.urlencode({'suid': doc['suid']})
    hdr = {'Content-Type': 'application/x-www-form-urlencoded'}
    if len(router) > 0:
        ret_val = 0
        try:
            req = urllib2.Request("%s/%s/delete" % (base, router), data, hdr)
            conn = urllib2.urlopen(req)
            code = conn.getcode()
            title = 'Removed notification registration'
            desc = ('Removed %s as %s for %s' %
                    (doc['user'], prompts[doc['service']], doc['name']))
            ts = current_doc['event_timestamp'] if 'event_timestamp' in current_doc else None
            add_history_item(title, desc, doc['_id'], doc['_rev'], True, ts=ts)
            if 'event_timestamp' in doc:
                del doc['event_timestamp']
            doc['suid'] = ''
            doc['status'] = 'done'
        except urllib2.HTTPError, e:
            doc['status'] = 'error'
        except urllib2.URLError, e:
            doc['status'] = 'error'
        finally:
            db.save_doc(doc)


def registration(doc):
    router = get_router_id()
    data = urllib.urlencode({'service': doc['service'],
                             'userdetails': doc['user']})
    hdr = {"Content-type": "application/x-www-form-urlencoded"}
    if len(router) > 0:
        try:
            req = urllib2.Request("%s/%s/register" % (base, router), data, hdr)
            conn = urllib2.urlopen(req)
            code = conn.getcode()
            if code == 200:
                response = conn.read()
                doc['suid'] = response
                doc['status'] = 'done'
                title = 'Added notification registration'
                desc = ('Added %s as %s for %s' %
                        (doc['user'], prompts[doc['service']], doc['name']))
                ts = current_doc['event_timestamp'] if 'event_timestamp' in current_doc else None
                add_history_item(title, desc, doc['_id'], doc['_rev'], True, ts=ts)
                if 'event_timestamp' in doc:
                    del doc['event_timestamp']
        except urllib2.HTTPError, e:
            doc['status'] = 'error'
        except urllib2.URLError, e:
            doc['status'] = 'error'
        finally:
            db.save_doc(doc)
