# -*- coding: utf-8 -*-
__author__ = 'fuse'

import requests, json

import httplib, logging
httplib.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

id_device = 'CHIPIN'
base_url = 'http://split2pay.ru:8080/splittpay/rest'

def add_event(amount, card_number, owner_name, members):
    data = {
        'id_dev': id_device,
        'sum': str(amount),
        'card_number': card_number,
        'owner_name': owner_name,
        'members': members
    }
    r = _post('/addEvent', data)
    print r.content
    return r.json()

def _post(uri, data):
    return requests.post(base_url + uri, data=json.dumps(data), headers={'Content-Type': 'application/json'})

def default_member(amount):
    return {'name': 'Default member', 'credit': str(amount), 'debit': '0', 'tel_number': '79000000000'}

def test_event():
    return {u'event_sum': 100, u'owner_name': u'fuse', u'timestamp': u'2014-05-31 18:26:59', u'id_event': 4111, u'owner_card_number': u'5559492700675633', u'members': [{u'status': 0, u'tel_number': u'79032930205', u'name': u'Andrey Zakharov', u'id_member': 1385, u'credit': 100, u'debet': u'0'}], u'owner_id': 1371}

if __name__ == '__main__':
    event = add_event(
        amount='100',
        card_number='5559492700675633',
        owner_name='Andrey Pachay',
        members=[{'name': 'Andrey Zakharov', 'credit': '100', 'debit': '0', 'tel_number': '79032930205'}]
    )
    print event

