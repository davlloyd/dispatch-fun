# Setup vcenter1

# Install base images for Python and nodejs

# Install images
- vmomi image is for vsphere functions
- request module added to nodejs for slack

dispatch create seed-images

dispatch create base-image python3-base dispatchframework/python3-base --language python3
dispatch create image python3 python3-base
dispatch create image python-vmomi python3-base --runtime-deps ./requirements-vmomi.txt
dispatch create image python-request python3-base --runtime-deps ./requirements-requests.txt

dispatch create base-image nodejs-base dispatchframework/nodejs-base --language nodejs
dispatch create image nodejs nodejs-base
dispatch create image nodejs-request nodejs-base --runtime-deps ./package.json

# Create access secret
dispatch create -f 1-secret-vsphere-pks.yaml
dispatch create -f 2-secret-slack.yaml


# Define driver for vcenter
dispatch create -f 3-drivertype-vcenter.yaml
dispatch create -f 4-driver-vcenter-dsc.yaml   (or 4.1 for personal repo version)

# Create functions for slack, git and vmclone requests

dispatch create function --image=python-vmomi clonevm functions/clonevm --handler=clonevm-web.handle --secret vsphere-cloud
dispatch create function --image=python-request slack-post-vm functions/slack-post --handler=slack_post.handle --secret slack,vsphere-cloud
dispatch create function --image=python-request git-vmrequest functions/git-vmrequest --handler=git-vmrequest.handle --secret git

# Publish the cloneVM and Git-Request API

dispatch create api --https-only --method POST --path /clonevm post-clonevm clonevm
dispatch create api --https-only --method POST --path /git-vmrequest post-gitvm git-vmrequest

# Subscribe to the vm events

dispatch create subscription --name vmPoweredOnSlack --event-type="vm.powered.on" slack-post-vm --secret slack
dispatch create subscription --name vmPoweredOffSlack --event-type="vm.powered.off" slack-post-vm --secret slack
dispatch create subscription --name vmCloneSlack --event-type="vm.clone" slack-post-vm  --secret slack

dispatch create subscription --name vmCreatedSlack --event-type="vm.being.created" slack-post-vm --secret slack
dispatch create subscription --name vmDeployedSlack --event-type="vm.being.deployed" slack-post-vm --secret slack
dispatch create subscription --name vmReconfiguredSlack --event-type="vm.reconfigured" slack-post-vm  --secret slack
dispatch create subscription --name vmCreatedSlack --event-type="vm.being.created" slack-post-vm --secret slack



# Powershell demo

dispatch create image powershell-powercli powershell-base --runtime-deps ./requirements-powercli.psd1
dispatch create function vmlist ./functions/vmlist/vm_list.ps1 --image=powershell-powercli --handler=vm_list.ps1::handle --secret vsphere-cloud
dispatch exec vmlist --wait --secret vsphere-cloud


#Python Debug Demo
dispatch create function --image=python3 hello-py functions/hello-py --handler=hello-py.handle

# Test Functions

dispatch exec clonevm --wait --input='{"host": "sydscvvcloudvc01.syddsc.local","name": "test-026","template": "ubuntu-1604-template-agent"}' --secret vsphere-cloud

dispatch exec git-vmrequest --wait --input='{"repository": {"full_name": "davlloyd/dispatch-cmp"}, "commits": [ {"added": [ "request-8.json" ]}]}' --secret vsphere-cloud


# Test Slack Webhook


curl -X POST -H 'Content-type: application/json' --data '{"text":"Hello, World!"}' https://hooks.slack.com/services/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

# Test Published API

curl -k "https://jump.wwko2018.com:8443/dispatch/hello" -H "Content-Type: application/json" -d '{"name": "Jon", "place": "winterfell"}'

curl -k "https://192.168.192.83:443/dispatch/hello" -H "Content-Type: application/json" -d '{"name": "Jon", "place": "winterfell"}'


curl -X POST -k "https://jump.wwko2018.com:8443/dispatch/git-vmrequest" -H "Content-Type: application/json" -d '{"repository": [{"full_name": "davlloyd/dispatch-cmp"}], "commits": [ {"added": [ "request-26.json" ]}]}'

