BASE_PATH='registry.gitlab.com/tuteria/tuteria'
IMAGE_NAME="$BASE_PATH/pyconng"

WEB_CONTAINER_IMAGE_NAME="$BASE_PATH/pyconng-app"
WEB_CONTAINER_IMAGE_NAME_BACKUP="$BASE_PATH/pyconng-app-backup"
STATIC_CONTAINER_IMAGE_NAME="$BASE_PATH/pyconng-static"

cd /home/sama/app_code/pyconng && docker build -f compose/django/Dockerfile -t=$IMAGE_NAME .
docker login -u $1 -p $2 registry.gitlab.com
docker push $IMAGE_NAME 

cd /home/sama/app_code/pyconng && docker build -f compose/nginx/Dockerfile-django -t=$WEB_CONTAINER_IMAGE_NAME ./compose/nginx
docker push $WEB_CONTAINER_IMAGE_NAME

cd /home/sama/app_code/pyconng && docker build -f compose/nginx/Dockerfile-backup -t=$WEB_CONTAINER_IMAGE_NAME_BACKUP ./compose/nginx
docker push $WEB_CONTAINER_IMAGE_NAME_BACKUP

cd /home/sama/app_code/pyconng && docker build -f compose/design/Dockerfile -t=$STATIC_CONTAINER_IMAGE_NAME ./python_nigeria/static/designs
docker push $STATIC_CONTAINER_IMAGE_NAME

docker image prune -f
# cd /home/sama/tuteria && docker build -f compose/celery/Dockerfile -t=registry.gitlab.com/tuteria/tuteria/celery compose/celery
# docker push registry.gitlab.com/tuteria/tuteria/celery
# cd ~/projects/tuteria/ && docker build -f compose/django/Dockerfile -t=gbozee/tuteria .
# cd /home/sama/code/tuteria && docker build -f pricing_service/Dockerfile -t=registry.gitlab.com/tuteria/tuteria/pricing pricing_service
# docker push registry.gitlab.com/tuteria/tuteria/pricing