# from twilio.rest import Client
from os import getenv
from twilio.twiml.messaging_response import MessagingResponse
# from dotenv import load_dotenv

# load_dotenv()




"""
takes 2 parameters the message to send and user number contry code inclueded.
"""
def send_message(message,contact_number):
    print(contact_number)
    print("in twilio send message")
    
   

    msg = MessagingResponse()
    res = msg.message()
    res.body(message)
    # return message error status for error handling
    return str(msg)

