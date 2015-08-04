#!/bin/bash

logfile=/home/pi/var/www/disk/skynet/conversionlog.txt
now=$(date)

rm $logfile

#if [ -z "$(pgrep mkv2mp4.sh)" ]
#if ps -ef | grep -v grep | grep mkv2mp4
if [[ "`pidof -x $(basename $0) -o %PPID`" ]]
then
  echo "process running..."
  echo -e $now" - Stopped by process running..." >> $logfile
  echo "This script is already running with PID `pidof -x $(basename $0) -o %PPID`" >> $logfile
  exit 0
else
  echo "no process running..."
  echo -e $now" - Starting new process...\n\n" >> $logfile
fi

echo "SINGLEFILES"
SINGLEFILES=$(find /home/pi/var/www/disk/skynet -maxdepth 1 -name '*.avi' -o -name '*.mkv' -o -name '*.mp4')
echo -e "\n\nfound potential spelunkers:\n"
echo $SINGLEFILES
for singlefile in $SINGLEFILES; do
  newdirpath="${singlefile%.*}"
  echo "creating home at" $newdirpath
  mkdir $newdirpath
  mv $singlefile $newdirpath
done

FILES=$(find /home/pi/var/www/disk/skynet -name "*.mkv" -o -name '*.avi')
echo -e "\n\nfound potential unconverted files:\n"
echo $FILES
echo -e "--------------------------------------\n\n"

echo "CONPLETIONCHECK:"
#check completion
for file in $FILES; do
  if [ -f $file.mp4 ]; then
    echo "File not found!"
    echo $file
    mkvlength=$(avconv -i $file 2>&1 | grep 'Duration' | awk '{print $2}' | sed s/,//)
    mp4length=$(avconv -i $file.mp4 2>&1 | grep 'Duration' | awk '{print $2}' | sed s/,//)

    mkvsec=$(date +'%s' -d $mkvlength)
    mp4sec=$(date +'%s' -d $mp4length)
    echo $mkvlength ' - ' $mkvsec
    echo $mp4length ' - ' $mp4sec
    dev=$(expr $mkvsec - $mp4sec)
    echo $dev
    if [ $dev -gt 10 ]
    then
      echo "removing uncomplete file: " $file.mp4
      echo -e "removing uncomplete file: " $file.mp4 >> $logfile  
      rm $file.mp4
    fi
  fi
done


for file in $FILES; do
  echo $file

    if [ -f $file'.isconverting' ]
    then
      echo "incomplete conversion encountered, resetting..."
      rm $file.mp4
      rm $file.isconverting
    fi

    if [ ! -f $file'.mp4' ]
    then
      echo file is not converted, converting...
      echo -e $now" - "$file "will be converted...\n" >> $logfile

      echo file is not converted, converting...
      INCFILE=$file.isconverting
      echo $file >> $INCFILE

      if [ ${file: -4} == ".mkv" ]
      then
	 echo "founc mkv file, only recoding sound"
         #if mkv --> no video codec needed
         avconv -y -i $file -vcodec copy -acodec aac -strict experimental $file.mp4
      else
	 echo "non-mkv found, recoding video and audio!"
         #if other format --> libx264 codec, with -preset veryslow
         #avconv -y -i $file -c:v libx264 -preset ultrafast -c:a aac -strict experimental $file.mp4
      fi

      echo creating html videofile...
      HTMLFILE=$file.html
      echo "<iframe src="$file".mp4></iframe>" > $HTMLFILE

      rm $INCFILE
   else
      echo -e "file converted, skipping...\n\n"
      echo -e $now" - "$file "already converted, skipping...\n" >> $logfile
    fi

  #avconv -i $file -codec copy $file.mp4
  #avconv -y -i $file -vcodec copy -acodec aac -strict experimental $file.mp4
done






echo -e "--------------------------------------\n\n"
