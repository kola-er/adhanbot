import dotenv

dotenv.load()

"""
Methods identifying various schools of thought about how to compute the timings
0 - Shia Ithna-Ashari
1 - University of Islamic Sciences, Karachi
2 - Islamic Society of North America (ISNA)
3 - Muslim World League (MWL)
4 - Umm al-Qura, Makkah
5 - Egyptian General Authority of Survey
7 - Institute of Geophysics, University of Tehran
"""
METHOD = 3

LATITUDE = 6.4531
LONGITUDE = 3.3958
TIMEZONE = 'Africa/Lagos'

# Slack webhook url
SLACK_WEBHOOK_URL= dotenv.get('SLACK_WEBHOOK_URL', '')
SLACK_CHANNEL = dotenv.get('SLACK_CHANNEL', '')

# Email support
SENDGRID_API_KEY = dotenv.get('SENDGRID_API_KEY', '')
TO_EMAIL = dotenv.get('TO_EMAIL', '')
FROM_EMAIL = 'support@adhanbot.com'

"""
Limit number of salah to get notification for.

Example: SALAWAT = ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']
"""
SALAWAT = ['Dhuhr', 'Asr']

"""
Days of the week to be exempted for notifications.

0 - Monday
1 - Tuesday
2 - Wednesday
3 - Thursday
4 - Friday
5 - Saturday
6 - Sunday

Example: DAYS_OF_THE_WEEK_EXEMPTED = [0, 1, 2]
"""
DAYS_OF_THE_WEEK_EXEMPTED = [5, 6]

# Adhan data source
ADHAN_API_BASE_URL = 'http://api.aladhan.com/timings'

# Constants
CONSTANT_REMINDER = 'The Success you search for calls you FIVE times a day!'
DUA_BEFORE_NIGHT_SLEEP = 'Remember to recite ayat-ul-kurisiy, surat-ul-ihklas, surat-ul-falaq, surat-u-nas before going to bed. May Allah forgive us our sins, overlook our shortcomings and have mercy on us. Aameen'
FAJR_DUA = 'الْحَمْدُ لِلَّهِ الَّذِي أَحْيَانَا بَعْدَ مَا أَمَاتَنَا وَإِلَيْهِ النُّشُورُ'
FAJR_DUA_TRANSLATION = 'All praise be to Allah, who gave us life after killing us (sleep is a form of death) and to Him we will be raised and returned'
NIGHT_SLEEP_IN_SECONDS = 32000
REMINDER_TEXT = '...حي على الصلاة...حي على الفلاح'
