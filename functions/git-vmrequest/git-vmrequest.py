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
                    if "template" in entry:
                        sourcetemplate = entry["template"]
                    else:
                        sourcetemplate = template
                    if "targethost" in entry:
                        targethost = entry["targethost"]
                    else:
                        targethost = host
                    if "dc" in entry:
                        targetdc = entry["dc"]
                    if "vmfolder" in entry:
                        targetfolder = entry["vmfolder"]
                    if "resourcepool" in entry:
                        respool = entry["resourcepool"]
                    if "poweron" in entry:
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
