import sys
import time
from datetime import datetime

import pytz

from . import settings
from .service import Service


class AdhanBot(object):
    def __init__(self, subscribers=None):
        self.subscribers = subscribers or []
        self.service = Service()

    @property
    def current_time(self):
        try:
            return datetime.now(pytz.timezone(settings.TIMEZONE))
        except pytz.exceptions.UnknownTimeZoneError:
            print("UnknownTimeZoneError")
            sys.exit(1)

    def sleep_for(self, seconds):
        time.sleep(seconds)

    def notify_subscribers(self, salah):
        for subscriber in self.subscribers:
            data = {"channel": subscriber, "salah": salah}
            self.service.slack.post(data)

    def get_time_diff_between_now_and_salah(self, salah, adhan_timings):
        current_time = self.current_time

        current_datetime = datetime.strptime(
            "{}:{}".format(current_time.hour, current_time.minute), "%H:%M"
        )
        salah_datetime = datetime.strptime(adhan_timings[salah], "%H:%M")

        return (salah_datetime - current_datetime).total_seconds()

    def call_to_prayer(self, salah):
        time_diff_in_seconds = self.get_time_diff_between_now_and_salah(
            salah, self.service.aladhan.adhan_timings
        )

        if time_diff_in_seconds >= 0:
            self.sleep_for(time_diff_in_seconds)
            self.notify_subscribers(salah)

    def sleep_on_exempted_days(self):
        current_time = self.current_time
        if current_time.weekday() in settings.DAYS_OF_THE_WEEK_EXEMPTED:
            self.sleep_for((24 - current_time.hour) * 3600)
            return self.sleep_on_exempted_days()

    def run(self):
        while True:
            try:
                self.sleep_on_exempted_days()
                for salah in settings.SALAWAT:
                    self.call_to_prayer(salah)

                self.sleep_for(settings.NIGHT_SLEEP_IN_SECONDS)
            except Exception as e:
                self.service.sendgrid.notify_of_error(e)
