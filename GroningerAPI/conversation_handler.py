class Conversation_Handler:
    def receive_message(self, message_text, user_data):
        return user_data['first_name'] + " stuurde: " + message_text
