import requests
import os
import json

pg_token=os.environ['PAGERDUTY_TOKEN']
headers = {'Accept': 'application/json'} # returns json
print pg_token

test_url = "https://apitester.pagerduty.com/api/v1/users"

response = requests.get(test_url, 
                        headers=headers,
                        verify = True)

    # #Here is the info one can get about users, info can also be inserted
    # #alerts can also be found and inserted
    # users = response.json()['users']
    # print "USERS OBJECTS IN LIST: ", users
