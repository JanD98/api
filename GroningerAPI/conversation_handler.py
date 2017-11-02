from GroningerAPI.intent_parser import IntentParser
from GroningerAPI.models import Message, Conversation, User
from GroningerAPI.wit_parser import WitParser

class ConversationHandler:
    def receive_message(self, message_text, user_data):
        try:
            conversation = None
            # beetje dodgy
            if 'first_name' not in user_data:
                user = User.objects.get_or_create(session_id=user_data['id'])
            else:
                user = User.objects.get_or_create(facebook_id=user_data['id'], name=user_data['first_name'], surname=user_data['last_name'])
            print(user)

            if not conversation:
                conversation = Conversation(user=user)
                conversation.save(force_insert=True)
            else:
                conversation = Conversation.objects.order_by("-time_stamp").first()
            print(conversation)

            Message.objects.create(conversation, "message", "user", message_text)

            wit_parser = WitParser()
            parsed_intent = wit_parser.parse(message_text)
            intent_parser = IntentParser()
            result = intent_parser.parse(parsed_intent, conversation)

            Message.objects.create(conversation, "message", "bot", result)

            return result
        except Exception as e:
            print(e)
            return str(e)
