import datetime

from dateutil.relativedelta import relativedelta


def calculate_age(date):
    return relativedelta(datetime.datetime.now(), date).years
