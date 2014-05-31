# coding=utf-8
from wtforms import Form, TextAreaField, IntegerField, StringField, validators


class CreateEventForm(Form):
    image = StringField(u'Картинка:', [validators.DataRequired(u'Укажите картинку')])
    description = TextAreaField(u'Описание:', [validators.DataRequired(message=u'Укажите описание')])
    amount = IntegerField(u'Сумма:', [validators.DataRequired(message=u'Укажите сумму'),
                                      validators.NumberRange(min=1, message=u'Укажите целое число')])
    card = StringField(u'Номер карты:', [validators.DataRequired(message=u'Укажите номер карты'),
                                         validators.Regexp(regex=r'^\d{16}$',
                                                           message=u'Укажите номер карты в формате '
                                                                   u'XXXXXXXXXXXXXXXX')])
