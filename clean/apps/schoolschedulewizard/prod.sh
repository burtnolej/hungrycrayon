#!/bin/bash
. ~/.bashrc

ROOT=quad



#ROOTPATH=/Users/burtnolej/Development/pythonapps/clean
ROOTPATH=$APPROOT/clean
TARGETDB=$ROOTPATH/db/fucia.sqlite
SOURCEDB=$ROOTPATH/apps/schoolschedulewizard/$ROOT.sqlite
PYEXEC=ssviewer_rest.py
PYEXECPATH=$ROOTPATH/apps/schoolschedulewizard/$PYEXEC

RUNDATE=`date +"%m%d%y-%H%M%S"`
PYEXECLOG=$RUNDATE"_"$PYEXEC.log
UNAMESTR=`uname`

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

# killall the existing python instances
if [ "$UNAMESTR" == "Darwin" ]; then
	killall Python
elif [ "$UNAMESTR" == "Linux" ]; then
	killall python
else
	echo "unknown os:"$UNAMESTR
	exit
fi

killall java

# start the rest service
echo "using "$PYEXELOG
python $PYEXECPATH --allow-unknown --custom-source 56m >& /tmp/log/$PYEXECLOG
