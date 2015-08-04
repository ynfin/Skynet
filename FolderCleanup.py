# import stash
import os
import datetime
import shutil

class Info:
    def __init__(self, name, time):
        self.name = name
        self.time = time

infolist = list()

# specify directory
dir_to_search = "/home/pi/var/www/disk/skynet"

print "opening terminator logfile for logging..."
text_file = open("/home/pi/var/www/disk/skynet/TerminatorLog.txt", "wb")

text_file.write(str("cron scheduled script /home/pi/FolderCleanup.py output file: \ndeletion day: 30days \ntorrent deletion: 20 days \n"))
text_file.write(str("======================= - "))
text_file.write(str(datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")))
text_file.write(str(" - =======================\n"))

namelist_del = list()
namelist_1 = list()
namelist_2 = list()
namelist_3 = list()


# search upper directort
for dirpath, dirnames, filenames in os.walk(dir_to_search):

   print "dirpath: " , dirpath 
   print "dirnames: ", dirnames
   print "filenames", filenames
   print " "

# remove empty folders
   if os.listdir(dirpath) == []:
      shutil.rmtree(dirpath)
      print "FOUND EMPTY FOLDER, DELETING IT!!!"
      print dirpath

# go through files and check timestamp
   for file in filenames:
      curpath = os.path.join(dirpath, file)
      file_modified = datetime.datetime.fromtimestamp(os.path.getmtime(curpath))
# if timestamp older then set amount delete file
      now = datetime.datetime.now()
      print curpath
      if now  - file_modified > datetime.timedelta(days=50):
          if file == ("TerminatorLog.txt"):
             print "days: " , (now-file_modified).days,"\tkeeping ", file
          else:
             print "ENTERING DELETE LOOP"
             #shutil.rmtree(curpath)
             os.remove(curpath) # does not remove folder
             print "days: ", (now-file_modified).days,"\tREMOVE --> ", file
             namelist_del.append(str(file))
             if os.path.isdir(curpath):
                print "Found folder, but it may not be empty..."
                if os.listdir(curpath)==[]:
                   shutil.rmtree(curpath)
                   print "\t- The folder was empty, it will be deleted..."
             # text_file.write(file)
             # text_file.write('\n')
      else:
          print "days: ", (now-file_modified).days,"\tkeeping ", file
          
          infolist.append(Info(file,(now-file_modified).days))

          if (now - file_modified) > datetime.timedelta(days=(30-1)):
             namelist_1.append(file)
          elif (now - file_modified) > datetime.timedelta(days=(30-2)):
             namelist_2.append(file)          
          elif (now - file_modified) > datetime.timedelta(days=(30-3)):
             namelist_3.append(file)

print "\n\ndelete now:"
text_file.write("\n- Deleted today: \n")
for names in namelist_del:
   print '\t',names
   text_file.write('\t')
   text_file.write(names)
   text_file.write('\n')
print '\n'

print "deleting in next 24 hours:"
text_file.write("\n- Deletion in 1 day: \n")
for names in namelist_1:
   print '\t',names
   text_file.write('\t')
   text_file.write(names)
   text_file.write('\n')
print '\n'

print "deleting in next 48 hours:"
text_file.write("\n- Deletion in 2 days: \n")
for names in namelist_2:
   print '\t', names
   text_file.write('\t')
   text_file.write(names)
   text_file.write('\n')
print '\n'

print "deleting in next 72 hours:"
text_file.write("\n- Deletion in 3 days: \n")
for names in namelist_3:
   print '\t', names
   text_file.write('\t')
   text_file.write(names)
   text_file.write('\n')
print '\n'

# sorterer liste for logg
infolist.sort(key=lambda x: x.time, reverse=False)

print "------------------------------------------------------------------------------------------------------"

text_file.write(str("\n\n\n\nIndex of shit...\n---------------------------------------------------------------------------------------------\nage\tname\n"))

day_one = False
day_two = False
day_three = False
week_one = False
week_two = False
week_three = False

for thing in infolist:
   print str(thing.time),'\t', str(thing.name)

   if (thing.time > (30-1)) and (not day_one):
      text_file.write("\n\n--------------------------------------------------------------- deletion in < 1 days")
      day_one = True

   elif (thing.time > (30-2)) and not day_two:
      text_file.write("\n\n--------------------------------------------------------------- deletion in < 2 days")
      day_two = True
  
   elif (thing.time > (30-3)) and not day_three:
      text_file.write("\n\n--------------------------------------------------------------- deletion in < 3 days")
      day_three = True

   elif (thing.time > (30-7)) and not week_one:
      text_file.write("\n\n--------------------------------------------------------------- deletion in < 1 week")
      week_one = True

   elif (thing.time > (30-14)) and not week_two:
      text_file.write("\n\n--------------------------------------------------------------- deletion in < 2 weeks")
      week_two = True

   elif (thing.time > (30-21)) and not week_three:
      text_file.write("\n\n--------------------------------------------------------------- deletion in < 3 weeks")
      week_three = True

   text_file.write('\n')
   text_file.write(str(thing.time))
   text_file.write('\t')
   text_file.write(str(thing.name))   
  # text_file.write('\n')

print "\nClosing loggfile"
text_file.close()
