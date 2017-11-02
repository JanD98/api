from GroningerAPI.models import Conversation, User


class IntentParser:
    def __int__(self):
        pass

    def yes(self, data, conversation):
        pass

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

    @staticmethod
    def initialize_user(user_id):
        conversation = None
        user = User.objects.get_or_create(user_id=user_id)

        if not conversation:
            conversation = Conversation(user=user)
            conversation.save(force_insert=True)
        else:
            conversation = Conversation.objects.order_by("-time_stamp").first()

        return conversation

