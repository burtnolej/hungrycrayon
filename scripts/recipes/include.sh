#!/bin/bash

echo $BASH_SOURCE

dir="${BASH_SOURCE%/*}"

if [[ ! -d $dir ]]; then dir="$PWD"; fi
. "$dir/args.sh"

argarray=("--foo" "bar" "--foobar" "barfoo")
val=$(argset "--foobar")
echo "$val"

