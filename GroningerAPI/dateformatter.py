class DateFormatter(object):
    def __init__(self, date):
        self.date = date

    def __str__(self):
        # todo
        if type(self.date) is dict:
            return self.date['value']
        else:
            return self.date
