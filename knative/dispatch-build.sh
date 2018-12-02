export KO_DOCKER_REPO="pks-harbor.syddsc.local/library"
export DOCKER_REPO_OVERRIDE="${KO_DOCKER_REPO}"
export K8S_CLUSTER_OVERRIDE="faas"

export DISPATCH_NAMESPACE="dispatch-server"
export DISPATCH_DEBUG="true"
export RELEASE_NAME="dispatch-server"
export MINIO_USERNAME="dispatch"
export MINIO_PASSWORD="dispatch"
export INGRESS_IP=$(kubectl get svc knative-ingressgateway --namespace istio-system --output 'jsonpath={.status.loadBalancer.ingress[0].ip}')


brew install golang dep

---- 
# Go development environent for shell preference
export GOPATH=$HOME/go
export GOROOT=/usr/local/opt/go/libexec
export PATH=$PATH:$GOPATH/bin
export PATH=$PATH:$GOROOT/bin

test -d "${GOPATH}" || mkdir "${GOPATH}"
test -d "${GOPATH}/src/github.com" || mkdir -p "${GOPATH}/src/github.com"

go get k8s.io/client-go/...

helm dep build

----


