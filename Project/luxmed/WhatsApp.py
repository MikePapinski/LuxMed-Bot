# Download the helper library from https://www.twilio.com/docs/python/install
# This twillio API module
from twilio.rest import Client

def SendWhatsApp(DoctorNameValue, DateTimeValue, CityValue, ServiceValue, PhoneNumber):

    #Define the twilio SID and AUTH_TOKEN to process WhatsApp message:
    account_sid = 'ACcdf7b977980620c52d1be681fa30bf3c'
    auth_token = '3bd9318e9c6036d2793d45a4069630a6'

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