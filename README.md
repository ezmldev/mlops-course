# mlops-course

## Single node installation in codespaces
```
go install sigs.k8s.io/kind@v0.20.0 && kind create cluster

# And then basically this: 
https://www.kubeflow.org/docs/components/pipelines/v1/installation/localcluster-deployment/

curl -sfL https://get.k3s.io | sh -
sudo k3s server &
sudo k3s kubectl get node

export PIPELINE_VERSION=2.0.0
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic-pns?ref=$PIPELINE_VERSION"


```
