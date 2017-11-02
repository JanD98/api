from GroningerAPI.models import Conversation, User


class Intent_Parser:
    def __int__(self):
        pass

    def yes(self, data):
        user_id = data.get("userId")
        conversation = self.initialize_user(user_id)
        return data.get("subject", "0")

    def no(self):
        pass

    def find_something(self):
        pass

    def find_movie(self):
        pass

    def recommend_something(self):
        pass

    def recommend_movie(self):
        pass

    def recommend_other(self):
        pass

    def accept_recommend(self):
        pass

    def reserve_something(self):
        pass

    def find_parking(self):
        pass

    def review(self):
        pass

    def request_human(self):
        pass

    def find_restaurant(self):
        pass

    def reserve_restaurant(self):
        pass

    def recommend_book(self):
        pass

    def information(self):
        pass

    def price_information(self):
        pass

    def initialize_user(self, id):
        user = User.objects.filter(user_id=id)
        conversation = None
        if not user:
            user = User(user_id=id)
            user.save()
            conversation = ""
            #convo aanmaken
        else:
            conversation = ""
            #laatste convo ophalen van user

        return conversation
