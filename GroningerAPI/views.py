import json

from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponse
from django.views import View
from rest_framework import viewsets

from GroningerAPI.conversation_handler import Conversation_Handler
from GroningerAPI.facebook import Facebook
from GroningerAPI.intent_parser import IntentParser
from GroningerAPI.models import User
from GroningerAPI.serializers import UserSerializer



class ParserView(View):

    def post(self, request):
        print(request.body)
        data = json.loads(request.body)
        intent = data.get("intent", "0")
        print(intent)

        intent_class = IntentParser()
        result = getattr(intent_class, intent)(data)
        # debug print(intent)

        user_id = data.get("userId")
        conversation = IntentParser.initialize_user(user_id, False)

        intent_parser = IntentParser()
        result = getattr(intent_parser, intent)(data, conversation)


        return HttpResponse(result)


class FacebookView(View):
    def post(self, request):
        raw_body = request.body.decode('utf8')
        message = json.loads(raw_body)
        message = message['entry'][0]
        facebook = Facebook()
        user_id = facebook.get_user_id_form_message(message)
        facebook.send_mark_as_read(user_id)
        facebook.turn_typing_on(user_id)
        message_text = facebook.get_message_text(message)
        user_data = facebook.get_user_data(user_id)
        handler = Conversation_Handler()
        facebook.send_message(user_id, handler.receive_message(message_text, user_data))
        facebook.turn_typing_off(user_id)
        return HttpResponse("received")

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

