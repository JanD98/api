import json

from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponse
from django.views import View
from rest_framework import viewsets

from GroningerAPI.conversation_handler import Conversation_Handler
from GroningerAPI.facebook import Facebook
from GroningerAPI.models import User, Message, Conversation
from GroningerAPI.serializers import UserSerializer


class FacebookView(View):
    def post(self, request):
        raw_body = request.body.decode('utf8')
        message = json.loads(raw_body)
        message = message['entry'][0]
        facebook = Facebook()
        facebook_user_id = facebook.get_user_id_form_message(message)
        facebook.send_mark_as_read(facebook_user_id)
        facebook.turn_typing_on(facebook_user_id)
        message_text = facebook.get_message_text(message)
        user_data = facebook.get_user_data(facebook_user_id)
        Message.log(Conversation(pk=1), "message", "user", message_text)
        handler = Conversation_Handler()
        response_text = handler.receive_message(message_text, user_data)
        Message.log(Conversation(pk=1), "message", "bot", response_text)
        facebook.send_message(facebook_user_id, response_text)
        facebook.turn_typing_off(facebook_user_id)
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
