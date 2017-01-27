#!/bin/bash

. ~/.bashrc

python test_database_table_util.py
#python test_database_util.py	

python test_misc_utils_objectfactory.py
python test_misc_utils_generic.py
python test_misc_utils.py	

#test_misc_utils_process.py
#test_http_utils.py
#test_module_utils.py
#test_image_utils.py
#test_type_utils.py
#test_misc_utils_enum.py	
#test_ui_utils2.py
#test_misc_utils_log.py	
#test_xml_utils.py

python ./test_ssloader.py 

python ./test_ssviewer_utils.py 
python ./test_ssviewer.py

./test_ssviewer_rest.sh

./test_all.sh		

./test_multi.sh


