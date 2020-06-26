#!/bin/sh

echo "Waiting for mysql..."
until mysqladmin ping -h"db" -P"3306" --silent
do
  echo "mysql is not ready will retry in 5..."
  sleep 5
done

echo -e "\nmysql is ready"

mysql -h"db" -P"3306" -p"root" -u"root" -e "SHOW DATABASES"
