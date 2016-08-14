from datetime import datetime
import json, os, signal, sys, time

from daemonize import Daemonize
import pytz, requests

import mail, settings


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

def get_time_diff_between_now_and_salah(salah, adhan_timings):
    current_time = pytz.timezone(settings.TIMEZONE).localize(datetime.now())
    current_datetime = datetime.strptime('%d:%d' % (current_time.hour, current_time.minute), '%H:%M')
    salah_datetime = datetime.strptime(adhan_timings[salah], '%H:%M')

    return (salah_datetime - current_datetime).total_seconds()

def display_help_message():
    return """
    Usage: python -m adhanbot.app.adhan <command>

    <command>
    start: Run program
    stop: Kill running instance of the program
    """

def main():
    while True:
        aladhan_response = requests.get(get_adhan_api_endpoint())
        if aladhan_response.status_code != 200:
            mail.send_mail('AlAdhan API is down!')
            sys.exit(1)

        adhan_timings = aladhan_response.json()['data']['timings']
        for salah in settings.SALAWAT:
            time_diff_in_seconds = get_time_diff_between_now_and_salah(salah, adhan_timings)

            if time_diff_in_seconds >= 0:
                time.sleep(time_diff_in_seconds);
                if requests.post(settings.SLACK_WEBHOOK_URL, data={'payload': form_slack_payload(salah, settings.SLACK_CHANNEL)}).status_code != 200:
                    mail.send_mail('Slack Webhook seems to be down!')

        time.sleep(settings.NIGHT_SLEEP_IN_SECONDS)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'start':
            daemon = Daemonize(app='adhanbot', pid=settings.PID_FILE, action=main)
            daemon.start()
        elif sys.argv[1] == 'stop':
            if os.path.isfile(settings.PID_FILE):
                with open(settings.PID_FILE, 'r') as f:
                    os.kill(int(f.read()), signal.SIGTERM)
        else:
            print(display_help_message())
    else:
        print(display_help_message())
