#!/bin/bash

str='acccccca'
newstr=$(echo $str | sed "s/c/\ /g")

echo $newstr

