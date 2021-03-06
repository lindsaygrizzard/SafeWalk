from twilio.rest import TwilioRestClient
import twilio
import os

# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

default_caller=os.environ['LG']
default_receiver=os.environ['AP']
default_message="I'll meet you at Twiiter in 10 minutes!"

def send_sms(caller=default_caller, receiver=default_receiver, message=default_message):
    try:
        client = twilio.rest.TwilioRestClient(account_sid, auth_token)
        message = client.messages.create(
            body=message,
            to=receiver,
            from_=caller
        )
    except twilio.TwilioRestException as e:
        print e
