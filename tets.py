import json

text = '{"repository": [{"full_name": "davlloyd/dispatch-cpm"}], "commits": [ {"added": [ "request-4.json" ]}]}'
test = json.loads(text)
print(test["repository"][0]["full_name"])