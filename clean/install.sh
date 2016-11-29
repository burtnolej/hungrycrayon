#!/bin/bash

HOST=www.hungrycrayon.com
USER=burtnolejusa
PASSWD=G0ldm@n1

CWD=`pwd`
HOME=/home/burtnolej
RHOME=/home/burtnolejusa

APPROOT=./Development/pythonapps3
#APPROOT=$HOME/Development/pythonapps3
PHPAPPROOT=$APPROOT/phpapps
DBPATH=$APPROOT/clean/db
SCRIPTPATH=$APPROOT/clean/scripts

PHPFILEPATH=$PHPAPPROOT/apps/sswebviewer
CSSFILEPATH=$PHPAPPROOT/apps/sswebviewer
PHPUTILPATH=$PHPAPPROOT/utils

PYFILEPATH=$APPROOT/clean/apps/schoolschedulewizard
PYUTILPATH=$APPROOT/clean/utils

DBNAME=fucia.sqlite

phpfiles=( "login" "getlink" "url" "xml2html2" "new" "edit" "search")
scriptfiles=( "killit" )
phputilfiles=( "ui_utils" "db_utils" "utils_xml")
cssfiles=( "fancytable" )

pyfiles=( "ssviewer" "ssviewer_rest" "ssviewer_utils_palette" "ssviewer_utils" "sswizard" "sswizard_utils" "dbtableviewer" "sswizard_query_utils" )

pyutilfiles=( "database_table_util" "database_util" "ui_utils" "misc_utils" "xml_utils" "misc_utils_log" "misc_utils_objectfactory" "misc_utils_generic" "misc_utils_process" "format_utils" "type_utils" "misc_utils_enum" )

linkscript="/tmp/remoteinstall.sh"
HTMLDOCROOT="/var/www/html"

rm $linkscript
#cat /dev/null > $linkscript

echo "#!/bin/bash" >> $linkscript
echo "cd $RHOME"
echo "gunzip $RHOME/install.tar.gz" >> $linkscript
echo "rm -rf $RHOME/Development" >> $linkscript
echo "tar -xvf $RHOME/install.tar" >> $linkscript
echo "rm $HTMLDOCROOT/*.php" >> $linkscript

cd $HOME

for phpfile in "${phpfiles[@]}"
do
	tarfiles="$tarfiles $PHPFILEPATH/$phpfile.php"
	echo "ln -s $RHOME/$PHPFILEPATH/$phpfile.php $HTMLDOCROOT" >> $linkscript
done

# php utils #############################################

for phputilfile in "${phputilfiles[@]}"
do
	tarfiles="$tarfiles $PHPUTILPATH/$phputilfile.php"
done

# scripts ###############################################

for scriptfile in "${scriptfiles[@]}"
do
	tarfiles="$tarfiles $SCRIPTPATH/$scriptfile.sh"
done

# css files ###############################################

for cssfile in "${cssfiles[@]}"
do
	tarfiles="$tarfiles $CSSFILEPATH/$cssfile.css"
	echo "ln -s $RHOME/$CSSFILEPATH/$cssfile.css $HTMLDOCROOT/default.css" >> $linkscript
done

for pyfile in "${pyfiles[@]}"
do
	tarfiles="$tarfiles $PYFILEPATH/$pyfile.py"
done

for pyutilfile in "${pyutilfiles[@]}"
do
	tarfiles="$tarfiles $PYUTILPATH/$pyutilfile.py"
done

# add on databases
tarfiles="$tarfiles $DBPATH/$DBNAME"

# add on linkscript
tarfiles="$tarfiles $linkscript"

# add on rest service restart
#python ./ssviewer_rest.py fucia


echo "rm $RHOME/install.tar" >> $linkscript

echo "export PATH=$PATH:$RHOME/$SCRIPTPATH" >> $linkscript
echo "killit.sh ssviewer_rest" >> $linkscript
echo "nohup python $RHOME/$PYFILEPATH/ssviewer_rest.py fucia &" >> $linkscript
#echo "rm -rf $RHOME/tmp" >> $linkscript

chmod +x $linkscript

tar -cvf /tmp/install.tar $tarfiles
gzip -f /tmp/install.tar

sshpass -p G0ldm@n1 sftp -oBatchMode=no -b  $CWD/sftp.txt burtnolejusa@www.hungrycrayon.com

sshpass -p G0ldm@n1 ssh -o StrictHostkeyChecking=no burtnolejusa@www.hungrycrayon.com "tar -xvf install.tar.gz"

sshpass -p G0ldm@n1 ssh -o StrictHostkeyChecking=no burtnolejusa@www.hungrycrayon.com .$linkscript

