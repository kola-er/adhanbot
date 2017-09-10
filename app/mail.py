import sendgrid

from . import settings

def send_mail(message):
    sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)
    data = {
      'personalizations': [
        {
          'to': [
            {
              'email': settings.TO_EMAIL
            }
          ],
          'subject': 'AdhanBot Critical Report'
        }
      ],
      'from': {
        'email': settings.FROM_EMAIL
      },
      'content': [
        {
          'type': 'text/plain',
          'value': message
        }
      ]
    }

    return sg.client.mail.send.post(request_body=data)
