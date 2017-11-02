from django.http import HttpResponse
from django.views import View
from GroningerAPI.intent_parser import Intent_Parser


class ParserView(View):

    def post(self, request):
        print(request.POST)
        data = request.POST
        intent = data.get("intent", "0")
        print(intent)
        intent_class = Intent_Parser()
        result = getattr(intent_class, intent)(data)

        return HttpResponse(result)


class FacebookView(View):
    def get(self, request):
        # token
        return HttpResponse("Hanze2017")
