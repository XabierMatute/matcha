
if [ -z "$1" ]; then
    docker exec -it flask_app_v2 sh
else
    docker exec -it flask_app_v2 $1
fi