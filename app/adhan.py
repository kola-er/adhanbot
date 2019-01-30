import sys
import time

from . import settings
from .service import Service
from . import utils


class AdhanBot(object):
    """
    Bot model that reminds subscribed Muslims of the five daily islamic prayers
    at the exact time of each based on some settings like location e.t.c.

    method `run` kicks off the notification
    """

    def __init__(self, subscribers=None):
        self.subscribers = subscribers or []
        self.adhan_timings = None
        self.service = Service()

    def notify_subscribers(self, prayer):
        day_identifier = (
            "weekend" if utils.current_datetime().weekday() in [5, 6] else "weekday"
        )

        for subscriber in self.subscribers:
            subscriber_preferences = settings.SUBSCRIBERS_PREFERENCES.get(subscriber) or {}
            subscriber_excluded_prayer = utils.clean_data(
                (
                    subscriber_preferences.get("exclude") or {}
                ).get(day_identifier)
                or []
            )

            if prayer.lower() in subscriber_excluded_prayer:
                continue

            self.service.slack.post({
                "channel": subscriber,
                "prayer": prayer,
                "notifier": subscriber_preferences.get("broadcast_notifier") or "<!channel>"
            })

    def get_time_diff_between_now_and_prayer(self, prayer):
        current_datetime = utils.current_datetime()
        current_datetime = utils.parse_hour_and_min_to_datetime(
            current_datetime.hour, current_datetime.minute
        )
        prayer_datetime = utils.parse_hour_and_min_to_datetime(
            *self.adhan_timings[prayer].split(":")
        )

        return (prayer_datetime - current_datetime).total_seconds()

    def call_to_prayer(self, prayer):
        time_diff_in_seconds = self.get_time_diff_between_now_and_prayer(prayer)
        if time_diff_in_seconds >= 0:
            time.sleep(time_diff_in_seconds)
            self.notify_subscribers(prayer)

    def sleep_at_night(self):
        n = settings.NIGHT_SLEEP_IN_SECONDS + self.get_time_diff_between_now_and_prayer("Isha")
        if n > 0:
            time.sleep(n)

    def run(self):
        """
        Method that kicks off the notification process and ensures it's continuous
        unless the timezone is unknown
        """

        while True:
            try:
                self.adhan_timings = self.service.aladhan.get_adhan_timings()
                for prayer in ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]:
                    self.call_to_prayer(prayer)

                self.sleep_at_night()
            except utils.pytz.exceptions.UnknownTimeZoneError as e:
                self.service.sendgrid.notify_of_error(
                    "UnknownTimeZoneError: {}".format(e)
                )
                sys.exit(1)
            except Exception as e:
                self.service.sendgrid.notify_of_error(e)
