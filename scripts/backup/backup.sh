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

# reset test directories

if [ "$1" = "reset" ]; then

	rm -rf $TESTBASE/backup
	cp $TESTBASE/filelist.orig $TESTBASE/filelist
	rm -rf $TESTBASE/source
	cp -r $TESTBASE/source.orig $TESTBASE/source

	# archive logs
	if [ ! -f $LOGIDIR/RUNDATE ]; then
		mkdir $LOGDIR/$RUNDATE
	fi

	mv $LOGDIR/backup.sh.* $LOGDIR/$RUNDATE
	
	# remove lock
	rm $LOCKFILE
	exit
fi

# if test passed then update SOURCE and TARGET

if [ "$MODE" = "test" ]; then
	SOURCE=$TESTBASE/source/
	TARGET=$TESTBASE/backup

	# --------------------------------------------------------
	# make changes to source to test rsync picks up everything 
	# --------------------------------------------------------

	# add a new file
	touch $SOURCE/$RUNDATE

	# change existing file
	cp $SOURCE/foobar1 /tmp/foobar1 # make a copy of orig for comparing purposes
	echo $RUNDATE >> $SOURCE/foobar1 # make a change

	# timestamp only
	touch $SOURCE/foobar2 # change timestamp only

	# change an attribute
	setfattr -n user.foobar -v $RUNDATE $SOURCE/foobar3

	EXPTESTRESULT=$TESTBASE/filelist
	echo $RUNDATE >> $EXPTESTRESULT
	sort $EXPTESTRESULT > /tmp/tmp
	mv /tmp/tmp $EXPTESTRESULT

	SUCCESSTEST="Files "$EXPTESTRESULT" and "$TESTRESULT" are identical"

	# --------------------------------------------------------
	# create a list of files to exclude
	# --------------------------------------------------------
	EXCLUDE=( "foobar4" "foobar5" )
	for i in "${EXCLUDE[@]}"
	do	
        	EXCLUDEFLAG=$EXCLUDEFLAG" --exclude="$i
	done

fi

EXEC="rsync -rv -backup --backup-dir=./"$BACKUP/$RUNDATE" "$SOURCE" "$TARGET" --links --times --xattrs --log-file="$LOGDIR/$LOGFILE" "$EXCLUDEFLAG
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

	# --------------------------------------------------------
	# assert results are correct
	# --------------------------------------------------------

	# check that the new files have been rsynced
	`ls $TARGET | sort  > $TESTRESULT`

	DIFFRESULT=`diff -s $EXPTESTRESULT $TESTRESULT`
	
	if [ "$DIFFRESULT" = "$SUCCESSTEST" ]; then
		echo "SUCCESS:NEW"
	else
		echo "FAILURE:NEW - checkout "$TESTRESULT
	fi

	# check that the attribute update has been preserved
	ATTRVAL=`getfattr --name=user.foobar --only-values "$TARGET"/foobar3`

	if [ $ATTRVAL = $RUNDATE ]; then
		echo "SUCCESS:ATTR"
	else
		echo "FAILURE:ATTR - checkout "$TESTRESULT
	fi

	# check that the updated file has been synced


	# check that the prev version is in the delta directory
fi

rm $LOCKFILE

tail -n 3 $LOGDIR/$LOGFILE
