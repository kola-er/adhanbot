from datetime import datetime

import pytz

from . import settings


def clean_data(data):
    cleaned_data = data

    # Add more cases to handle other data types
    if isinstance(data, str):
        cleaned_data = data.strip().lower()
    elif isinstance(data, list):
        cleaned_data = [item.strip().lower() for item in data]

    return cleaned_data


def current_datetime():
    return datetime.now(pytz.timezone(settings.TIMEZONE))


def parse_hour_and_min_to_datetime(hour, minute):
    return datetime.strptime("{}:{}".format(hour, minute), "%H:%M")
