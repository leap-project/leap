#!/bin/bash

# apache2 version: 2.4.41   
# mysql version: 8.0.25
# php version: 7.4.3 

sudo apt install unzip
sudo apt update
sudo apt install -y apache2

sudo apt install -y mysql-server

sudo mysql -Bse "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password'; FLUSH PRIVILEGES;"
sudo apt install -y php libapache2-mod-php php-mysql php-curl php-xml php-gd php-zip
sudo systemctl restart apache2
