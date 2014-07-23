# coding=utf-8
from wtforms import Form, TextAreaField, IntegerField, StringField, validators


class CreateEventForm(Form):
    image = StringField(u'Картинка:', [validators.DataRequired(u'Загрузите фотографию подарка')])
    description = TextAreaField(u'Описание:', [validators.DataRequired(message=u'Расскажите о подаркe')])
    amount = IntegerField(u'Сумма:', [validators.DataRequired(message=u'Укажите сумму'),
                                      validators.NumberRange(min=100, message=u'Сумма должна быть не менее 100 руб.')])
    card = StringField(u'Номер карты:', [validators.DataRequired(message=u'Укажите номер кредитной карты'),
                                         validators.Regexp(regex=r'^\d{16}$',
                                                           message=u'Укажите номер кредитной карты в формате'
                                                                   u'XXXX-XXXX-XXXX-XXXX')])


class CreateEmailForm(Form):
    email = StringField(u'E-mail:', [validators.DataRequired(message=u'Укажите корректный е-мейл')])