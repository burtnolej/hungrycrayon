#!/bin/bash
. ~/.bashrc

ROOT=webcore

export SSDBNAME=/Users/burtnolej/Development/pythonapps/clean/db/fucia.sqlite
PHPPATH=/Users/burtnolej/Development/pythonapps/phpapps/utils

ROOTPATH=/Users/burtnolej/Development/pythonapps/clean
TEST_PYEXEC=test_$ROOT.py
TEST_PHPEXEC=$PHPPATH/test_webpage_utils.php

TEST_PYEXECPATH=$ROOTPATH/apps/schoolschedulewizard/$TEST_PYEXEC

SELENIUMPATH=~/Downloads/selenium-server-standalone-2.53.0.jar
CHROMEDRIVER=/usr/local/bin/chromedriver 
GECKODRIVER=/usr/local/bin/geckodriver

RUNDATE=`date +"%m%d%y-%H%M%S"`
PYEXECLOG=$RUNDATE"_"$PYEXEC.log
SELENIUMLOG=$RUNDATE_selenium.log

# run php tests to create webpages to test
php $TEST_PHPEXEC

# killall the existing python instances
killall Python
killall java

sleep 1

# start selenium server (browser api service)
java -jar $SELENIUMPATH -Dwebdriver.chrome.driver=$CHROMEDRIVER &> /tmp/log/$SELENIUMLOG &

sleep 1
if [ "$1" = "runtest" ]; then
	if [ "$2" = "debug" ]; then
		python -m pdb TEST_PYEXECPATH
	else
		python $TEST_PYEXECPATH
	fi
fi

# killall the existing python instances
killall Python
killall java
