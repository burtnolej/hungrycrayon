#!/bin/bash

PATH=$PATH:/bin:/usr/bin
rootdir=/home/burtnolej/Development/pythonapps3/scripts/backup
logdir=$rootdir/logs
backup=delta

target=/media/backup/test
source=/usr
exclude=( "/dev" "/proc" "/sys" ) # files to exclude
utils=/home/burtnolej/Development/pythonapps3/scripts/utils
basename=`basename "$0"`
rundate=`date +"%m%d%y-%H%M%S"`
mailto=burtnolejusa2@gmail.com

logfile=$logdir/$basename.$rundate
lockfile="."$basename".lock"

pid=$BASHPID
argarray=( "$@" )
touch $logfile

. $utils/utils.sh

mode=$(argset "--mode")
reset=$(argset "--reset")
source=$(argset "--source")

if [ "$mode" = "notfound" ]; then mode="test"; fi

if [ "$reset" = "notfound" ]; then reset="false"; fi

if [ "$source" = "notfound" ]; then 
	if [ ! "$mode" = "test" ]; then 
		exit 
	fi
fi

writelog "[args] mode=$mode reset=$reset" 20 " " "right" $logfile

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

	# make changes to source to test rsync picks up everything 

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

# create exclusion list
for i in "${exclude[@]}"
do
	excludeFLAG=$excludeFLAG" --exclude="$i
done
	
writelog "target="$target 20 " " "right" $logfile
writelog "source=$source" 20 " " "right" $logfile
writelog "exclude=$exclude" 20 " " "right" $logfile

exec="rsync -rvv -backup --backup-dir=./"$backup/$rundate" "$source" "$target" --links --times --xattrs --log-file="$logfile" "$excludeFLAG
`$exec`

writelog "command=$exec" 20 " " "right" $logfile

# check if any updated files (stored in delta dir)
numdelta=`ls $target/$backup/$rundate | wc -l` 

# if delta empty then delete
if [ "$numdelta" -eq 0 ];  then
	writelog $backup/$rundate" is empty so removing" 20 " " "right" $logfile
	rmdir $target/$backup/$rundate
fi

# check results
if [ "$mode" = "test" ]; then

	testresult=/tmp/$basename.testresult
	exptestresult=$rootdir/filelist
	successtest="Files "$exptestresult" and "$testresult" are identical"

	# check that the new files have been rsynced
	`ls $target | sort  > $testresult`

	diffresult=`diff -s $exptestresult $testresult`
	
	if [ "$diffresult" = "$successtest" ]; then
		writelog "test success:new" 20 " " "right" $logfile
	else
		writelog "test failure:new - checkout "$testresult 20 " " "right" $logfile
		echo "$successtest != $diffresult" >> $logfile
	fi

	# check that the attribute update has been preserved
	attrval=`getfattr --name=user.foobar --only-values "$target"/foobar3`

	if [ $attrval = $rundate ]; then
		writelog "test success:attr" 20 " " "right" $logfile
	else
		writelog "test failure:attr - checkout "$testresult 20 " " "right" $logfile
	fi

	# check that the updated file has been synced


	# check that the prev version is in the delta directory
fi

# add backup dir sizes to logfile
`cd $target$source;du -bm -all --max-depth=2 --human-readable .  >> $logfile`

finishup $source
