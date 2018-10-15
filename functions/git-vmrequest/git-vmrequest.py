import json
import requests


def handle(ctx, payload):
    secrets = ctx["secrets"]
    if secrets is None:
        raise Exception("Requires git secret")
    clone_url = secrets["vmcloneurl"]
    host = secrets["vcenterhost"]
    template = secrets["template"]
    repopath = payload["repository"]["full_name"]

    filerequests = payload["commits"][0]["added"]

    vmlist = ""
    if (len(filerequests)):
        for filename in filerequests:
            if "template" not in filename.lower():
                file_url = 'https://raw.githubusercontent.com/{0}/master/{1}'.format(repopath, filename)
                response = requests.get(file_url)
                if response.status_code == 200:
                    entry = response.json()

                    name = entry["name"]
                    if(entry["template"] != ""):
                        sourcetemplate = entry["template"]
                    else:
                        sourcetemplate = template
                    if(entry["targethost"] != ""):
                        targethost = entry["targethost"]
                    else:
                        targethost = host
                    targetdc = entry["dc"]
                    targetfolder = entry["vmfolder"]
                    respool = entry["resourcepool"]
                    poweron = entry["poweron"]                

                    clone_data = {
                        'host': targethost, 
                        'name': name, 
                        'template': sourcetemplate,
                        'datacenterName': targetdc,
                        'vmFolder': targetfolder,
                        'resourcePool': respool,
                        'powerOn': poweron}

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
