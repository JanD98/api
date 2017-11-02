class Facebook:
    def __int__():
        pass

    def get_user_id_form_message(self, json):
        return json['messaging'][0]['sender']['id']

    def get_message_text(self, json):
        return json['messaging'][0]['message']['text']
