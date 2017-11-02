from GroningerAPI.conversationdata import ConversationData
from GroningerAPI.models import Conversation, User


class IntentParser:
    def __init__(self):
        pass


    def find_something(self, data, conversation):
        parameters = ConversationData(conversation.conversation_params)
        parameters.film_date = data.get('date')
        parameters.subject = data.get('subject')
        conversation.conversation_params = parameters.to_json()


    def find_movie(self, data, conversation):
        parameters = ConversationData(conversation.conversation_params)
        parameters.film_date = data.get('date')
        parameters.subject = data.get('subject')
        conversation.conversation_params = parameters.to_json()

    def recommend_something(self, data, conversation):
        parameters = ConversationData(conversation.conversation_params)
        parameters.genre = data.get('genre')
        parameters.subject = data.get('subject')
        conversation.conversation_params = parameters.to_json()

    def recommend_movie(self, data, conversation):
        parameters = ConversationData(conversation.conversation_params)
        parameters.subject = data.get('subject')
        parameters.genre = data.get('genre')
        parameters.film_date = data.get('date')
        conversation.conversation_params = parameters.to_json()

    def reserve_something(self, data, conversation):
        parameters = ConversationData(conversation.conversation_params)
        parameters.film_date = data.get('date')
        parameters.subject = data.get('subject')
        parameters.number_of_persons = data.get('number')
        conversation.conversation_params = parameters.to_json()

    def find_parking(self, data, conversation):
        parameters = ConversationData(conversation.conversation_params)
        parameters.film_date = data.get('date')
        conversation.conversation_params = parameters.to_json()

    def review(self, data, conversation):
        parameters = ConversationData(conversation.conversation_params)
        parameters.review_sentiment = data.get('sentiment')
        conversation.conversation_params = parameters.to_json()

    def find_restaurant(self, data, conversation):
        parameters = ConversationData(conversation.conversation_params)
        parameters.number_of_persons = data.get('number')
        parameters.subject = data.get('subject')
        conversation.conversation_params = parameters.to_json()

    def reserve_restaurant(self, data, conversation):
        parameters = ConversationData(conversation.conversation_params)
        parameters.film_date = data.get('date')
        parameters.subject = data.get('subject')
        parameters.number_of_persons = data.get('number')
        conversation.conversation_params = parameters.to_json()

    def recommend_book(self, data, conversation):
        parameters = ConversationData(conversation.conversation_params)
        parameters.book_author = data.get('author')
        parameters.genre = data.get('genre')
        conversation.conversation_params = parameters.to_json()

    def information(self, data, conversation):
        parameters = ConversationData(conversation.conversation_params)
        parameters.subject = data.get('subject')
        conversation.conversation_params = parameters.to_json()

    def price_information(self, data, conversation):
        parameters = ConversationData(conversation.conversation_params)
        parameters.start_time = data.get('start_time')
        parameters.end_time = data.get('end')
        parameters.subject = data.get('subject')
        parameters.duration = data.get('duration')
        conversation.conversation_params = parameters.to_json()

    @staticmethod
    def initialize_user(user_token, facebook):
        conversation = None
        if not facebook:
            user = User.objects.get_or_create(session_id=user_token)
        else:
            user = User.objects.get_or_create(facebook_id=user_token)

        if not conversation:
            conversation = Conversation(user=user)
            conversation.save(force_insert=True)
        else:
            conversation = Conversation.objects.order_by("-time_stamp").first()

        return conversation

