
<?php

#require_once "phar:/pharapp/common.php";
require_once "/home/burtnolej/Development/pythonapps3/phpapps/recipes/pharapp/src/common.php";
$config = parse_ini_file("config.ini");
AppManager::run($config);

