# Setup vcenter1

# Install base images for Python and nodejs

# Install images
- vmomi image is for vsphere functions
- request module added to nodejs for slack

dispatch create base-image python3-base dispatchframework/python3-base --language python3
dispatch create image python3 python3-base
dispatch create image python-vmomi python3-base --runtime-deps ./requirements.txt

dispatch create base-image nodejs-base dispatchframework/nodejs-base --language nodejs
dispatch create image nodejs nodejs-base
dispatch create image nodejs-request nodejs-base --runtime-deps ./package.json

# Create access secret
dispatch create -f 1-secret-vsphere-pks.yaml
dispatch create -f 2-secret-slack.yaml


# Define driver for vcenter
dispatch create -f 3-drivertype-vcenter.yaml
dispatch create -f 4-driver-vcenter-pks.yaml

# Create functions for slack posts

dispatch create function --image=nodejs-request slack-post-vm-message functions/slack-post-vm-general --handler=./slack_vm_general.js
dispatch create function --image=nodejs-request slack-post-vm-deploy-message functions/slack-post-deploy-vm --handler=./slack_vm_being_deployed.js
dispatch create function --image=python-vmomi clonevm function/clonevm --handler=clonevm.handle --secret vsphere-pks


# Subscribe to the vm events
dispatch create subscription --name vmCreatedSlack --event-type vm.being.created slack-post-vm-message --secret slack
dispatch create subscription --name vmCloneSlack --event-type vm.clone slack-post-vm-message  --secret slack
dispatch create subscription --name vmPoweredOnSlack --event-type vm.poweredon slack-post-vm-message --secret slack
dispatch create subscription --name vmPoweredOffSlack --event-type vm.poweredoff slack-post-vm-message --secret slack
dispatch create subscription --name vmDeployedSlack --event-type vm.being.deployed slack-post-vm-deploy-message --secret slack




curl -X POST -H 'Content-type: application/json' --data '{"text":"Hello, World!"}' https://hooks.slack.com/services/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

# Slack webhook to channel 'dsc-dispatch'

cat << EOF > slack.json
{
    "slack_url": "https://hooks.slack.com/services/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"
}
EOF
dispatch create secret slack ./slack.json


dispatch create function --image=nodejs-request slack-post-vm-message . --handler=./slack_vm_general.js
dispatch create function --image=nodejs-request slack-post-vm-deploy-message . --handler=./slack_vm_being_deployed.js


dispatch create subscription --name vmCreatedSlack --event-type vm.being.created slack-post-vm-message --secret slack
dispatch create subscription --name vmCloneSlack --event-type vm.clone slack-post-vm-message  --secret slack
dispatch create subscription --name vmPoweredOnSlack --event-type vm.poweredon slack-post-vm-message --secret slack
dispatch create subscription --name vmPoweredOffSlack --event-type vm.poweredoff slack-post-vm-message --secret slack
dispatch create subscription --name vmDeployedSlack --event-type vm.being.deployed slack-post-vm-deploy-message --secret slack

cat << EOF > vsphere-cred.json
{
    "password": "password",
    "username": "pksservice@syddsc.local"
}
EOF


dispatch exec clonevm --wait --input='{"host": "sydscvvpksvc01.syddsc.local","name": "test-002","template": "ubuntu-1604-template"}' --secret vsphere
