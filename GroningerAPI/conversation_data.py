import json


class ConversationData:
    film_name = None
    film_date = None
    film_time = None
    genre = None
    film_location = None
    number_of_persons = None
    booking_date = None
    booking_time = None
    review_sentiment = None
    book_author = None
    start_time = None
    end_time = None
    subject = None
    duration = None

    def __init__(self, j_object):
        self.__dict__ = json.loads(j_object)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
