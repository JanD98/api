from facepy import GraphAPI

from GroningerAPI.intent_parser import IntentParser


class Facebook:
    graph = ""
    api_token = "EAAEGVfJehVABADQboSAmxsCBb64Drfs6JQ8NaOJ8ogD68bIZBTPapSZAqZApZBSSvkhbcddhF7srS5Hh1aAuddKlQRZB2UyqHs3ZCs6lYjK4ySlJb2DguxnsvczIaMh7ZC0ZBvN1I4mHoFGEwzNpkpegda9slYK1vFZAjKOGDJeio93033c2WTLZAt"

    def __init__(self):
        self.graph = GraphAPI(self.api_token)

    def get_user_id_form_message(self, json):
        return json['messaging'][0]['sender']['id']

    def get_message_text(self, json):
        return json['messaging'][0]['message']['text']

    def get_user_data(self, facebook_id):
        return {'profile_pic': 'https://scontent.xx.fbcdn.net/v/t1.0-1/23031354_103638190408641_2437891292324580905_n.jpg?oh=63b362fc756b2e733336e95f0a4625dc&oe=5A7175B9', 'locale': 'nl_NL', 'gender': 'male', 'id': '103636133742180',
                'headers': {'Cache-Control': 'private, no-cache, no-store, must-revalidate', 'Connection': 'keep-alive', 'Content-Type': 'application/json; charset=UTF-8', 'x-fb-rev': '3422078', 'Content-Encoding': 'gzip', 'Vary': 'Accept-Encoding', 'Pragma': 'no-cache',
                            'Date': 'Thu, 02 Nov 2017 11:04:19 GMT', 'x-fb-trace-id': 'A7RTUulgFML', 'ETag': '"a76ec7f2451f48af7bb25030d25ee3b976d9e172"', 'Access-Control-Allow-Origin': '*', 'facebook-api-version': 'v2.10',
                            'X-FB-Debug': 'mgeNOpGAu/DOQZ+Pm/sFEXbvhoIEjm0RTGN6xVMRjWxZa+9q+DxOGgq2zja5bBASsNF7Df5rfYb9qLr7PC6dwQ==', 'Content-Length': '234', 'Expires': 'Sat, 01 Jan 2000 00:00:00 GMT'}, 'last_name': 'Wouters', 'first_name': 'Ton', 'timezone': 1}
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
        user = IntentParser.get_conversation_by_token(facebook_id, True)
        # if not user.name:
        # user.name = self.get_user_first(facebook_id)
        # user.surname = self.get_user_last(facebook_id)
        #
        return user
