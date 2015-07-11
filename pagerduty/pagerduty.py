import requests
import os
import json

pg_token=os.environ['PAGERDUTY_TOKEN']

partner_service_key=os.environ['FIND_PARTNER_SERVICE_KEY']
partner_api_key=os.environ['FIND_PARTNER_API_KEY']

headers = {'Accept': 'application/json', 
        'Authorization' : 'Token token=%s' % pg_token}

print pg_token

test_url = "https://apitester.pagerduty.com/api/v1/users"

get_request = requests.get(test_url, 
                        headers=headers
                        )
                        # verify=True)

# post_request = requests.post("", headers=headers, data=)

trigger_url = 'https://empowerwalk.pagerduty.com/services/PSSZYG8'
trigger_data = { 
          "service_key": service_key,
          "incident_key": "srv01/HTTP",
          "event_type": "trigger",
          "description": "Find me a partner please",
          "client": "Sample Partnering Service",
          "client_url": "/",
          "details": {"ping time": "1500ms",
                      "load avg": 0.75 }, 
          "contexts":[{"type": "link",
                       "href": "http://empowerwalk.pagerduty.com"}] 
            }


trigger_request = requests.post(trigger_url, headers=headers, data=json.dumps(trigger_data))

 # #Here is the info one can get about users, info can also be inserted
    # #alerts can also be found and inserted
    # users = response.json()['users']
    # print "USERS OBJECTS IN LIST: ", users