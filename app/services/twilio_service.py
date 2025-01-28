from decouple import config
from twilio.rest import Client

class TwilioService:
    def __init__(self):
        self.client = Client(
            config("TWILIO_ACCOUNT_SID"), 
            config("TWILIO_AUTH_TOKEN")
        )
        self.from_phone = config("TWILIO_FROM_PHONE")

    def send_sms(self, to_phone, message):
        try:
            message = self.client.messages.create(
                body=message,
                from_=self.from_phone,
                to=to_phone
            )
            print(f"SMS envoyé avec succès. SID: {message.sid}")
        except Exception as e:
            print(f"Erreur lors de l'envoi du SMS: {e}")
