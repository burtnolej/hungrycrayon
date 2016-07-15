#!/bin/bash

PATH=$PATH:/bin:/usr/bin
rootdir=/home/burtnolej/Development/pythonapps3/scripts/backup
logdir=$rootdir/logs
backup=delta

target=/media/backup/test
source=/usr
exclude=( "/dev" "/proc" "/sys" ) # files to exclude

basename=`basename "$0"`
rundate=`date +"%m%d%y-%H%M%S"`

logfile=$logdir/$basename.$rundate
lockfile="."$basename".lock"

pid=$BASHPID
argarray=( "$@" )
touch $logfile

function argset {
        arg=$1

        numargs=${#argarray[@]}

	writelog "[Args] numargs=$numargs detected" 20 " " "right" $logfile

        i=0
        while [ $i -lt "$numargs" ]
        do

                if [ ${argarray[$i]} = "$arg" ]; then
                        i=$[$i+1]
                        echo ${argarray[$i]}
                        exit
                fi
                i=$[$i+2]

        done

        echo "notfound"
}

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
        local rundate=`date +"%Y/%m/%d"` #date
        local runtime=`date +"%H:%M:%S"` #time

        # create list of all metadataitems to output
        metalist=( "$rundate " "$runtime " "[$pid]" "[$base]" )

	IFS='%' # allows strings to be made of consecutive spaces
        # iterate and pad each element with default padlen
        for meta in "${metalist[@]}"
        do
                padresult=$padresult$(spacepad $meta $metalength $just $padchar)

        done

        # pad content with user def len
        padresult=$padresult$(spacepad $content $strlen $just $padchar)

        # put on stdout
        if [ -f $logfile ]; then
		touch $logfile
		echo $padresult >> $logfile
	else
		echo $padresult
	fi
	
	unset IFS
}

function finishup {
	rm $logdir/CURRENT

	ln -s $logfile $logdir/CURRENT

	# mail results
	grep -v 'uptodate' $logdir/CURRENT | mail -s "log for backup:"$source burtnolejusa2@gmail.com

	rm $lockfile

	exit
}

mode=$(argset "--mode")
reset=$(argset "--reset")

if [ "$mode" = "notfound" ]; then
	writelog "[Args] defaulting to mode=test" 20 " " "right" $logfile
	mode="test"
else
	writelog "[Args] running with mode=$mode" 20 " " "right" $logfile
fi

if [ "$reset" = "notfound" ]; then
	writelog "[Args] defaulting to reset=false" 20 " " "right" $logfile
	reset="false"
else
	writelog "[Args] reset=$reset" 20 " " "right" $logfile
fi

if [ "$mode" = "test" ]; then
	target=$rootdir/backup
	source=$rootdir/source/
	exclude=( "foobar4" "foobar5" ) # files to exclude
fi

# remove lock
if [ "$1" = "removelock" ]; then
	rm $lockfile
	mode=$2
fi

# check if lock exists and create if doesnt
if [ -f $lockfile ]; then
	echo $lockfile" exists - check process is not already running"
	exit
else
	touch $lockfile
fi

# reset test directories

if [ "$reset" = "true" ]; then

	if [ "$mode" = "test" ]; then
		writelog "[reset] resetting $source & $target" 20 " " "right" $logfile
		cp $rootdir/filelist.orig $rootdir/filelist
		rm -rf $source
		cp -r $rootdir/source.orig $source
		rm -rf $target
	else
		writelog "[reset] resetting $target" 20 " " "right" $logfile
		rm -rf $target
	fi

	# archive logs
	if [ ! -f $logdir/rundate ]; then
		mkdir $logdir/$rundate
	fi

	mv $logdir/backup.sh.* $logdir/$rundate
	
	# remove lock
	rm $lockfile
	finishup	
fi

# if test passed then update source and target

if [ "$mode" = "test" ]; then

	# --------------------------------------------------------
	# make changes to source to test rsync picks up everything 
	# --------------------------------------------------------

	# add a new file
	touch $source/$rundate

	# change existing file
	cp $source/foobar1 /tmp/foobar1 # make a copy of orig for comparing purposes
	echo $rundate >> $source/foobar1 # make a change

	# timestamp only
	touch $source/foobar2 # change timestamp only

	# change an attribute
	setfattr -n user.foobar -v $rundate $source/foobar3

	exptestresult=$rootdir/filelist
	echo $rundate >> $exptestresult
	sort $exptestresult > /tmp/tmp
	mv /tmp/tmp $exptestresult

fi

# --------------------------------------------------------
# create exclusion list
# --------------------------------------------------------
for i in "${exclude[@]}"
do
	excludeFLAG=$excludeFLAG" --exclude="$i
done
	
writelog "Target="$target 20 " " "right" $logfile
writelog "Source=$source" 20 " " "right" $logfile
writelog "Exclude=$exclude" 20 " " "right" $logfile

exec="rsync -rvv -backup --backup-dir=./"$backup/$rundate" "$source" "$target" --links --times --xattrs --log-file="$logfile" "$excludeFLAG
`$exec`

writelog "Command=$exec" 20 " " "right" $logfile

# check if any updated files (stored in delta dir)
numdelta=`ls $target/$backup/$rundate | wc -l` 

# if delta empty then delete
if [ "$numdelta" -eq 0 ];  then
	writelog $backup/$rundate" is empty so removing" 20 " " "right" $logfile
	rmdir $target/$backup/$rundate
fi

# check results
if [ "$mode" = "test" ]; then

	# --------------------------------------------------------
	# assert results are correct
	# --------------------------------------------------------

	testresult=/tmp/$basename.testresult
	exptestresult=$rootdir/filelist
	successtest="Files "$exptestresult" and "$testresult" are identical"

	# check that the new files have been rsynced
	`ls $target | sort  > $testresult`

	diffresult=`diff -s $exptestresult $testresult`
	
	if [ "$diffresult" = "$successtest" ]; then
		writelog "SUCCESS:NEW" 20 " " "right" $logfile
	else
		writelog "FAILURE:NEW - checkout "$testresult 20 " " "right" $logfile
		echo "$successtest != $diffresult" >> $logfile
	fi

	# check that the attribute update has been preserved
	attrval=`getfattr --name=user.foobar --only-values "$target"/foobar3`

	if [ $attrval = $rundate ]; then
		writelog "SUCCESS:ATTR" 20 " " "right" $logfile
	else
		writelog "FAILURE:ATTR - checkout "$testresult 20 " " "right" $logfile
	fi

	# check that the updated file has been synced


	# check that the prev version is in the delta directory
fi

# add backup dir sizes to logfile
`cd $target;du -bm -all --max-depth=2 --human-readable .  >> $logfile`

finishup
