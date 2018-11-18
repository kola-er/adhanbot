from app import settings
from app.adhan import AdhanBot

if __name__ == "__main__":
    adhan = AdhanBot(subscribers=settings.SLACK_CHANNELS)
    adhan.run()
