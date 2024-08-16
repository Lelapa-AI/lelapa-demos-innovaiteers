from twilio.rest import Client
from os import getenv
from dotenv import load_dotenv
load_dotenv()




"""
takes 2 parameters the message to send and user number contry code inclueded.
"""
def send_message(message,contact_number):
    account_sid = getenv("TWILLIO_SID")
    auth_token = getenv('TWILLIO_TOKEN')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
    from_='whatsapp:+14155238886',
    body=message,
    to=f'whatsapp:{contact_number}'
    )
    # return message error status for error handling
    return str(message)

