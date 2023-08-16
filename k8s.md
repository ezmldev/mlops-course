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
  --values deploy/helm/dev/spam-values.yaml 

helm upgrade -i \
  web  \
  onechart/static-site \
  --values deploy/helm/dev/web-values.yaml
```

## prompt

show k8s context/ns in prompt
```
export PS1_OLD=$PS1
kp() { kubectl config view --minify -o json | jq '"\(.contexts[0].name)/\(.contexts[0].context.namespace)"' -r ; }
export PS1='$(kp) $ '
```

reset prompt
```
export PS1=$PS1_OLD
```