from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponse
from django.views import View

from GroningerAPI.intent_parser import Intent_Parser
from GroningerAPI.models import User
from GroningerAPI.serializers import UserSerializer


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
        data = request.GET
        token = data.get("hub.verify_token")
        mode = data.get("hub.mode")
        if token != "hanze2017":
            raise SuspiciousOperation("Token invalid")
        if not mode:
            raise SuspiciousOperation("Mode missing")
        if mode == "subscribe":
            # validate app
            return HttpResponse(data.get("hub.challenge"))
        # something went wrong if this line is reached
        raise SuspiciousOperation("Invalid mode")


class UserView(View):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request):
        data = request.POST
        email = data.get("email")
        user = User.objects.filter(email=email)
        return HttpResponse(user)

