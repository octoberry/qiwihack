# -*- coding: utf-8 -*-
__author__ = 'fuse'

import requests
from hashlib import md5
from collections import OrderedDict
import httplib, logging
import traceback
from server import app
from models import PayonlineLog
from pony.orm import commit
import json
from datetime import datetime

def debug_logging():
    httplib.HTTPConnection.debuglevel = 1
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

if app.config['DEBUG']:
    debug_logging()

MERCHANT_ID = app.config['PAYONLINE_MERCHANT_ID']
PRIVATE_SECURITY_KEY = app.config['PAYONLINE_PRIVATE_SECURITY_KEY']
EVENT_ID = None

base_url = 'https://secure.payonlinesystem.com/payment'


class Order(object):
    def __init__(self, order_id=None, amount=None, currency='RUB'):
        self.id = order_id
        self.amount = amount
        self.currency = currency

    @staticmethod
    def gen_id():
        return datetime.now().strftime('%s')

    def to_payonline(self):
        data = OrderedDict()
        data['OrderId'] = self.id
        data['Amount'] = "%.2f" % self.amount
        data['Currency'] = self.currency
        return data


class Card(object):
    def __init__(self, holder_name=None, number=None, exp_date=None, cvv=None):
        self.holder_name = holder_name
        self.number = number
        self.exp_date = exp_date
        self.cvv = cvv

    def to_payonline(self):
        data = OrderedDict()
        data['CardHolderName'] = self.holder_name
        data['CardNumber'] = self.number
        data['CardExpDate'] = self.exp_date
        data['CardCvv'] = self.cvv
        data = OrderedDict(filter(lambda x: x[1], data.iteritems()))
        return data


class RecipientCard(object):
    def __init__(self, rebill_anchor=None, card_number=None):
        self.rebill_anchor = rebill_anchor
        self.card_number = card_number

    def to_payonline(self):
        data = OrderedDict()
        if self.rebill_anchor:
            data['RecipientRebillAnchor'] = self.rebill_anchor
        else:
            data['RecipientCardNumber'] = self.card_number
        return data


class Response(object):
    def __init__(self, body):
        self.body = body
        self.data = self.parse_body(body)

    @staticmethod
    def parse_body(body):
        return OrderedDict([tuple(item.split('=', 1)) for item in body.strip().split('&') if item])

    def get(self, key):
        return self.data[key] if self.data else None

    @property
    def is_ok(self):
        return self.get('Result') == 'Ok'

    @property
    def is_error(self):
        return self.get('Result') == 'Error'

    @property
    def code(self):
        return self.get('Code')

    @property
    def required_3ds(self):
        return self.is_error and self.code == '6001'


def transaction_auth(order, card):
    """
    :type order: Order
    :type card: Card
    :rtype: OrderedDict
    """
    data = order.to_payonline()
    data.update(card.to_payonline())
    return _post('/transaction/auth/', data)


def transaction_void(transaction_id):
    """
    :type transaction_id: int
    :rtype: Response
    """
    return _post('/transaction/void/', OrderedDict(TransactionId=transaction_id))


def get_card_rebill_anchor(card, order_id=None):
    """
    :type card: Card
    :type order_id: str
    :rtype: str|None
    """
    order = Order(amount=1.0)
    order.id = order_id or Order.gen_id()
    r = transaction_auth(order, card)
    if r.get('Result') == 'Ok':
        transaction_void(r.get('Id'))
        return r.get('rebillAnchor')
    return None


def transaction_card2card(rebill_anchor, recip_card, order):
    """
    :type rebill_anchor: str
    :type recip_card: RecipientCard
    :type order: Order
    :rtype: Response
    """
    data = OrderedDict(RebillAnchor=rebill_anchor)
    data.update(recip_card.to_payonline())
    data.update(order.to_payonline())
    return _post('/transaction/card2card/', data, {'Operation': 'Card2Card'})


def transaction_card2card_3ds(pares, pd):
    data = OrderedDict(PARes=pares, PD=pd)
    return _post('/transaction/card2card/3ds/', data, add_security_key=False)


def _post(uri, data, ext_encode_data=None, add_security_key=True):
    """
    :type uri: str
    :type data: OrderedDict
    :rtype: Response
    """
    request_data = OrderedDict(MerchantId=MERCHANT_ID)
    request_data.update(data)
    if add_security_key:
        encode_data = request_data.copy()
        encode_data.update(ext_encode_data or {})
        request_data['SecurityKey'] = _gen_security_key(encode_data)

    try:
        r = requests.post(base_url + uri, data=request_data)
        print r.text
        if r.ok:
            _create_log(uri, request_data, r.text)
        else:
            print r.headers
        return Response(body=r.text)
    except:
        print 'Error Payonline'
        print traceback.format_exc()


_SECURITY_ENCODE_KEYS = ('MerchantId', 'RebillAnchor', 'OrderId', 'Amount', 'Currency',
                         'TransactionId', 'Operation', 'PARes', 'PD')

def _gen_security_key(data):
    encode_data = OrderedDict([(k, data[k]) for k in _SECURITY_ENCODE_KEYS if k in data])
    encode_data['PrivateSecurityKey'] = PRIVATE_SECURITY_KEY
    encode_str = '&'.join(['%s=%s' % (k, v) for k, v in encode_data.iteritems()])
    # print encode_str
    return md5(encode_str).hexdigest()

def _create_log(uri, request_data, response):
    log = PayonlineLog(
        event_id=EVENT_ID,
        operation=_get_operation_by_uri(uri),
        request=json.dumps(request_data),
        response=response
    )
    commit()
    return log

def _get_operation_by_uri(uri):
    return uri.strip('/').split('/')[-1]
