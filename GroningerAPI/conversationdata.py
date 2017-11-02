from django.core.serializers import json


class ConversationData:

    film_name = None
    film_date = None
    film_time = None
    film_genre = None
    film_subject = None
    film_location = None
    number_of_persons = None
    booking_date = None
    booking_time = None

    def __init__(self, j_object):
        self.__dict__ = json.loads(j_object)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
