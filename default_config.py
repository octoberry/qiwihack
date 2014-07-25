import os

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/app/static/uploads/'
UPLOAD_PATH = '/static/uploads/'
UPLOAD_SIZE = 250, 250

DATABASE = "postgres://username:password@localhost/database"

DEBUG = True

SALT = 'secret_peerpay_salt'

MIN_EVENT_AMOUNT = 100
