#!/bin/bash

arg1="foo"
arg2="bar"

list2=( $arg1 $arg2 )
#list2=( "dsdsd" "dsdsdsdsdsd" "32323" )

for i in "${list2[@]}"
do
	echo "$i"
done

i=0
max=10
padchar=" "
str="foobar"
padstr=$str

lenstr=${#padstr}
lenpad=$[$max-$lenstr]
echo $lenpad

IFS='%'

while [ $i -lt "$lenpad" ]
do 
	i=$[$i+1]
	padstr=$padchar$padstr
done

echo "123456789012345678909"
echo $padstr

unset IFS
