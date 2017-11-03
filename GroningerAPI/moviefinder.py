from random import randint

from GroningerAPI.models import Movie


class MovieFinder(object):
    def __init__(self, subject=None, genre=None, datetime=None):
        self.subject = subject
        self.genre = genre
        self.datetime = datetime

    def find_best_time(self):
        # todo
        return '2017-11-06T20:00:00'

    def recommend_movies(self):
        return 'Pulp Fiction'
        # if self.genre & self.subject:
        #     return Movie.objects.filter(genre=self.genre, subject=self.subject).order_by('?').first()
        # elif self.genre:
        #     return Movie.objects.filter(genre=self.genre).order_by('?').first()
        # elif self.subject:
        #     return Movie.objects.filter(subject=self.subject).order_by('?').first()
        # else:
        #     return Movie.objects.order_by('?').first()

    def reserve(self, number, user):
        # todo
        return randint(0, 1) == 1