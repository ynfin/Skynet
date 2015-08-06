import os
import time
import datetime

time.sleep(30)
os.system("sudo mount -t auto /dev/sda1/ /home/pi/var/www/disk")

with open("diskmountlog.txt","a") as myfile:
	myfile.write("disk remount triggered by reboot at "+ datetime.datetime.now()+ "\n")
