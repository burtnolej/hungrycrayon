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
PID=$BASHPID

function spacepad {

        # passed args
        content=$1  # the string to pad
        strlen=$2 # the length of the result str (len(pad)+len(content))
        padchar=$4 # the char to pad with
        just=$3 # left / right

        # init working variables
        padstr=""
        i=0

        # work out the size of pad needed
        contentlen=${#content}
        lenpad=$[$strlen-$contentlen]

        # create a str of char=padchar x lenpad
        while [ $i -lt "$lenpad" ]
        do
                i=$[$i+1]
                padstr=$padstr$padchar
        done

        # apply justify instructions
        if [ $just = "left" ]; then
                echo $padstr$content
        else
                echo $content$padstr
        fi
}

function writelog {

        # passed args
        content=$1 # the string to pad
        strlen=$2 # the length of the result content str
        padchar=$3 # the char to pad with
        just=$4 # left/right
	logfile=$5
        metalength=8 # the target len of non content fields (like date)

        # init
        padresult=""

        # get meta data for log
        base=`basename "$0"` # caller script name
        rundate=`date +"%Y/%m/%d"` #date
        runtime=`date +"%H:%M:%S"` #time

        # create list of all metadataitems to output
        metalist=( "$rundate " "$runtime " "[$PID]" "($base)" )

	IFS='%' # allows strings to be made of consecutive spaces
        # iterate and pad each element with default padlen
        for meta in "${metalist[@]}"
        do
                padresult=$padresult$(spacepad $meta $metalength $just $padchar)

        done

        # pad content with user def len
        padresult=$padresult$(spacepad $content $strlen $just $padchar)

	echo $logfile

        # put on stdout
        if [ -f $logfile ]; then
		echo $padresult >> $logfile
	else
		echo $padresult
	fi
	
	unset IFS
}

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

EXEC="rsync -rvv -backup --backup-dir=./"$BACKUP/$RUNDATE" "$SOURCE" "$TARGET" --links --times --xattrs --log-file="$LOGDIR/$LOGFILE" "$EXCLUDEFLAG
`$EXEC`

rm $LOGDIR/CURRENT

ln -s $LOGFILE $LOGDIR/CURRENT
 

# if no changes to existing files are present; delete the dir created in delta

#awk '{split($0,a," "); print a[1]}'`

#need a test if dir gets deleted - if delta file has 1 more line than orig file and if updated timestamp is done

# check if any updated files (stored in delta dir)
NUMDELTA=`ls $TARGET/$BACKUP/$RUNDATE | wc -l` 

# if delta empty then delete
if [ "$NUMDELTA" -eq 0 ];  then
	writelog $BACKUP/$RUNDATE" is empty so removing" 20 " " "right" $LOGDIR/$LOGFILE
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
		writelog "SUCCESS:NEW" 20 " " "right" $LOGDIR/$LOGFILE
	else
		writelog "FAILURE:NEW - checkout "$TESTRESULT 20 " " "right" $LOGDIR/$LOGFILE
	fi

	# check that the attribute update has been preserved
	ATTRVAL=`getfattr --name=user.foobar --only-values "$TARGET"/foobar3`

	if [ $ATTRVAL = $RUNDATE ]; then
		writelog "SUCCESS:ATTR" 20 " " "right" $LOGDIR/$LOGFILE
	else
		writelog "FAILURE:ATTR - checkout "$TESTRESULT 20 " " "right" $LOGDIR/$LOGFILE
	fi

	# check that the updated file has been synced


	# check that the prev version is in the delta directory
fi

echo -e "\n\n"$EXEC >> $LOGDIR/$LOGFILE # log the command that was run
rm $LOCKFILE
