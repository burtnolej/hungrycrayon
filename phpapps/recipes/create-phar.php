<?php

/*
phar is a packaging system and can convert between different archive and compressiion formats
phar - make deployment onto web servers easy

PHP Fatal error:  Uncaught exception 'UnexpectedValueException' with message 'creating archive "/home/burtnolej/Development/pythonapps3/phpapps/recipes/pharapp//build/myapp.phar" disabled by the php.ini setting phar.readonly' in /home/burtnolej/Development/pythonapps3/phpapps/recipes/create-phar.php:8

For documentation purposes, what harel needed to do. He needed to change
from "; phar.readonly = on"
to      "phar.readonly = off"

Eg. un-comment the line and change on to off.
*/

$home = "/home/burtnolej/Development/pythonapps3/phpapps/recipes/pharapp/";
$srcRoot = $home."/src";
$buildRoot= $home."/build";

$phar = new Phar($buildRoot . "/myapp.phar", 
FilesystemIterator::CURRENT_AS_FILEINFO | FilesystemIterator::KEY_AS_FILENAME, "myapp.phar");
	
$phar["index.php"] = file_get_contents($srcRoot . "/index.php");
$phar["common.php"] = file_get_contents($srcRoot . "/common.php");
$phar->setStub($phar->createDefaultStub("index.php"));

copy($srcRoot . "/config.ini", $buildRoot . "/config.ini");

/*

pharapp
   src
   	index.php
   	common.php
   	common.ini
   build
   
   
/* Contents of index.php
<?php
require_once "<path>/pharapp/src/common.php";
$config = parse_ini_file("config.ini");
AppManager::run($config);
*/

/*
<?php
class AppManager
{
    public static function run($config) {
         echo "Application is now running with the following configuration... ";
         var_dump($config);
     }
}
*/

/* config.ini
[database]
host=localhost
db=dbname
user=myuser
pass=dbpass
*/



