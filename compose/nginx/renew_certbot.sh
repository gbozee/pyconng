#!/bin/bash
cd /home/pycon/pyconng
docker-compose run --rm --name certbot certbot bash -c "sleep 6 && certbot certonly --standalone -d pycon.ng -d www.pycon.ng --text --agree-tos --email hello@pycon.ng --server https://acme-v01.api.letsencrypt.org/directory --rsa-key-size 4096 --verbose --keep-until-expiring --standalone-supported-challenges http-01"
docker exec pyconng_nginx_1 nginx -s reload
