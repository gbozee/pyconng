IMAGE_NAME="registry.gitlab.com/tuteria/pyconng"

cd /home/sama/app_code/pyconng && docker build -f compose/django/Dockerfile -t=$IMAGE_NAME .
docker login -u $1 -p $2 registry.gitlab.com
docker push $IMAGE_NAME 
docker rmi $(docker images --filter "dangling=true" -q --no-trunc)
# cd /home/sama/tuteria && docker build -f compose/celery/Dockerfile -t=registry.gitlab.com/tuteria/tuteria/celery compose/celery
# docker push registry.gitlab.com/tuteria/tuteria/celery
# cd ~/projects/tuteria/ && docker build -f compose/django/Dockerfile -t=gbozee/tuteria .
# cd /home/sama/code/tuteria && docker build -f pricing_service/Dockerfile -t=registry.gitlab.com/tuteria/tuteria/pricing pricing_service
# docker push registry.gitlab.com/tuteria/tuteria/pricing