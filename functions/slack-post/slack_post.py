import json
import requests

def handle(ctx, payload):
    secrets = ctx["secrets"]
    if secrets is None:
        raise Exception("Requires slack secret")
    webhook_url = secrets["slack_url"]
    metadata = payload.get("metadata")
    if metadata is not None:
        vmName = metadata.get("vm_name");
        vmId = metadata.get("vm_id")
    else:
        vmName = ""
        vmId = ""
    message = payload.get("message");

    try:
        postmessage = "\n{0}\nVM Name: {1}\nVM_ID: {2}".format(message, vmName, vmId)
    except:
        postmessage = str(payload)
 
    slack_data = {'text': postmessage}
  

    response = requests.post(
        webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    return {"status": response.status_code}
