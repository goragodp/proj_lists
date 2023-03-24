#!/bin/bash
echo $1
sudo echo $1 > /etc/hostname
sudo echo 127.0.0.1 $1 >> /etc/hosts
sudo hostname $1
sudo service avahi-daemon restart
sudo echo $1 > /etc/salt/minion_id
sudo service salt-minion restart
