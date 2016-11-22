#/bin/sh

echo
echo
echo "killing the following processes that match" $1
echo "-------------------------------------------------"
ps -ef | grep $1 

ps -ef | grep $1 | awk '{split($0,a," "); print a[2]}' | xargs kill -9

sleep 1

echo
echo
echo "processes running now that match" $1
echo "-------------------------------------------------"
ps -ef | grep $1

