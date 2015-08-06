import os
import time
import sys

path = "/home/pi/var/www/disk/skynet"

now = time.time()

day = 86400
hour = 3600
min = 60

delay = 30 * min

f = os.path.join(path, f)

for f in os.listdir(path):
	if os.stat(f).st_mtime < now - delay:
		if os.path.isfile(f):
			os.remove(f)
