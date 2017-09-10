import json
import os
import signal
import sys
import time
from datetime import datetime

import pytz
import requests

from . import mail, settings


def form_slack_payload(salah, slack_channel):
    return json.dumps({
        'channel': '#%s' % slack_channel,
        'attachments': [{
            'color': '#36a64f',
            'pretext': '%s <!channel>' % settings.REMINDER_TEXT,
            'title': salah,
            'text': settings.CONSTANT_REMINDER,
            'fields': get_attachment_field_content(salah)
        }]
    })

def get_attachment_field_content(salah):
    if salah == 'Fajr':
        field_contents = [
            {
                'title': 'Dua upon waking up in the morning',
                'value': settings.FAJR_DUA
            },
            {
                'value': settings.FAJR_DUA_TRANSLATION
            }
        ]
    elif salah == 'Isha':
        field_contents = [
            {
                'title': 'Dua before going to bed at night',
                'value': settings.DUA_BEFORE_NIGHT_SLEEP
            }
        ]
    else:
        field_contents = []

    return field_contents

def get_adhan_api_endpoint():
    return '{}?latitude={}&longitude={}&timezonestring={}&method={}'.format(
        settings.ADHAN_API_BASE_URL,
        settings.LATITUDE,
        settings.LONGITUDE,
        settings.TIMEZONE,
        settings.METHOD
    )

def get_current_time():
    try:
        return datetime.now(pytz.timezone(settings.TIMEZONE))
    except pytz.exceptions.UnknownTimeZoneError:
        print('UnknownTimeZoneError')
        sys.exit(1)

def sleep_on_exempted_days():
    current_time = get_current_time()
    if current_time.weekday() in settings.DAYS_OF_THE_WEEK_EXEMPTED:
        time.sleep((24 - current_time.hour) * 3600)
        return sleep_on_exempted_days()

def get_time_diff_between_now_and_salah(salah, adhan_timings):
    current_time = get_current_time()

    current_datetime = datetime.strptime('%d:%d' % (current_time.hour, current_time.minute), '%H:%M')
    salah_datetime = datetime.strptime(adhan_timings[salah], '%H:%M')

    return (salah_datetime - current_datetime).total_seconds()

def main():
    while True:
        # sleep_on_exempted_days()
        aladhan_response = requests.get(get_adhan_api_endpoint())
        if aladhan_response.status_code != 200:
            mail.send_mail('AlAdhan API is down!')
            sys.exit(1)

        adhan_timings = aladhan_response.json()['data']['timings']
        for salah in settings.SALAWAT:
            # time_diff_in_seconds = get_time_diff_between_now_and_salah(salah, adhan_timings)

            # if time_diff_in_seconds >= 0:
            # time.sleep(time_diff_in_seconds);
            if requests.post(settings.SLACK_WEBHOOK_URL, data={'payload': form_slack_payload(salah, settings.SLACK_CHANNEL)}).status_code != 200:
                mail.send_mail('Slack Webhook seems to be down!')

        time.sleep(settings.NIGHT_SLEEP_IN_SECONDS)


if __name__ == '__main__':
    main()
