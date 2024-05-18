#!/bin/bash

if ! [ -x "$(command -v docker-compose)" ]; then
  echo 'Error: docker-compose is not installed.' >&2
  exit 1
fi

domains=(estechpc.ru)
rsa_key_size=4096
data_path="./certbot"
email="mdikiy069@gmail.com" # Adding a valid address is strongly recommended
staging=0 # Set to 1 if you're testing your setup to avoid hitting request limits

if [ -d "$data_path" ]; then
  read -p "Existing data found for ${domains[*]}. Continue and replace existing certificate? (y/N) " decision
  if [ "$decision" != "Y" ] && [ "$decision" != "y" ]; then
    exit
  fi
fi

mkdir -p "$data_path/conf"
mkdir -p "$data_path/www"

docker-compose run --rm --entrypoint "\
  certbot certonly --webroot -w /var/www/certbot \
    --email $email \
    -d ${domains[*]} \
    --rsa-key-size $rsa_key_size \
    --agree-tos \
    --force-renewal" certbot
