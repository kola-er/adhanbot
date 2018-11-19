# encoding: utf-8

import os
import json

import dotenv

dotenv.load()

# Methods identifying various schools of thought about how to compute the timings
# 0 - Shia Ithna-Ashari
# 1 - University of Islamic Sciences, Karachi
# 2 - Islamic Society of North America (ISNA)
# 3 - Muslim World League (MWL)
# 4 - Umm al-Qura, Makkah
# 5 - Egyptian General Authority of Survey
# 7 - Institute of Geophysics, University of Tehran
METHOD = 3

# Location
LATITUDE = 6.4531
LONGITUDE = 3.3958
TIMEZONE = "Africa/Lagos"

# Slack
SLACK_WEBHOOK_URL = (dotenv.get("SLACK_WEBHOOK_URL") or "").strip()
SLACK_CHANNELS = [i.strip() for i in (dotenv.get("SLACK_CHANNELS") or "").split(",")]

# Email support
SENDGRID_API_KEY = (dotenv.get("SENDGRID_API_KEY") or "").strip()
TO_EMAIL = (dotenv.get("TO_EMAIL") or "").strip()
FROM_EMAIL = "support@adhanbot.com"

# Adhan info source
ADHAN_API_BASE_URL = "http://api.aladhan.com/timings"
DEFAULT_ADHAN_TIMINGS = {
    "Fajr": "05:30",
    "Dhuhr": "13:15",
    "Asr": "16:15",
    "Maghrib": "19:05",
    "Isha": "20:20",
}

# Constants
CONSTANT_REMINDER = "The Success you search for calls you FIVE times a day!"
DUA_BEFORE_NIGHT_SLEEP = "Remember to recite ayat-ul-kurisiy, surat-ul-ihklas, surat-ul-falaq, surat-u-nas before going to bed. May Allah forgive us our sins, overlook our shortcomings and have mercy on us. Aameen"
FAJR_DUA = (
    "الْحَمْدُ لِلَّهِ الَّذِي أَحْيَانَا بَعْدَ مَا أَمَاتَنَا وَإِلَيْهِ النُّشُورُ"
)
FAJR_DUA_TRANSLATION = "All praise be to Allah, who gave us life after killing us (sleep is a form of death) and to Him we will be raised and returned"
NIGHT_SLEEP_IN_SECONDS = 28800
REMINDER_TEXT = "...حي على الصلاة...حي على الفلاح"

# Automatically sets variables using the key-value pair of the `config.json` file in the project root directory
# NOTE: This overwites the values of any variables set above if keys of exact names (case-insensitive) exist in the file
try:
    config_file_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json"
    )
    with open(config_file_path) as f:
        for k, v in json.load(f).items():
            exec(k.upper() + "=v")
except (IOError, ValueError) as e:
    pass
