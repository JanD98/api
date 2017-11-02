from facepy import GraphAPI

from GroningerAPI.intent_parser import IntentParser


class Facebook:
    graph = ""
    api_token = "EAAEGVfJehVABALbXGQ1z5ex7UlGYobpKsMa7LwdJMi4ZCnkUzOoaTeNKZANNlAU6silAvaDxD2q5jNOX5ijPblOk8CtOg7Qz5UQqFwZBmZCXmZAvBSDOze0FQXU0cZB573edC9det4FIZBT9Bt343Cyg6bz9Qg9j7jxlEFEMs0abDpYZBfwhH3pv"

    def __init__(self):
        self.graph = GraphAPI(self.api_token)

    def get_user_id_form_message(self, json):
        return json['messaging'][0]['sender']['id']

    def get_message_text(self, json):
        return json['messaging'][0]['message']['text']

    def get_user_data(self, facebook_id):
        return self.graph.get(facebook_id)

    def send_message(self, facebook_id, message):
        self.graph.post(path='me/messages', recipient={"id": facebook_id}, message={"text": message})

    def send_sender_action(self, facebook_id, action):
        self.graph.post(path='me/messages', recipient={"id": facebook_id}, sender_action=action)

    def send_mark_as_read(self, facebook_id):
        self.send_sender_action(facebook_id, "mark_seen")

    def turn_typing_on(self, facebook_id):
        self.send_sender_action(facebook_id, "typing_on")

    def get_user_token_from_optin_request(self, json):
        return json['messaging'][0]['optin']['ref']

    def turn_typing_off(self, facebook_id):
        self.send_sender_action(facebook_id, "typing_off")

    def get_application_user_by_facebook_id(self, facebook_id):
        user = IntentParser.initialize_user(facebook_id, True)
        # if not user.name:
            # user.name = self.get_user_first(facebook_id)
            # user.surname = self.get_user_last(facebook_id)
            #
        return user