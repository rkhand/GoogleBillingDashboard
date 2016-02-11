#!/bin/bash
set -x
echo "discovering bootstrap bucket..."
APP_RELEASE=1.0
APP_VERSION=1.0
APP_NAME=billing-app
BUCKET_NAME=hd-automation-billing-app

echo "Automation user Creation"
USER='automation'
sudo useradd -c "Automation User" -m -r -s "/bin/sh" ${USER} || echo "User already exists."

echo " APT GET PYTHON, MYSQL, NGINX, NODEJS and NPM "
apt-get update
apt-get install -y python-pip python-dev build-essential
apt-get install -y libmysqlclient-dev
apt-get install -y python-MySQLdb
apt-get install -y nginx
apt-get install -y nodejs
apt-get install -y npm

echo " symlink for node and install virtual env "
sudo rm -r /usr/bin/node
ln -sf `which nodejs` /usr/bin/node


DEPLOY_HOME=/opt/${APP_NAME}
mkdir -p ${DEPLOY_HOME}
gsutil cp -R gs://${BUCKET_NAME}/* ${DEPLOY_HOME}
chown -R automation ${DEPLOY_HOME}
pip install -r ${DEPLOY_HOME}/requirements.txt
cd ${DEPLOY_HOME}
/usr/local/bin/gunicorn --bind 0.0.0.0:8080 --workers=10 --error-logfile ${DEPLOY_HOME}/gunicorn.log --timeout 240 wsgi:app -D


echo " grunt and npm install "
cd /opt/${APP_NAME}
npm install -g grunt-cli
npm install
grunt

install -m 644 --backup=numbered ${DEPLOY_HOME}/nginx-site.conf /etc/nginx/sites-available/gru.conf
rm -f /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/gru.conf /etc/nginx/sites-enabled/
service nginx restart


