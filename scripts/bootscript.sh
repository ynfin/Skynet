#!/usr/bin/env bash

sudo chmod 770 /var/www/data/disk

# mount external disk
sudo mount /dev/sda1 /var/www/data/disk

# add permissions
usermod -a -G debian-transmission pi
chgrp debian-transmission /var/www/data
sudo chmod 770 /var/www/data/disk
