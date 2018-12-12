#!/usr/bin/env bash
user="davlloyd"
pass="B3ach8um!"
#curl -X DELETE -u "$user:$pass" https://index.docker.io/v1/repositories/$namespace/$reponame/
curl -X GET -u "$user:$pass" https://index.docker.io/v2/_catalog
