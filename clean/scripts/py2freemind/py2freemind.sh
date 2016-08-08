#!/bin/bash

python ./py2freemind.py --input-filename=../../utils/module_utils.py \
                        --full-label \
                        --suppress-attrib=Name \
                        --groupby-tag=var,arg \
                        --input-format-filename=./format_python_code.xml
