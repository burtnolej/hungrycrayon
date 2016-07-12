#!/bin/bash

SOURCE=/usr
TARGET=/media/backup/test
PATH=$PATH:/bin:/usr/bin
BASENAME=`basename "$0"`
LOCKFILE="."$BASENAME".lock"
RUNDATE=`date +"%m%d%y-%H%M%S"`
LOGFILE=$BASENAME.$RUNDATE
TESTBASE=/home/burtnolej/Development/pythonapps3/scripts/backup/backup-test-dir
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
	TARGET=$TESTBASE/backup
	BACKUP=./delta
	echo $RUNDATE > $SOURCE/foobar1 # change a file so delta exists to backup
	touch $SOURCE/foobar2 # touch a file so delta exists

	EXPTESTRESULT=$TESTBASE/filelist
	SUCCESSTEST="Files "$EXPTESTRESULT" and "$TESTRESULT" are identical"

	EXCLUDE=( "foobar4" "foobar5" )
	for i in "${EXCLUDE[@]}"
	do	
        	EXCLUDEFLAG=$EXCLUDEFLAG" --exclude="$i
	done

fi

EXEC="rsync -r -backup --backup-dir="$BACKUP/$RUNDATE" "$SOURCE" "$TARGET" --links --times -xattr --log-file="$LOGFILE
`$EXEC`

echo $EXEC >> $LOGFILE # log the command that was run

# check results
if [ "$2" = "checktest" ]; then
	`ls $TARGET > $TESTRESULT`

	DIFFRESULT=`diff -s $EXPTESTRESULT $TESTRESULT`
	
	if [ "$DIFFRESULT" = "$SUCCESSTEST" ]; then
		echo "SUCCESS"
	else
		echo "FAILURE - checkout "$TESTRESULT
	fi
fi

rm $LOCKFILE

tail -n 3 $LOGFILE
