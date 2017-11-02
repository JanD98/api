from random import randint

class MovieFinder(object):
    def __init__(self, subject=None, genre=None, datetime=None):
        self.subject = subject
        self.genre = genre
        self.datetime = datetime

    def find_best_time(self):
        # todo
        return '2017-11-06T20:00:00'

    def recommend_movies(self):
        # todo
        return ['Pulp Fiction', 'Reservoir Dogs', 'Hateful Eight'][:randint(0, 3)]

    def reserve(self, number, user):
        # todo
        return randint(0, 1) == 1