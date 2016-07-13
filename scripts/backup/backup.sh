#!/bin/bash

SOURCE=/usr
TARGET=/media/backup/test
PATH=$PATH:/bin:/usr/bin
BASENAME=`basename "$0"`
LOCKFILE="."$BASENAME".lock"
RUNDATE=`date +"%m%d%y-%H%M%S"`
LOGFILE=$BASENAME.$RUNDATE
ROOTDIR=/home/burtnolej/Development/pythonapps3/scripts/backup
TESTBASE=$ROOTDIR/backup-test-dir
TESTRESULT=/tmp/$BASENAME.testresult
BACKUP=delta
MODE=$1
LOGDIR=$ROOTDIR/logs

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

	# make changes to source to test rsync picks up everything 
	touch $SOURCE/$RUNDATE # add a new file
	echo $RUNDATE >> $SOURCE/foobar1 # change existing file
	touch $SOURCE/foobar2 # change timestamp only
        # setfattr 

	EXPTESTRESULT=$TESTBASE/filelist
	echo $RUNDATE >> $EXPTESTRESULT
	sort $EXPTESTRESULT > /tmp/tmp
	mv /tmp/tmp $EXPTESTRESULT

	SUCCESSTEST="Files "$EXPTESTRESULT" and "$TESTRESULT" are identical"

	EXCLUDE=( "foobar4" "foobar5" )
	for i in "${EXCLUDE[@]}"
	do	
        	EXCLUDEFLAG=$EXCLUDEFLAG" --exclude="$i
	done

fi

EXEC="rsync -rv -backup --backup-dir=./"$BACKUP/$RUNDATE" "$SOURCE" "$TARGET" --links --times -xattr --log-file="$LOGDIR/$LOGFILE" "$EXCLUDEFLAG
`$EXEC`

rm $LOGDIR/CURRENT

ln -s $LOGFILE $LOGDIR/CURRENT
 
echo $EXEC >> $LOGDIR/$LOGFILE # log the command that was run

# if no changes to existing files are present; delete the dir created in delta

#awk '{split($0,a," "); print a[1]}'`

#need a test if dir gets deleted - if delta file has 1 more line than orig file and if updated timestamp is done


# check if any updated files (stored in delta dir)
NUMDELTA=`ls $TARGET/$BACKUP/$RUNDATE | wc -l` 

# if delta empty then delete
if [ "$NUMDELTA" -eq 0 ];  then
	echo $BACKUP/$RUNDATE" is empty so removing"
	rmdir $TARGET/$BACKUP/$RUNDATE
fi

# check results
if [ "$1" = "test" ]; then
	`ls $TARGET | sort  > $TESTRESULT`

	DIFFRESULT=`diff -s $EXPTESTRESULT $TESTRESULT`
	
	if [ "$DIFFRESULT" = "$SUCCESSTEST" ]; then
		echo "SUCCESS"
	else
		echo "FAILURE - checkout "$TESTRESULT
	fi
fi

rm $LOCKFILE

tail -n 3 $LOGDIR/$LOGFILE
