from django.http import HttpResponse
from django.views import View
from requests import Response
from rest_framework.views import APIView

from GroningerAPI.forms import MoneyForm


class MoneyView(View):
    def post(self, request):
        form = MoneyForm(request.POST)
        assert form.is_valid()

        amount = form.cleaned_data['amount']
        currency = form.cleaned_data['currency']
        # logic met je nieuwe data
        return HttpResponse(amount)