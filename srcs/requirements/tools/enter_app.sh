
if [ -z "$1" ]; then
    docker exec -it flask_app sh
else
    docker exec -it flask_app $1
fi