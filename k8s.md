## Setup

setup k3d
```
curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash
k3d cluster create -p "80:80@loadbalancer" -p "6443:6443@loadbalancer"
```


```
alias k=kubectl
. <(k completion bash)
complete -o default -F __start_kubectl k
. <(helm completion bash)
```


## deploy serving api and web ui - kubectl

```
kubectl apply -f deploy/kubectl/ --recursive
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


## Setting env var for GH action

First create a [classic token](https://github.com/settings/tokens/new)
- with the sinle `repo/public_repo` scope

```
echo $CODESPACE_NAME | GITHUB_TOKEN=ghp_xxxxxxxxxxxx gh variable set CODESPACE_NAME

kubectl create sa boss -n default
k create clusterrolebinding boss --serviceaccount default:boss --clusterrole cluster-admin

BOSS_TOKEN=$(kubectl create token boss -n default)
echo $BOSS_TOKEN | GITHUB_TOKEN=ghp_xxxxxxxxxxxx gh variable set BOSS_TOKEN
```

## codespace k8s api port expose

In VSCode locate the `PORTS` tab on the `Panel` (probably next to the terminal tab)

Open up port 6443:
- Change Protocol Port to HTTPS (right click)
- Port Visibility: Public (right click)

## remote KUBECONFIG

```
k config set-cluster codespace --server https://${CODESPACE_NAME}-6443.app.github.dev/ --insecure-skip-tls-verify 
k config set-credentials boss --token $BOSS_TOKEN 
k config set-context codespace --cluster codespace --user boss --namespace spam
k config use-context codespace
```