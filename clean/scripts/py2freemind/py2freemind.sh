#!/bin/bash

#inputfile=../../utils/module_utils.py
inputfile=$1

#python ./py2freemind.py --input-filename=../../utils/module_utils.py \
python ./py2freemind.py --input-filename=$inputfile \
                        --full-label \
                        --suppress-attrib=Name \
                        --groupby-tag=var,arg \
                        --input-format-filename=./format_python_code.xml
