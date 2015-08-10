address="192.168.0.108"
echo $address

scp -r webfiles/* pi@$address:/var/www
scp scripts/* pi@$address:~/skynet/scripts
scp configs/* pi@$address:~/skynet/configs
