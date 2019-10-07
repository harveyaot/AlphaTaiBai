docker stop emb_server
docker rm emb_server
docker image prune -y
docker run --name emb_server -p 8500:5000 emb:latest /bin/bash run.sh
