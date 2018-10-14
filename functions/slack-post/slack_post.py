
import json
import requests

def handle(ctx, payload):
    secrets = ctx["secrets"]
    if secrets is None:
        raise Exception("Requires slack secret")
    webhook_url = secrets["slack_url"]
    slack_data = {'text': "Incoming from Dispatch"}

    response = requests.post(
        webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    return {"status": response.status_code}
