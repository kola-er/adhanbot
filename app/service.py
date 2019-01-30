import json
import math
import random

import requests
import sendgrid

from . import settings


class AlAdhanAPIWrapper(object):
    """
    Wrapper for the AlAdhan API

    Add more methods for the API endpoints as necessary
    """

    def __init__(self):
        self.api_url = "{}?latitude={}&longitude={}&timezonestring={}&method={}".format(
            settings.ADHAN_API_BASE_URL,
            settings.LATITUDE,
            settings.LONGITUDE,
            settings.TIMEZONE,
            settings.METHOD,
        )
        self.service = Service(service_classes=[SendGridAPIWrapper])

    def get_adhan_timings(self):
        aladhan_response = requests.get(self.api_url)
        if aladhan_response.status_code != 200:
            self.service.sendgrid.notify_of_error(service="AlAdhan API")
            return settings.DEFAULT_ADHAN_TIMINGS
        return aladhan_response.json()["data"]["timings"]


class AlQuranAPIWrapper(object):
    """
    Wrapper for the AlQuran API

    Add more methods for the API endpoints as necessary
    """

    def __init__(self):
        self.api_url = (
            "http://api.alquran.cloud/ayah/{}/editions/quran-uthmani,en.sahih"
        )

    def get_random_quranic_verse(self):
        random_verse = int(math.ceil(random.random() * 6236))
        return self.get_quranic_verse(random_verse)

    def get_quranic_verse(self, verse):
        response = requests.get(self.api_url.format(verse))

        if response.status_code == 200:
            return response.json()


class SendGridAPIWrapper(object):
    """
    Wrapper for the SendGrid API

    Add more methods for the API endpoints as necessary
    """

    def __init__(self):
        self.api_key = settings.SENDGRID_API_KEY
        self.to_email = settings.TO_EMAIL
        self.from_email = settings.FROM_EMAIL

    def send_mail(self, body):
        sg = sendgrid.SendGridAPIClient(apikey=self.api_key)
        data = {
            "personalizations": [
                {
                    "to": [{"email": self.to_email}],
                    "subject": "AdhanBot Critical Report",
                }
            ],
            "from": {"email": self.from_email},
            "content": [{"type": "text/plain", "value": body}],
        }

        return sg.client.mail.send.post(request_body=data)

    def notify_of_error(self, service=None, error_message=None):
        """
        Note that this method is special and does not translate in any sense
        to any of SendGrid existing API endpoints
        """

        message = "Something doesn't seem to be right!"
        if service:
            message = "{} seems to be down!".format(service)

        if error_message:
            message += "\nError Message: {}".format(error_message)

        self.send_mail(message)


class SlackWebhookAPIWrapper(object):
    """
    Wrapper for the Slack Incoming Webhook API
    """

    def __init__(self):
        self.webhook_url = settings.SLACK_WEBHOOK_URL
        self.service = Service(service_classes=[AlQuranAPIWrapper, SendGridAPIWrapper])

    def compose_attachment_fields(self, prayer):
        fields = []
        if prayer == "Fajr":
            fields = [
                {
                    "title": "Dua upon waking up in the morning",
                    "value": settings.FAJR_DUA,
                },
                {"value": settings.FAJR_DUA_TRANSLATION},
            ]
        elif prayer == "Isha":
            fields = [
                {
                    "title": "Dua before going to bed at night",
                    "value": settings.DUA_BEFORE_NIGHT_SLEEP,
                }
            ]
        else:
            quranic_verse = self.service.alquran.get_random_quranic_verse()
            if quranic_verse:
                title = "{} {}:{}     [{} - {}] {}".format(
                    quranic_verse["data"][1]["surah"]["name"],
                    quranic_verse["data"][1]["surah"]["number"],
                    quranic_verse["data"][1]["numberInSurah"],
                    quranic_verse["data"][1]["surah"]["englishName"],
                    quranic_verse["data"][1]["surah"]["englishNameTranslation"],
                    quranic_verse["data"][1]["edition"]["name"],
                )
                value = "{}\n{}\nPLEASE, read immediate verses for context https://quran.com/{}/{}".format(
                    quranic_verse["data"][0]["text"],
                    quranic_verse["data"][1]["text"],
                    quranic_verse["data"][1]["surah"]["number"],
                    quranic_verse["data"][1]["numberInSurah"],
                )

                fields = [{"title": title, "value": value}]

        return fields

    def compose_payload(self, data):
        channel = data.get("channel")
        prayer = data.get("prayer") or ""

        if not channel:
            raise Exception(
                "A notification was stopped from going to Slack because the channel wasn't set"
            )

        return json.dumps(
            {
                "channel": "#{}".format(channel),
                "attachments": [
                    {
                        "color": "#36a64f",
                        "pretext": "{} {}".format(settings.REMINDER_TEXT, data.get("notifier")),
                        "title": prayer,
                        "text": settings.CONSTANT_REMINDER,
                        "fields": self.compose_attachment_fields(prayer),
                    }
                ],
            }
        )

    def post(self, data):
        slack_response = requests.post(
            self.webhook_url, data={"payload": self.compose_payload(data)}
        )

        if slack_response.status_code != 200:
            self.service.sendgrid.notify_of_error(service="Slack Webhook")


class Service(object):
    """
    Third-party API service accessible on-demand

    Its initialization defaults to a registry of services currently available
    """

    def __init__(self, service_classes=None):
        service_classes = service_classes or [
            SlackWebhookAPIWrapper,
            AlAdhanAPIWrapper,
            AlQuranAPIWrapper,
            SendGridAPIWrapper,
        ]

        for service_class in service_classes:
            if service_class == SlackWebhookAPIWrapper:
                self.slack = SlackWebhookAPIWrapper()
            elif service_class == AlAdhanAPIWrapper:
                self.aladhan = AlAdhanAPIWrapper()
            elif service_class == AlQuranAPIWrapper:
                self.alquran = AlQuranAPIWrapper()
            elif service_class == SendGridAPIWrapper:
                self.sendgrid = SendGridAPIWrapper()
