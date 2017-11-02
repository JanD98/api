from random import randint

class ParkingFinder(object):
    def __init__(self, datetime=None):
        self.datetime = datetime

    def expected_spots(self):
        # todo
        return max(0, randint(-30, 200))