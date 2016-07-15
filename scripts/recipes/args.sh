

function argset {
	arg=$1

	numargs=${#argarray[@]}

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

	echo -1
}

#argarray=( "$@" )

#argarray=("--foo" "bar")
#val=$(argset "--foo")
#echo "$val"

val=$(argset "bar")

if [ "$val" = -1 ]; then
	echo "default"
else
	echo "$val"
fi

#argarray=("--foo" "bar" "--foobar" "barfoo")
#val=$(argset "--foobar")
#echo "$val"
