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
        return "Heeft u een tijdstip in gedachte?"

    def find_movie(self, data, conversation):
        parameters = ConversationData(conversation.conversation_params)
        parameters.film_date = data.get('date')
        parameters.subject = data.get('subject')
        conversation.conversation_params = parameters.to_json()
        return "Wanneer zou je naar de film willen?"

    def recommend_something(self, data, conversation):
        parameters = ConversationData(conversation.conversation_params)
        parameters.genre = data.get('genre')
        parameters.subject = data.get('subject')
        conversation.conversation_params = parameters.to_json()
        return "Misschien dat deze films iets zijn? : [...show films...]"

    def recommend_movie(self, data, conversation):
        parameters = ConversationData(conversation.conversation_params)
        parameters.subject = data.get('subject')
        parameters.genre = data.get('genre')
        parameters.film_date = data.get('date')
        conversation.conversation_params = parameters.to_json()
        return "Wanneer zou je naar de film willen gaan?"

    def reserve_something(self, data, conversation):
        parameters = ConversationData(conversation.conversation_params)
        parameters.film_date = data.get('date')
        parameters.subject = data.get('subject')
        parameters.number_of_persons = data.get('number')
        conversation.conversation_params = parameters.to_json()
        return "Hoe zou u de kaartjes willen ontvangen?"

    def find_parking(self, data, conversation):
        parameters = ConversationData(conversation.conversation_params)
        parameters.film_date = data.get('date')
        conversation.conversation_params = parameters.to_json()
        return "Hoelaat bent u van plan te komen?"

    def review(self, data, conversation):
        parameters = ConversationData(conversation.conversation_params)
        parameters.review_sentiment = data.get('sentiment')
        conversation.conversation_params = parameters.to_json()
        return "Bedankt voor uw feedback"

    def find_restaurant(self, data, conversation):
        parameters = ConversationData(conversation.conversation_params)
        parameters.number_of_persons = data.get('number')
        parameters.subject = data.get('subject')
        conversation.conversation_params = parameters.to_json()
        return "Wanneer bent u van plan te komen?"

    def reserve_restaurant(self, data, conversation):
        parameters = ConversationData(conversation.conversation_params)
        parameters.film_date = data.get('date')
        parameters.subject = data.get('subject')
        parameters.number_of_persons = data.get('number')
        conversation.conversation_params = parameters.to_json()
        return "Dat kan. De reservering is gedaan."

    def recommend_book(self, data, conversation):
        parameters = ConversationData(conversation.conversation_params)
        parameters.book_author = data.get('author')
        parameters.genre = data.get('genre')
        conversation.conversation_params = parameters.to_json()
        return "Dat kan. Hier is het aanbod:"

    def information(self, data, conversation):
        parameters = ConversationData(conversation.conversation_params)
        parameters.subject = data.get('subject')
        conversation.conversation_params = parameters.to_json()
        "[De geleverde informatie]"

    def price_information(self, data, conversation):
        parameters = ConversationData(conversation.conversation_params)
        parameters.start_time = data.get('start_time')
        parameters.end_time = data.get('end')
        parameters.subject = data.get('subject')
        parameters.duration = data.get('duration')
        conversation.conversation_params = parameters.to_json()
        return "De prijs is [price]"

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

