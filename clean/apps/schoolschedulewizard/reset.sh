#!/bin/bash

killall Python
cp test_ssviewer_rest.sqlite.backup test_ssviewer_rest.sqlite
python ./ssviewer_rest.py --allow-unknown

sleep 1
if [ "$1" = "runtest" ]; then
        if [ "$2" = "debug" ]; then
                python -m pdb ./test_ssviewer_rest.py
        else
                python ./test_ssviewer_rest.py
        fi
fi
