import json
import requests

def handle(ctx, payload):
    secrets = ctx["secrets"]
    if secrets is None:
        raise Exception("Requires git secret")
    clone_url = secrets["vmcloneurl"]
    host = secrets["vcenterhost"]
    name = payload["hook_id"]
    template = secrets["template"]

    clone_data = {'host': host, 'name': name, 'template': template}

    response = requests.post(
        clone_url, 
        data=json.dumps(clone_data),
        headers={'Content-Type': 'application/json'},
        verify=False
    )
    return {"status": response.status_code, "data": clone_data}
