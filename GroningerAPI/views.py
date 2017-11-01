from django.http import HttpResponse
from django.views import View

from GroningerAPI.forms import MoneyForm


class MoneyView(View):
    def post(self, request):
        form = MoneyForm(request.POST)
        assert form.is_valid()
        # logic met je nieuwe data
        return HttpResponse("TESTT")


class FacebookView(View):
    def get(self, request):
        # token
        return HttpResponse("Hanze2017")
