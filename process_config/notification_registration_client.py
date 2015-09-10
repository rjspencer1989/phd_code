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


def edit(doc, from_undo=False):
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
                if from_undo is True:
                    title = 'Undo edit of notification registration'
                    desc = ('Undo edit of %s for %s. %s is now identified by %s' %
                            (prompts[doc['service']], doc['name'], doc['name'], doc['user']))
                ts = doc['event_timestamp'] if 'event_timestamp' in doc else None
                doc_arr = [{'doc_id': doc['_id'], 'doc_rev': doc['_rev'], 'doc_collection': 'notifications', 'action': 'edit'}]
                add_history_item(title, desc, doc_arr, True, ts=ts)
                if 'event_timestamp' in doc:
                    del doc['event_timestamp']
        except urllib2.HTTPError, e:
            doc['status'] = 'error'
        except urllib2.URLError, e:
            doc['status'] = 'error'
        finally:
            db.save_doc(doc)


def delete(doc, from_undo=False):
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
            if from_undo is True:
                title = 'Undo adding notification registration'
            ts = doc['event_timestamp'] if 'event_timestamp' in doc else None
            doc_arr = [{'doc_id': doc['_id'], 'doc_rev': doc['_rev'], 'doc_collection': 'notifications', 'action': 'delete'}]
            add_history_item(title, desc, doc_arr, True, ts=ts)
            if 'event_timestamp' in doc:
                del doc['event_timestamp']
            del doc['suid']
            doc['status'] = 'done'
        except urllib2.HTTPError, e:
            doc['status'] = 'error'
        except urllib2.URLError, e:
            doc['status'] = 'error'
        finally:
            db.save_doc(doc)


def registration(doc, from_undo=False):
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
                if from_undo is True:
                    title = 'Undo removal of notification registration'
                ts = doc['event_timestamp'] if 'event_timestamp' in doc else None
                doc_arr = [{'doc_id': doc['_id'], 'doc_rev': doc['_rev'], 'doc_collection': 'notifications', 'action': 'add'}]
                add_history_item(title, desc, doc_arr, True, ts=ts)
                if 'event_timestamp' in doc:
                    del doc['event_timestamp']
        except urllib2.HTTPError, e:
            doc['status'] = 'error'
        except urllib2.URLError, e:
            doc['status'] = 'error'
        finally:
            db.save_doc(doc)
