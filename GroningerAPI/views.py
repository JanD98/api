import json

from django.core.exceptions import SuspiciousOperation
from django.db import connection
from django.http import HttpResponse
from django.views import View
from rest_framework import viewsets

from GroningerAPI.conversation_handler import ConversationHandler
from GroningerAPI.facebook import Facebook
from GroningerAPI.models import User
from GroningerAPI.serializers import UserSerializer


class ConversationView(View):
    def get(self, request):
        facebook = Facebook()
        with connection.cursor() as cursor:
            cursor.execute(
                "select c.id, data as last_message, m.time_stamp, sender, u.facebook_id"
                " from GroningerAPI_message m" +
                " JOIN GroningerAPI_conversation c on m.conversation_id = c.id" +
                " JOIN GroningerAPI_user u on c.user_id = u.id" +
                " GROUP BY conversation_id" +
                " order by m.time_stamp DESC", )
            rows = cursor.fetchall()
        data = []
        for row in rows:
            facebook_user = facebook.get_user_data(facebook_id=row[4])
            data.append({
                "id": row[0],
                "last_message": row[1],
                'timestamp': row[2].strftime('%s'),
                'sender': row[3],
                'image': facebook_user['profile_pic'],
                'name': facebook_user["first_name"] + " " + facebook_user["last_name"]
            })
        return HttpResponse(json.dumps(data))

    def post(self, request):
        return HttpResponse("received")


class FacebookView(View):
    def post(self, request):
        raw_body = request.body.decode('utf8')
        message = json.loads(raw_body)
        message = message['entry'][0]
        facebook = Facebook()
        facebook_user_id = facebook.get_user_id_form_message(message)
        user_data = facebook.get_user_data(facebook_user_id)
        if 'message' in message['messaging'][0]:
            # message request
            print("message")
            facebook.send_mark_as_read(facebook_user_id)
            facebook.turn_typing_on(facebook_user_id)
            message_text = facebook.get_message_text(message)

            handler = ConversationHandler()
            response_text = handler.receive_message(message_text, user_data)

            facebook.send_message(facebook_user_id, response_text)
            facebook.turn_typing_off(facebook_user_id)
        elif 'optin' in message['messaging'][0]:
            # optin request
            session_token = facebook.get_user_token_from_optin_request(message)
            # check if user exists for token
            user, created = User.objects.get_or_create(session_id=session_token)
            user.facebook_id = facebook_user_id
            user.save()
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
