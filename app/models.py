# -*- coding: utf-8 -*-
__author__ = 'fuse'

from server import db, hashids, app
from pony.orm import Required, Optional, select, LongStr, LongUnicode
from datetime import datetime


class Events(db.Entity):
    description = Required(LongUnicode)
    amount = Required(int)
    rebill_anchor = Optional(unicode)
    image = Required(unicode)
    updated_at = Required(datetime)
    created_at = Required(datetime)

    @property
    def income(self):
        return select(sum(t.amount) for t in Transaction if t.status == 1 and t.event_id == self.id)[:1][0]

    @property
    def hashid(self):
        return hashids.encrypt(self.id, int(self.created_at.strftime('%s')))

    @staticmethod
    def get_by_hashid(hashid):
        parts = hashids.decrypt(hashid)
        if len(parts) == 2:
            event_id, _ = parts
            return Events.get(id=event_id)

    @property
    def image_path(self):
        return app.config['UPLOAD_PATH']+self.image


class Transaction(db.Entity):
    event_id = Required(int)
    amount = Required(int)
    md = Required(unicode)
    status = Required(int)
    updated_at = Required(datetime)
    created_at = Required(datetime)


class PayonlineLog(db.Entity):
    _table_ = 'payonline_log'
    event_id = Required(int)
    operation = Required(unicode)
    request = Required(LongStr)
    response = Required(LongStr)
    created_at = Optional(datetime)


class Subscribe(db.Entity):
    email = Required(str)
    tags = Optional(str)
    created_at = Optional(datetime)
    updated_at = Optional(datetime)


db.generate_mapping()
