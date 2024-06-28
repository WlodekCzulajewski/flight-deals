from twilio.rest import Client
import requests
import smtplib
import os

TWILIO_SID = os.environ.get("TWI_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWI_AUTH_TOKEN")
TWILIO_VIRTUAL_NUMBER = "+12072557763"
TWILIO_VERIFIED_NUMBER = os.environ.get("TWI_VER_NUMBER")

SHEETY_USERS_ENDPOINT = "https://api.sheety.co/148f13651d8fa3e988f6ff238d52e333/flightDeals/users"
MY_EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("EMAIL_PASSWORD")


class NotificationManager:

    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    def send_sms(self, message):
        message = self.client.messages.create(
            body=message,
            from_=TWILIO_VIRTUAL_NUMBER,
            to=TWILIO_VERIFIED_NUMBER,
        )
        # Prints if successfully sent.
        print(message.sid)

    def send_emails(self, message):
        response = requests.get(url=SHEETY_USERS_ENDPOINT)
        data = response.json()
        user_data = data["users"]
        for row in user_data:
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=PASSWORD)
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=row["email"],
                    msg=message.encode('utf-8')
                )
