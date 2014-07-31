# coding=utf-8
from wtforms import Form, TextAreaField, IntegerField, StringField, validators, ValidationError


class Luhn(object):
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        value = field.data
        valid = False
        if value:
            valid = self.luhn_checksum(value) == 0

        if not valid:
            message = self.message
            if message is None:
                message = field.gettext('Invalid card number.')
            raise ValidationError(message)

    @staticmethod
    def luhn_checksum(card_number):
        def digits_of(n):
            return [int(d) for d in str(n)]
        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = 0
        checksum += sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d*2))
        return checksum % 10


class CardMixin(object):
    card_number = StringField(u'Номер карты:', [validators.DataRequired(message=u'Укажите номер карты'),
                                                validators.Regexp(regex=r'^\d{16}$',
                                                                  message=u'Укажите номер карты в формате '
                                                                          u'XXXXXXXXXXXXXXXX'),
                                                Luhn(message=u'Проверьте номер кредитной карты')])
    holder_name = StringField(u'Имя держателя', [validators.DataRequired(message=u'Укажите имя держателя')])
    exp_month = StringField(u'Срок действия', [validators.DataRequired(message=u'Укажите месяц срока действия')])
    exp_year = StringField(u'Срок действия', [validators.DataRequired(message=u'Укажите год срока действия')])
    card_cvv = StringField(u'CVV', [validators.DataRequired(message=u'Укажите CVV'),
                                    validators.Regexp(regex=r'^\d{3}$',
                                                      message=u'Укажите корректный CVV')])

    @property
    def card_expdate(self):
        return "%s%s" % (self.exp_month.data, self.exp_year.data)


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
