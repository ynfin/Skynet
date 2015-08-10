#!/usr/bin/env python

import os
import sys
from lxml import etree
import time
import stat
from datetime import datetime, timedelta
import shutil

skynetFiles_lower = []
skynetFiles = []

# delete old files
deletedays = 40

print 'filetimes:'
for path, subdirs, files in os.walk('/var/www/data/disk/storage'):
    for name in files:
	fullfilepath = os.path.join(path,name)
	aged = time.time() - os.path.getmtime(fullfilepath) > (deletedays * 24 * 60 * 60)
	if aged:
	    shutil.rmtree(path)
	    #os.remove(fullfilepath)
	    #os.rmdir(path)
	elif 'sample' in name:
	    #os.remove(fullfilepath)
	    #os.rmdir(path)
	    shutil.rmtree(path)	

for path, subdirs, files in os.walk('/var/www/data/disk/storage'):
    for name in files:
    	if name.endswith(('.mp4','.avi')):
            skynetFiles_lower.append(name.lower())
            skynetFiles.append(os.path.join(path,name))
            print name
            print os.path.join(path,name)
            print ' '

skynetFiles.sort(key=lambda x: os.path.getmtime(x), reverse=True)

with open('/home/pi/.flexget/config.yml') as f:
    content = f.readlines()

sidepanel = []

for line in content:
    if line.startswith("      - "):
	cleanline = line.replace("      - ","").lower()
	splitline = cleanline.split()
	for filename in skynetFiles_lower:
	    if all(x in filename for x in splitline):
		print filename + ' matches ',
		print splitline
		sidepanel.append(' '.join([str(x) for x in splitline]).title())

finalList = list(set(sidepanel))
finalList.sort()

# Write XML file for AJAX sidepanel
response = etree.Element("response")
panelfiles = etree.SubElement(response, "panelfiles")
serverfiles = etree.SubElement(response, "serverfiles")

for item in finalList:
    panelfile = etree.SubElement(panelfiles, "panelfile")
    filename = etree.SubElement(panelfile, "panelfilename")
    filename.text = str(item)

for item in skynetFiles:
    serverfile = etree.SubElement(serverfiles, "serverfile")
    filename = etree.SubElement(serverfile, "serverfilename")
    filepath = etree.SubElement(serverfile, "serverfilepath")
    filedate = etree.SubElement(serverfile, "serverfiledate")
    filename.text = str(os.path.basename(item))
    filepath.text = str(item).replace("/var/www/","")
    filedate.text = str(time.ctime(os.path.getmtime(item)))

print(etree.tostring(response, pretty_print=True))

# Write the XML to the output file
with open('/var/www/skynetcontent.xml', 'w') as output_file:
    output_file.write('<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>\n')
    output_file.write(etree.tostring(response, pretty_print = True))

print "xml written..."
