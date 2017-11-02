from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponse
from django.views import View
from rest_framework import viewsets

from GroningerAPI.IntentParser import Intent_Parser, IntentParser
from GroningerAPI.models import User
from GroningerAPI.serializers import UserSerializer


class ParserView(View):

    def post(self, request):
        print(request.POST)
        data = request.POST
        intent = data.get("intent", "0")
        # debug print(intent)

        user_id = data.get("userId")
        conversation = IntentParser.initialize_user(user_id)

        intent_parser = IntentParser()
        result = getattr(intent_parser, intent)(data, conversation)


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


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request):
        data = request.POST
        email = data.get("email")
        user = User.objects.filter(email=email)
        return HttpResponse(user)

