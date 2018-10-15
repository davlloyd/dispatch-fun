# Setup vcenter1

# Install base images for Python and nodejs

# Install images
- vmomi image is for vsphere functions
- request module added to nodejs for slack

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
dispatch create -f 4-driver-vcenter-pks.yaml

# Create functions for slack, git and vmclone requests

dispatch create function --image=python-vmomi clonevm functions/clonevm --handler=clonevm-web.handle --secret vsphere-pks
dispatch create function --image=python-request slack-post-vm functions/slack-post --handler=slack_post.handle --secret slack
dispatch create function --image=python-request git-vmrequest functions/git-vmrequest --handler=git-vmrequest.handle --secret git

# Publish the cloneVM and Git-Request API

dispatch create api --https-only --method POST --path /clonevm post-clonevm clonevm
dispatch create api --https-only --method POST --path /git-vmrequest post-gitvm git-vmrequest

# Subscribe to the vm events

dispatch create subscription --name vmDeployedSlack --event-type vm.being.deployed slack-post-vm --secret slack
dispatch create subscription --name vmPoweredOnSlack --event-type vm.poweredon slack-post-vm --secret slack
dispatch create subscription --name vmPoweredOffSlack --event-type vm.poweredoff slack-post-vm --secret slack
dispatch create subscription --name vmCreatedSlack --event-type vm.being.created slack-post-vm --secret slack
dispatch create subscription --name vmCloneSlack --event-type vm.clone slack-post-vm  --secret slack



# Test Functions

dispatch exec clonevm --wait --input='{"host": "sydscvvpksvc01.syddsc.local","name": "test-008","template": "ubuntu-1604-template"}' --secret vsphere-pks

dispatch exec git-vmrequest --wait --input='{"hook_id": "test001"}' --secret vsphere-pks


# Test Slack Webhook


curl -X POST -H 'Content-type: application/json' --data '{"text":"Hello, World!"}' https://hooks.slack.com/services/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

# Test Published API

curl -k "https://jump.wwko2018.com:8443/dispatch/hello" -H "Content-Type: application/json" -d '{"name": "Jon", "place": "winterfell"}'


curl -X POST -k "https://jump.wwko2018.com:8443/dispatch/git-vmrequest" -H "Content-Type: application/json" -d '{"hook_id": "Jon"}'

