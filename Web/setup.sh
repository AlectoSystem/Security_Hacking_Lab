#! /bin/sh

sudo apt-get -y update
sudo apt-get -y upgrade 

apt-get install -y git
apt-get install -y python3
apt-get install -y python3-pip

git clone https://github.com/crypt0rr/typo3enum.git

pip install requests

