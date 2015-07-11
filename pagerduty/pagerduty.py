import requests

response = requests.get(
    "https://apitester.pagerduty.com/api/v1/users",
    headers = {
        "Authorization": "Token token=jvTJtbBKEPADtZyKyhrr",
    },
    verify = True,  # Verify SSL certificate
    )

    #Here is the info one can get about users, info can also be inserted
    #alerts can also be found and inserted
    users = response.json()['users']
    print "USERS OBJECTS IN LIST: ", users
