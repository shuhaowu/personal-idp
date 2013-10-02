#!/bin/bash

if [ -f /home/vagrant/installed ]; then
  echo "Setup already done... skipping. To run this again, remove /home/vagrant/installed"
  exit 0
fi

apt-get update
apt-get -y dist-upgrade
apt-get install -y python-software-properties
apt-add-repository ppa:chris-lea/node.js
apt-get update
apt-get install -y nginx python-dev libevent-dev automake libtool autoconf pkg-config build-essential openssl nodejs git-core libgmp3-dev g++ make libffi-dev

cd /home/vagrant
su vagrant -c "git clone https://github.com/mozilla/browserid.git; cd browserid; npm install"

cd /tmp
wget http://python-distribute.org/distribute_setup.py
python distribute_setup.py
easy_install pip

pip install -r /vagrant/requirements.txt

cd /vagrant
./script/setidp myidp
ln -s /etc/nginx/sites-available/idp /etc/nginx/sites-enabled/idp

echo "cd /vagrant" >> /home/vagrant/.bashrc

touch /home/vagrant/installed

echo "Setup complete! Some more things to do, though."
echo " 1. Setup the VM to use your own domain. Do /vagrant/scripts/setidp <your domain>"
echo " 2. Generate a keys inside the correct directory. Inside /vagrant/certs/, do openssl genrsa -out private-key.pem 4096; openssl rsa -in private-key.pem -pubout > public-key.pem"
echo " 3. Generate the support document by running /vagrant/scripts/gen_support_doc"
