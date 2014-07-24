# -*- coding: utf-8 -*-
__author__ = 'fuse'

import requests, uuid
from hashlib import md5
from collections import OrderedDict
import httplib, logging
import traceback

def debug_logging():
    httplib.HTTPConnection.debuglevel = 1
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

MERCHANT_ID = None
PRIVATE_SECURITY_KEY = None

base_url = 'https://secure.payonlinesystem.com/payment'


class Order(object):
    def __init__(self, order_id=None, amount=None, currency='RUB'):
        self.id = order_id
        self.amount = amount
        self.currency = currency

    @staticmethod
    def gen_id():
        return uuid.uuid1()

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

# Id=27454453&Operation=Auth&Result=Ok&Code=200&Status=PreAuthorized&rebillAnchor=3Rbx4VIFBLxc149ZIsYiTekavjSa1rdMqBrFanQ59BU=&binCountry=RU
# Id=27456676&Operation=Auth&Result=Ok&Code=200&Status=PreAuthorized&rebillAnchor=.MeLDV7g.cJL6cMOOybSdVFEDXmZpUINWZ4dCKGlPFg=&binCountry=RU

# Id=27828&Operation=Card2Card&Result=Error&Code=6001&Status=Awaiting3DAuthentication&errorCode=4&pareq=eJx1kt1u4jAQhV8F8QDYTkx+0GCJH1XNRVrE9h4ZZwRhSxKcBMHbd5xNoK20F5bmzIyOx98YPo4W
# cf0HTWtRQYp1rQ84yrP5WEjJ6aA/zVBGXOh9vNeGa70PwyzQ/ljBZrHFi4Ir2jovCyUmfOIBGyS5
# WXPURaNAm8syeVMyiKeRBNZLOKNN1irh6TtfvmyB/dNQ6DOqCi1ey2xX7/5q29x3he6CFlhXBlO2
# RWPvKpA+sEFAaz/VsWmqGWP/N3BNwJ7TbVoX1WR6yzOVrBaH3yc9GZmeDnNgrgMy3aDyiA4PPTES
# 8YxHM48D6/Kgz24aJTwxmVKyl1C5WxaPmit9TwFtwGJhhhcNCvBWlQVSB6F9xMCeQ69eHWDTELpI
# eIHvhTHtIQ5lGAe+T8SDSIjAUe96nGFOrGgCuqcXwJwL6xdKbLp/QNGP//EFdYq3Ew==&acsurl=https://acs.alfabank.ru/acs/PAReq&pd=jkNf8rU11jmd3d8mVqQWsY+PxCmz98mVZwyBXm5PKN48jwcpN2hmJlyWRx5SPP+JqbAZfK+VobGQUY/4vB4WDFJnwmwx8Ued1xiqMIaQXrQ=


# if __name__ == '__main__':
    # order = Order(order_id='133', amount=1.00)
    # card = Card(holder_name='ANDREY ZAKHAROV', number='4154817685289327', exp_date='0315', cvv='696')
    # debug_logging()
    # r = transaction_auth(order, card)
    # if r.get('Result') == 'Ok':
    #     recip_card = RecipientCard(card_number='5559492700675633')
    #     order = Order(order_id='134', amount=100.00)
    #     transaction_card2card(r.get('rebillAnchor'), recip_card, order)
    #     transaction_void(r.get('Id'))

    # rebill_anchor = 'R31bYik5zF5zEuSqCE24DKFoPJvUfNxaIVBscruAF3U='
    # order = Order(order_id='178', amount=1.00)
    # recip_card = RecipientCard(card_number='5559492700675633')
    # transaction_card2card(rebill_anchor, order, recip_card)



