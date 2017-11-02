import json

from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponse
from django.views import View

from GroningerAPI.conversation_handler import Conversation_Handler
from GroningerAPI.facebook import Facebook
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
    def post(self, request):
        raw_body = request.body.decode('utf8')
        message = json.loads(raw_body)
        message = message['entry'][0]
        facebook = Facebook()
        user_id = facebook.get_user_id_form_message(message)
        message_text = facebook.get_message_text(message)
        user_data = facebook.get_user_data(user_id)
        print (user_data)
        handler = Conversation_Handler()
        facebook.send_message(user_id, handler.receive_message(message_text, user_data))
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
