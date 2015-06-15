import os
import urllib
import urllib2
import couchdb_config_parser


def get_router_id():
    return os.environ['APP_ENGINE_ROUTER_ID']


def edit(doc):
    router = get_router_id()
    data = urllib.urlencode({'service': doc['service'], 'userdetails': doc['user'], 'suid': doc['suid']})
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    if len(router) > 0:
        try:
            req = urllib2.Request("https://2-dot-homework-notify.appspot.com/notify/2/%s/edit" % (router), data, headers)
            conn = urllib2.urlopen(req)
            code = conn.getcode()
            if code == 200:
                response = conn.read()
                doc['suid'] = response
                doc['status'] = 'done'
                add_history.add_history_item('Edited notification registration', 'Edited registration for %s for service %s now identified by %s' % (doc['name'], doc['service'], doc['user']), doc['_id'], doc['_rev'], True)
        except urllib2.HTTPError, e:
            doc['status'] = 'error'
        except urllib2.URLError, e:
            doc['status'] = 'error'
        finally:
            db.save_doc(doc)


def delete(doc):
    router = get_router_id()
    data = urllib.urlencode({'suid': doc['suid']})
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    if len(router) > 0:
        ret_val = 0
        try:
            req = urllib2.Request("https://2-dot-homework-notify.appspot.com/notify/2/%s/delete" % (router), data, headers)
            conn = urllib2.urlopen(req)
            code = conn.getcode()
            add_history.add_history_item('Removed notification registration', 'Removed registration for %s for service %s identified by %s' % (doc['name'], doc['service'], doc['user']), doc['_id'], doc['_rev'], True)
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
    data = urllib.urlencode({'service': doc['service'], 'userdetails': doc['user']})
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    if len(router) > 0:
        try:
            req = urllib2.Request("https://2-dot-homework-notify.appspot.com/notify/2/%s/register" % (router), data, headers)
            conn = urllib2.urlopen(req)
            code = conn.getcode()
            if code == 200:
                response = conn.read()
                doc['suid'] = response
                doc['status'] = 'done'
                add_history.add_history_item('Added notification registration', 'Added registration for %s for service %s identified by %s' % (doc['name'], doc['service'], doc['user']), doc['_id'], doc['_rev'], True)
        except urllib2.HTTPError, e:
            doc['status'] = 'error'
        except urllib2.URLError, e:
            doc['status'] = 'error'
        finally:
            db.save_doc(doc)
