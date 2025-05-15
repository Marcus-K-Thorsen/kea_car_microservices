## How to run the project using Docker compose

Be in the root of the project while running the commands.

```sh
# To initially build the project and start it
docker-compose build
docker-compose up -d

# If something should go wrong and you need to start over
docker-compose down --rmi all --volumes --remove-orphans
docker-compose down --volumes --remove-orphans

# To stop the docker compose regularly
docker-compose down

kubectl apply -R -f kubernetes/

kubectl delete -R -f kubernetes/
```
