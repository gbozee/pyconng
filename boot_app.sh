IMAGE_NAME="registry.gitlab.com/tuteria/pyung"

cd /home/sama/app_code/pyung && docker build -f compose/django/Dockerfile -t=$IMAGE_NAME .
docker push $IMAGE_NAME 
# cd /home/sama/tuteria && docker build -f compose/celery/Dockerfile -t=registry.gitlab.com/tuteria/tuteria/celery compose/celery
# docker push registry.gitlab.com/tuteria/tuteria/celery
# cd ~/projects/tuteria/ && docker build -f compose/django/Dockerfile -t=gbozee/tuteria .
# cd /home/sama/code/tuteria && docker build -f pricing_service/Dockerfile -t=registry.gitlab.com/tuteria/tuteria/pricing pricing_service
# docker push registry.gitlab.com/tuteria/tuteria/pricing