docker stop sem_search_server
docker rm sem_search_server
docker image prune -f
docker run --name sem_search_server -p 8600:5000 sem_search:emb_v2 /bin/ash run.sh
