# coding=utf-8
from wtforms import Form, TextAreaField, IntegerField, StringField, validators


class CreateEventForm(Form):
    image = StringField(u'Картинка:', [validators.DataRequired(u'Загрузите фотографию подарка')])
    description = TextAreaField(u'Описание:', [validators.DataRequired(message=u'Расскажите о подаркe')])
    amount = IntegerField(u'Сумма:', [validators.DataRequired(message=u'Укажите сумму'),
                                      validators.NumberRange(min=1, message=u'Укажите требуемую сумму')])
    card = StringField(u'Номер карты:', [validators.DataRequired(message=u'Укажите номер кредитной карты'),
                                         validators.Regexp(regex=r'^\d{16}$',
                                                           message=u'Укажите номер кредитной карты в формате'
                                                                   u'XXXX-XXXX-XXXX-XXXX')])

class CreateEmailForm(Form):
    email = StringField(u'E-mail:', [validators.DataRequired(message=u'Укажите корректный е-мейл')])


class PaymentForm(Form):
    amount = IntegerField(u'Сумма:', [validators.DataRequired(message=u'Укажите сумму'),
                                               validators.NumberRange(min=100, message=u'Минимальная сумма 100')])
    card_number = StringField(u'Номер карты:', [validators.DataRequired(message=u'Укажите номер карты'),
                                                validators.Regexp(regex=r'^\d{16}$',
                                                                  message=u'Укажите номер карты в формате '
                                                                          u'XXXXXXXXXXXXXXXX')])
    holder_name = StringField(u'Имя держателя', [validators.DataRequired(message=u'Укажите имя держателя')])
    card_expdate = StringField(u'Срок действия', [validators.DataRequired(message=u'Укажите срок действия')])
    card_cvv = StringField(u'CVV', [validators.DataRequired(message=u'Укажите CVV'),
                                    validators.Regexp(regex=r'^\d{3}$',
                                                      message=u'Укажите корректный CVV')])
