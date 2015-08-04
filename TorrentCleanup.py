#!/usr/bin/python

from deluge.log import LOG as log
from deluge.ui.client import client
import deluge.component as component
from twisted.internet import reactor, defer
import time

############
# Change the following
cliconnect = client.connect(host='127.0.0.1',port=58846,username="yngve",password="delpass")
seeddir = "/home/pi/var/www/disk/shitler" # Directory to ignore for torrents to remain seeding
timedifference = 40 # Remove torrents older than this this time (in days)
is_interactive = True # Set this to True to allow direct output or set to False for cron
do_remove_data = True # Set to True to delete torrent data as well, false to leave it

###############
# Do not edit below this line!

oldcount = 0
skipcount = 0
seedcount = 0
errorcount = 0
torrent_ids = []

def printSuccess(dresult, is_success, smsg):
    global is_interactive
    if is_interactive:
        if is_success:
            print "[+]", smsg
        else:
            print "[i]", smsg

def printError(emsg):
    global is_interactive
    if is_interactive:
        print "[e]", emsg

def endSession(esresult):
    if esresult:
        print esresult
        reactor.stop()
    else:
        client.disconnect()
        printSuccess(None, False, "Client disconnected.")
        reactor.stop()

def printReport(rresult):
    if errorcount > 0:
        printError(None, "Failed! Number of errors: %i" % (errorcount))
    else:
        if oldcount > 0:
            printSuccess(None, True, "Removed %i torrents -- Skipped %i torrents -- Seeding %i torrents" % (oldcount, skipcount, seedcount))
        else:
            printSuccess(None, True, "No old torrents! -- Skipped %i torrents -- Seeding %i torrents" % (skipcount, seedcount))
    endSession(None)

def on_torrents_status(torrents):
    global filtertime
    tlist=[]
    for torrent_id, status in torrents.items():
        if status["save_path"] == seeddir:
            global seedcount
            seedcount += 1
        else:
            unixtime = "%s" % (status["time_added"])
            numunixtime = int(unixtime[:-2])
            humantime = time.ctime(numunixtime)
            if numunixtime < filtertime:
                global do_remove_data
                global oldcount
                oldcount += 1
                successmsg = " Removed %s:  %s from %s" % (humantime, status["name"], status["save_path"])
                errormsg = "Error removing %s" % (status["name"])
                tlist.append(client.core.remove_torrent(torrent_id, do_remove_data).addCallbacks(printSuccess, printError, callbackArgs = (True, successmsg), errbackArgs = (errormsg)))
            else:
                global skipcount
                skipcount += 1
                printSuccess(None, False, " Skipping %s: %s from %s" % (humantime, status["name"], status["save_path"]))
    defer.DeferredList(tlist).addCallback(printReport)

def on_session_state(result):
    client.core.get_torrents_status({"id": result}, ["name","time_added","save_path",]).addCallback(on_torrents_status)

def on_connect_success(result):
    printSuccess(None, True, "Connection was successful!")
    global timedifference
    global filtertime
    curtime = time.time()
    filtertime = curtime - (timedifference * 24 * 60 * 60)
    printSuccess(None, False, "Current unix time is %i" % (curtime))
    printSuccess(None, False, "Filtering torrents older than %s" % (time.ctime(int(filtertime))))
    client.core.get_session_state().addCallback(on_session_state)

cliconnect.addCallbacks(on_connect_success, endSession, errbackArgs=("Connection failed: check settings and try again."))

reactor.run()
