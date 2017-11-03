from random import randint

from GroningerAPI.models import Movie


class MovieFinder(object):
    def __init__(self, subject=None, genre=None, datetime=None):
        self.subject = subject
        self.genre = genre
        self.datetime = datetime

    def find_best_time(self):
        # todo
        return '2017-11-03T16:00:00.00+01:00'

    def recommend_movie(self):
        return 'Misfits', '2017-11-03T16:00:00.00+01:00', 'zaal 5'
        # if self.subject:
        #     return Movie.objects.filter(name=self.subject).order_by('?').first()
        # elif self.genre:
        #     return Movie.objects.filter(genre=self.genre).order_by('?').first()
        # else:
        #     return Movie.objects.order_by('?').first()

    def reserve(self, number, user):
        # todo
        return randint(0, 1) == 1