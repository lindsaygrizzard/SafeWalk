import requests
import os
import json

pg_token=os.environ['PAGERDUTY_TOKEN']
print pg_token

    # response = requests.get(
    # "https://apitester.pagerduty.com/api/v1/users",
    # headers = {
    #     "Authorization": pg_token,
    # },
    # verify = True,  # Verify SSL certificate
    # )

    # #Here is the info one can get about users, info can also be inserted
    # #alerts can also be found and inserted
    # users = response.json()['users']
    # print "USERS OBJECTS IN LIST: ", users
