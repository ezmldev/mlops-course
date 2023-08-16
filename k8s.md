## Setup

setup k3d
```
curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash
k3d cluster create -p "80:80@loadbalancer"
```

## deploy serving api + web ui

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