address="192.168.0.108"
echo $address

scp webfiles/* pi@$address:/var/www
scp cleanup/* pi@$address:~/skynet/cleanup
scp configs/* pi@$address:~/skynet/configs
