#!/bin/bash

redcap_zip_file=redcap11.0.5.zip

mkdir redcap
unzip ${redcap_zip_file}
rm "'Installation Instructions.txt'"
rm "'REDCap License.txt'"

# Move redcap install files to the webfolder specified by Apache
sudo mv redcap /var/www/html/

# Create redcap database
sudo mysql -u root -p"password" -Bse 'CREATE DATABASE IF NOT EXISTS `redcap`;'

# Create mysql user to be used for redcap
sudo mysql -u root -p"password" -Bse "CREATE USER 'leap'@'%' IDENTIFIED WITH mysql_native_password BY 'password';"
sudo mysql -u root -p"password" -Bse "GRANT SELECT, INSERT, UPDATE, DELETE ON \`redcap\`.* TO 'leap'@'%';"

# Modify redcap .php file to use correct database and user
sed -i 's/your_mysql_host_name/localhost/g' /var/www/html/redcap/database.php
sed -i 's/your_mysql_db_name/redcap/g' /var/www/html/redcap/database.php
sed -i 's/your_mysql_db_username/leap/g' /var/www/html/redcap/database.php
sed -i 's/your_mysql_db_password/password/g' /var/www/html/redcap/database.php
sed -i "s/$salt = '';/$salt = 'jh398k3420jd2dj9';/g" /var/www/html/redcap/database.php

# Run redcap sql script for setup
mysql -u root -p"password" < redcap.sql

# Configure redcap cron job
(crontab -l 2>/dev/null; echo "* * * * * /usr/bin/php /var/www/html/redcap/cron.php > /dev/null") | crontab -

# Increase max_input_vars in php.ini
php_ini_path=/etc/php/7.4/apache2/php.ini
sudo sed -i "s/;max_input_vars = 1000/max_input_vars = 1000000/g" $php_ini_path
sudo systemctl restart apache2

# Change upload_max_filesize
sudo sed -i "s/upload_max_filesize = 2M/upload_max_filesize = 3000M/g" $php_ini_path
sudo sed -i "s/post_max_size = 8M/post_max_size = 3000M/g" $php_ini_path
sudo systemctl restart apache2

# Make folders writable
sudo chmod 777 /var/www/html/redcap/temp/
sudo chmod 777 /var/www/html/redcap/edocs/
sudo chmod 777 /var/www/html/redcap/modules/

# Disable rate limiter
sudo mysql -u root -p"password" -Bse "USE redcap; UPDATE redcap_config SET value=0 WHERE field_name='page_hit_threshold_per_minute';"

# Create super token
sudo mysql -u root -p"password" -Bse "UPDATE redcap_user_information SET api_token = 'FEJRQVHQ3993BYQ50KMXZ0XFQH17V3X5P5STELNZ2DE243EUKJDY4T2O12GZ5555' WHERE username='site_admin';"
