import datetime

class DateFormatter(object):

    months = ["januari", "februari", "maart", "april", "mei", "juni", "juli", "augustus", "september", "oktober",
              "november", "december"]
    days = ["maandag", "dinsdag", "woensdag", "donderdag", "vrijdag", "zaterdag", "zondag"]
    times = ["'s ochtends", "'s middags", "'s avonds", "'s nachts"]

    def __init__(self, date):
        if type(date) is dict:
            date = date['value']
        if isinstance(date, datetime.datetime):
            self.date = date
        else:
            self.date= datetime.datetime.strptime(date[:19], "%Y-%m-%dT%H:%M:%S")

    def __str__(self):
        if type(self.date) is dict:
            return self.calculate_result(self.date['value'])
        else:
            return self.calculate_result(self.date)

    def hour_to_prefix(self, date_time):
        hour = date_time.time().hour
        if hour > 18:
            return self.times[2]
        elif hour > 12:
            return self.times[1]
        elif hour > 6:
            return self.times[0]
        else:
            return self.times[3]

    def date_to_weekday(self, date_time):
        return self.days[date_time.date().weekday()]

    def date_to_month_string(self, date_time):
        return self.months[date_time.date().month-1]

    def date_to_hourstamp(self, date_time):
        return date_time.strftime('%I:%M')

    def calculate_result(self, date_time):
        delta = date_time.date() - datetime.datetime.now().date()
        if delta.days > 14:
            return str(date_time.date().day) + " " + self.date_to_month_string(date_time) + " om " + self.date_to_hourstamp(date_time)
        elif delta.days > 7:
            return "volgende week " + self.date_to_weekday(date_time) + " om " + self.date_to_hourstamp(date_time) + " " + self.hour_to_prefix(date_time)
        elif delta.days == 1:
            return "morgen om " + self.date_to_hourstamp(date_time) + " " + self.hour_to_prefix(date_time)
        elif delta.days == 0:
            return "om " + self.date_to_hourstamp(date_time) + " " + self.hour_to_prefix(date_time)
        else:
            return self.date_to_weekday(date_time) + " om " + self.date_to_hourstamp(date_time) + " " + self.hour_to_prefix(date_time)

