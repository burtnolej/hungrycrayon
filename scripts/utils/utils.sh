#!/bin/bash

function argset {
        arg=$1

        numargs=${#argarray[@]}

        writelog "numargs=$numargs detected" 20 " " "right" $logfile

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
        grep -v 'uptodate' $logdir/CURRENT | mail -s "log for backup:"$source $mailto

        rm $lockfile

        exit
}




