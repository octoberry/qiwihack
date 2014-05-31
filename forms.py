# coding=utf-8
from wtforms import Form, TextAreaField


class CreateEventForm(Form):
    description = TextAreaField(u'Описание', [])
