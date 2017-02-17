#!/bin/bash
. ~/.bashrc

ROOT=webcore

export SSDBNAME=/Users/burtnolej/Development/pythonapps/clean/db/fucia.sqlite
ROOTPATH=/Users/burtnolej/Development/pythonapps/clean

PHPPATH=/Users/burtnolej/Development/pythonapps/phpapps/utils

TARGETDB=$ROOTPATH/db/fucia.sqlite
SOURCEDB=$ROOTPATH/apps/schoolschedulewizard/test_$ROOT.sqlite
SOURCEDB_BACKUP=$ROOTPATH/apps/schoolschedulewizard/test_$ROOT.sqlite.backup
PYEXEC=ssviewer_rest.py
ROOTPATH=/Users/burtnolej/Development/pythonapps/clean
TEST_PYEXEC=test_$ROOT.py
TEST_PHPEXEC=$PHPPATH/test_webpage_utils.php

TEST_PYEXECPATH=$ROOTPATH/apps/schoolschedulewizard/$TEST_PYEXEC
PYEXECPATH=$ROOTPATH/apps/schoolschedulewizard/$PYEXEC

SELENIUMPATH=~/Downloads/selenium-server-standalone-2.53.0.jar
CHROMEDRIVER=/usr/local/bin/chromedriver 
GECKODRIVER=/usr/local/bin/geckodriver

RUNDATE=`date +"%m%d%y-%H%M%S"`
PYEXECLOG=$RUNDATE"_"$PYEXEC.log
SELENIUMLOG=$RUNDATE_selenium.log

# remove the current link
if [ -f $TARGETDB ]; then
        rm $TARGETDB
else
        echo "no "$TARGETDB" file found, skipping rm"
fi

# remake the link from fucia.sqlite to the db required for this test
if [ -f $SOURCEDB ]; then
        ln -s $SOURCEDB $TARGETDB
else
        echo "no "$SOURCEDB" file; exitting"
        exit
fi


# reset the database to erase any changes from last test
if [ -f $SOURCEDB_BACKUP ]; then
        cp $SOURCEDB_BACKUP $SOURCEDB
else
        echo "no "$SOURCEDB_BACKUP" file found; exitting"
        exit
fi
# run php tests to create webpages to test
php $TEST_PHPEXEC

# killall the existing python instances
killall java
killall Python

sleep 1

# start the rest service
echo "using "$PYEXELOG
python $PYEXECPATH --allow-unknown >& /tmp/log/$PYEXECLOG

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
killall java
