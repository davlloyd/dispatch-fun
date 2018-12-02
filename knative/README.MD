


export KO_DOCKER_REPO="pks-harbor.syddsc.local/library"
export DOCKER_REPO_OVERRIDE="${KO_DOCKER_REPO}"
export K8S_CLUSTER_OVERRIDE="faas"
export DOCKER_REGISTRY="pks-harbor.syddsc.local/library"
export DISPATCH_SERVER_DOCKER_REPOSITORY="pks-harbor.syddsc.local/library"

export DISPATCH_DEBUG="true"
export RELEASE_NAME="dispatch-server"
export MINIO_USERNAME="dispatch"
export MINIO_PASSWORD="dispatch"
export INGRESS_IP=$(kubectl get svc knative-ingressgateway --namespace istio-system --output 'jsonpath={.status.loadBalancer.ingress[0].ip}')


cat << EOF > config.json
{
  "current": "${RELEASE_NAME}",
  "contexts": {
    "${RELEASE_NAME}": {
      "host": "$(kubectl get service ${RELEASE_NAME}-nginx-ingress-controller -n ${DISPATCH_NAMESPACE}  --output 'jsonpath={.status.loadBalancer.ingress[0].ip}')",
      "port": 443,
      "scheme": "https",
      "insecure": true
    }
  }
}
EOF
# point to the config file (could also move to ~/.dispatch/config)
export DISPATCH_CONFIG=`pwd`/config.json

helm upgrade ${RELEASE_NAME} ./charts/dispatch -i --debug --namespace ${DISPATCH_NAMESPACE} -f ./charts/dispatch/values.yaml

helm install ${RELEASE_NAME} ./charts/dispatch --namespace ${DISPATCH_NAMESPACE} -f ./charts/dispatch/values.yaml