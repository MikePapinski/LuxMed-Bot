# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client

def SendWhatsApp(DoctorNameValue, DateTimeValue, CityValue, ServiceValue):
    # Your Account Sid and Auth Token from twilio.com/console
    # DANGER! This is insecure. See http://twil.io/secure
    account_sid = 'YOUR SID'
    auth_token = 'YOUR TOKEN'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
                                body='Hello from LuxMed-Bot! I found a new visit for you on: ' + str(DateTimeValue) + ', ' + ServiceValue + ', ' + DoctorNameValue + ', ' + CityValue,
                                from_='whatsapp:+14155238886',
                                to='whatsapp:+48884988538'
                            )

    print(message.sid)