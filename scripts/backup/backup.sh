#!/bin/sh

SOURCE=/usr/
TARGET=/media/backup/test
PATH=$PATH:/bin:/usr/bin
BASENAME=`basename "$0"`
LOCKFILE="."$BASENAME".lock"
RUNDATE=`date +"%m%d%y-%H%M%S"`
LOGFILE=$BASENAME.$RUNDATE
TESTBASE=/mnt/bumblebee-burtnolej/Development/scripts/backup-test-dir
TESTRESULT=/tmp/$BASENAME.testresult
MODE=$1

# remove lock
if [ "$1" = "removelock" ]; then
	rm $LOCKFILE
	MODE=$2
fi

# check if lock exists and create if doesnt
if [ -f $LOCKFILE ]; then
	echo $LOCKFILE" exists - check process is not already running"
	exit
else
	touch $LOCKFILE
fi

# if test passed then update SOURCE and TARGET

if [ "$MODE" = "test" ]; then
	SOURCE=$TESTBASE/source/
	TARGET=$TESTBASE/target
	EXPTESTRESULT=$TESTBASE/filelist
	SUCCESSTEST="Files "$EXPTESTRESULT" and "$TESTRESULT" are identical"
	rm -r $TARGET/*
fi

EXEC="rsync -r "$SOURCE" "$TARGET" --links --times -xattr --verbose --log-file="$LOGFILE

`$EXEC`

# check results
if [ "$1" = "test" ]; then
	`ls $TARGET > $TESTRESULT`

	DIFFRESULT=`diff -s $EXPTESTRESULT $TESTRESULT`
	
	if [ "$DIFFRESULT" = "$SUCCESSTEST" ]; then
		echo "SUCCESS"
	else
		echo "FAILURE - checkout "$TESTRESULT
	fi
fi

rm $LOCKFILE

tail -n 2 $LOGFILE
