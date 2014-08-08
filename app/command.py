# coding=utf-8

from flask.ext.script import Manager
from flask import url_for
from server import app, hashids
from pony.orm import db_session
from models import Events

manager = Manager(app)


@manager.command
@manager.option(dest='event_id')
@db_session
def event_url(event_id):
    event = Events.get(id=event_id)
    if event:
        print event.description, url_for('event', hashid=event.hashid)
    else:
        print 'Event not found'


@manager.command
@manager.option(dest='hashid')
@db_session
def event_info(hashid):
    event = Events.get_by_hashid(hashid)
    print hashids.decrypt(hashid)
    if event:
        print event.id, event.description, event.amount
    else:
        print 'Event not found'
        print hashids.decrypt(hashid)

