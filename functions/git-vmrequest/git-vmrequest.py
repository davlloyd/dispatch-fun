import json
import requests

def handle(ctx, payload):
    secrets = ctx["secrets"]
    if secrets is None:
        raise Exception("Requires vcenter secret")
    clone_url = "https://192.168.192.38:443/dispatch/clonevm"
    host = secrets["vcenterhost"]
    name =  = payload.get("name")
    template = "ubuntu-1604-template"

    clone_data = {'host': host, 'name': name, 'template':, template}
  

    response = requests.post(
        clone_url, data=json.dumps(clone_data),
        headers={'Content-Type': 'application/json'}
    )
    return {"status": response.status_code}
