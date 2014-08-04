# -*- coding: utf-8 -*-
from flask import Flask
from pony.orm import Database
from hashids import Hashids

app = Flask(__name__)
app.config.from_pyfile('../default_config.py')
app.config.from_pyfile('../config.py')

if not app.debug and app.config['LOG_FILE']:
    import logging
    file_handler = logging.FileHandler(app.config['LOG_FILE'])
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

db = Database('postgres', app.config['DATABASE'])

hashids = Hashids(salt=app.config['SALT'], min_length=8)

from app import views
