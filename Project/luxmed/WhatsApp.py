# Download the helper library from https://www.twilio.com/docs/python/install
# This twillio API module
from twilio.rest import Client

def SendWhatsApp(DoctorNameValue, DateTimeValue, CityValue, ServiceValue, PhoneNumber):

    #Define the twilio SID and AUTH_TOKEN to process WhatsApp message:
    account_sid = ''
    auth_token = ''

    #Connect to twilio service
    client = Client(account_sid, auth_token)

    #Send WhatsApp message to via twilio
    message = client.messages.create(
                                body='Hello from LuxMed-Bot! I found a new visit for you on: ' + str(DateTimeValue) + ', ' + ServiceValue + ', ' + DoctorNameValue + ', ' + CityValue,
                                from_='whatsapp:+14155238886', # Twilio test number - DO NOT CHANGE
                                to='whatsapp:' + str(PhoneNumber) # Users phone number to receive message
                            )

    # Print to confirm the message was sent
    print(message.sid) 