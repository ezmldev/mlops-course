## First Container

```
docker run --interactive --tty  ubuntu
# definition alert cont vs image
```

inside the container
```
ps
apt-get update
apt-get install curl -y
curl google.com
exit
# definition PID1=container
```

on the host
```
docker ps
docker ps -a
docker rename ac mycontainer
docker ps -a
docker start mycontainer
docker attach mycontainer
# definition alert
# realize fs lifecycle
curl
# even bash-history (up-arraow)
# ctrl-p ctrl-q
```

on the host
```
docker ps
# mycontainer is not exited
```

repeate the same run command, with short options
```
docker run -it  ubuntu
curl
# command not found
# definition alert immutable images
```

images ...
```
docker images
```

Create Dockerfile
```
FROM ubuntu
RUN apt-get update
RUN apt-get install -y curl
```

in the terminal
```
docker build -t mycurl .
docker images
docker rm -f mycontainer
docker ps -a
docker run -it mycurl 
exit
```

image names/tags/registries
```
docker images
# notice latest
docker push 
docker build -t ttl.sh/lalyos/mycurl .
docker images
docker push ttl.sh/lalyos/mycurl
```

## Networking

```
docker run --detach --name myweb nginx:1.25
docker exec -it myweb bash
curl localhost
exit
```

on the host
```
curl localhost
# obviously its not working
docker rm -f myweb
```

recreate container with short options
```
docker run --detach  --publish 8080:80 --name myweb nginx:1.25
curl localhost:8080
```

## Copy

Create index.html
```
<html lang="en">
<body>
   <h2>My web site</h2>    
</body>
</html>
```

Copy file from host into container (scp)
```
docker cp index.html myweb:/usr/share/nginx/html/\
curl localhost:8080
```

## Volumes

```
docker rm -f myweb 
docker run -d -p 8080:80 --name myweb --volume $PWD:/usr/share/nginx/html nginx:1.25
# slide todo
```

## FastAPI image

manual version
```
pip install uvicorn fastapi
python3 fastapi-example/app.py 
```

other terminal
```
curl localhost:8000
```

containerize
```
docker build -t ttl.sh/myfast ./fastapi-example
docker run -d -p 8000:8000 ttl.sh/myfast
curl localhost:8000
```

```
docker run -d -p 8000:8000 --name myfast ttl.sh/myfast
```

prove image containes everything:
```
pip uninstall uvicorn fastapi
```

