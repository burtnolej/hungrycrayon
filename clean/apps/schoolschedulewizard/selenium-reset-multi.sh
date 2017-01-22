#!/bin/bash

killall Python
cp test_multi.sqlite.backup test_multi.sqlite
python ./ssviewer_rest.py --allow-unknown &> rest.log

killall java
java -jar ~/Downloads/selenium-server-standalone-2.53.0.jar -Dwebdriver.chrome.driver=/usr/local/bin/chromedriver &> selenium.log &
#java -jar ~/Downloads/selenium-server-standalone-2.53.0.jar -Dwebdriver.gecko.driver=/usr/local/bin/geckodriver &> log.txt &

sleep 1
if [ "$1" = "runtest" ]; then
	if [ "$2" = "debug" ]; then
		python -m pdb ./test_multi.py 
	else
		python ./test_multi.py 
	fi
fi


