from django.forms import Form, DecimalField, CharField


class MoneyForm(Form):
    amount = DecimalField()
    currency = CharField()