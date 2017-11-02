from facepy import GraphAPI


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
