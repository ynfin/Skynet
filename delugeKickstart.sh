#!/bin/bash
#delugeKickstart.sh
#make sure deluge is running

makerun="deluged"

if ps ax | grep -v grep | grep deluged > /dev/null
        then
                exit
        else
        $makerun &

echo "Date: " $(date) >> /home/pi/var/www/disk/deluged.log
        fi
exit
