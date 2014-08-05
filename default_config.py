import os

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/app/static/uploads/'
UPLOAD_PATH = 'uploads/'
UPLOAD_SIZE = 250, 250

DATABASE = "postgres://username:password@localhost/database"

DEBUG = True
ASSETS_DEBUG = True
LOG_FILE = ''

SALT = 'secret_peerpay_salt'

MIN_EVENT_AMOUNT = 100

DISABLED_PAYMENT_TYPES = ['qiwi', 'yandex', 'webmoney']

PAYONLINE_MERCHANT_ID = 0
PAYONLINE_PRIVATE_SECURITY_KEY = ''