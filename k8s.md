## Setup

setup k3d
```
curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash
k3d cluster create -p "80:80@loadbalancer"
```


```
alias k=kubectl
. <(k completion bash)
complete -o default -F __start_kubectl k
. <(helm completion bash)
```


## deploy serving api and web ui - kubectl

```
kubectl apply -f deploy/ --recursive
```

testing locally
```
curl \
  -H "Content-type: application/json" \
  -d '{"data":"subscribe"}' \
  spam.lvh.me/invocations/ 
```

## deploy with helm

```
helm repo add onechart https://chart.onechart.dev

helm upgrade -i \
  spam onechart/onechart \
  --values spam-values.yaml 

helm upgrade -i \
  web  \
  onechart/static-site \
  --values web-values.yaml
```