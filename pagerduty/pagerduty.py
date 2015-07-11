import requests
import os
import json

PG_TOKEN=os.environ['PAGERDUTY_TOKEN']
FP_SERVICE_KEY=os.environ['FIND_PARTNER_SERVICE_KEY']
FP_API_KEY=os.environ['FIND_PARTNER_API_KEY']

def testing(token):
    """Test API call using generic PG Token"""
    headers_api_test = {'Accept': 'application/json', 
                        'Authorization' : 'Token token=%s' % token}
    test_url = "https://apitester.pagerduty.com/api/v1/users"
    get_request = requests.get(test_url, 
                            headers=headers_api_test
                            )
    return get_request


def trigger_fp():
    """Trigger Incident for Find Partner Service"""
    trigger_url = 'https://empowerwalk.pagerduty.com/services/PSSZYG8'

    trigger_headers = {'Accept': 'application/json', 
            'Authorization' : 'Token token=%s' % FP_API_KEY}

    trigger_data = { 
              "service_key": FP_SERVICE_KEY,
              "incident_key": "srv01/HTTP",
              "event_type": "trigger",
              "description": "Find me a partner please",
                }

    trigger_request = requests.post(trigger_url, 
                                    headers=trigger_headers, 
                                    data=json.dumps(trigger_data))

    return trigger_request


if __name__ == "__main__":
    test = testing(PG_TOKEN)
    trigger = trigger_fp()
