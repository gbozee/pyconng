IMAGE_NAME="registry.gitlab.com/tuteria/pyconng"
WEB_CONTAINER_IMAGE_NAME="registry.gitlab.com/tuteria/pyconng-app"

echo $1 $2

cd /home/sama/app_code/pyconng && docker build -f compose/django/Dockerfile -t=$IMAGE_NAME .
docker login -u $1 -p $2 registry.gitlab.com
docker push $IMAGE_NAME 

cd /home/sama/app_code/pyconng && docker build -f compose/nginx/Dockerfile-django -t=$WEB_CONTAINER_IMAGE_NAME ./compose/nginx
docker push $WEB_CONTAINER_IMAGE_NAME

docker image prune -f
# cd /home/sama/tuteria && docker build -f compose/celery/Dockerfile -t=registry.gitlab.com/tuteria/tuteria/celery compose/celery
# docker push registry.gitlab.com/tuteria/tuteria/celery
# cd ~/projects/tuteria/ && docker build -f compose/django/Dockerfile -t=gbozee/tuteria .
# cd /home/sama/code/tuteria && docker build -f pricing_service/Dockerfile -t=registry.gitlab.com/tuteria/tuteria/pricing pricing_service
# docker push registry.gitlab.com/tuteria/tuteria/pricing