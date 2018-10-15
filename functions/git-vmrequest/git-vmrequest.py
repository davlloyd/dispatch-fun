import json
import requests

def vmrequest(gituser, repo, filename):
    url = 'https://api.github.com/repos/{0}/{1}/contents/{2}'.format(gituser, repo, filename)
    req = requests.get(url)
    if req.status_code == 200:
        req = req.json() 


def handle(ctx, payload):
    secrets = ctx["secrets"]
    if secrets is None:
        raise Exception("Requires git secret")
    clone_url = secrets["vmcloneurl"]
    host = secrets["vcenterhost"]
    template = secrets["template"]
    repopath = payload["repository"][0]["full_name"]

    filerequests = payload["commits"][0]["added"]

    vmlist = ""
    if (len(filerequests)):
        for filename in filerequests:
            file_url = 'https://raw.githubusercontent.com/{0}/master/{1}'.format(repopath, filename)
            response = requests.get(file_url)
            if response.status_code == 200:
                entry = response.json()
                name = entry["name"]
                clone_data = {'host': host, 'name': name, 'template': template}
                response = requests.post(
                    clone_url, 
                    data=json.dumps(clone_data),
                    headers={'Content-Type': 'application/json'},
                    verify=False
                )
                vmlist += "{0}/n".format(clone_data)
            else:
                print(file_url)
    else:
        return {"status": "no new requests"}

    return {"status": "done", "data": vmlist}
