#!/bin/bash

python ./testrunner.py --rootdir=../../../clean/ \
                        --ignoredir ../testrunner/ >& tmp.log
