from twilio.twiml.messaging_response import MessagingResponse
from os import getenv
from dotenv import load_dotenv
load_dotenv()




"""
takes 2 parameters the message to send and user number contry code inclueded.
"""
def send_message(message):
    res = MessagingResponse()
    msg = res.message()
    if message != "":
        msg.body(message)
    # return message error status for error handling
    return str(res)

