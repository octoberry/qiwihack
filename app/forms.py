# coding=utf-8
from wtforms import Form, TextAreaField, IntegerField, StringField, validators


class CardMixin(object):
    card_number = StringField(u'Номер карты:', [validators.DataRequired(message=u'Укажите номер карты'),
                                                validators.Regexp(regex=r'^\d{16}$',
                                                                  message=u'Укажите номер карты в формате '
                                                                          u'XXXXXXXXXXXXXXXX')])
    holder_name = StringField(u'Имя держателя', [validators.DataRequired(message=u'Укажите имя держателя')])
    card_expdate = StringField(u'Срок действия', [validators.DataRequired(message=u'Укажите срок действия')])
    card_cvv = StringField(u'CVV', [validators.DataRequired(message=u'Укажите CVV'),
                                    validators.Regexp(regex=r'^\d{3}$',
                                                      message=u'Укажите корректный CVV')])


class CreateEventForm(Form):
    image = StringField(u'Картинка:', [validators.DataRequired(u'Загрузите фотографию подарка')])
    description = TextAreaField(u'Описание:', [validators.DataRequired(message=u'Расскажите о подаркe')])
    amount = IntegerField(u'Сумма:', [validators.DataRequired(message=u'Укажите сумму'),
                                      validators.NumberRange(min=100, message=u'Сумма должна быть не менее 100 руб.')])


class CardForm(Form, CardMixin):
    pass


class CreateEmailForm(Form):
    email = StringField(u'E-mail:', [validators.DataRequired(message=u'Укажите корректный е-мейл'),
                                     validators.Email(message=u'Укажите корректный е-мейл')])
    tags = StringField()


class PaymentForm(Form, CardMixin):
    amount = IntegerField(u'Сумма:', [validators.DataRequired(message=u'Укажите сумму'),
                                               validators.NumberRange(min=100, message=u'Минимальная сумма 100')])
