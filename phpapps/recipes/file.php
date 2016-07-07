<?php
$myfile = fopen("test.txt","r") or die("unable to open file!");
while (!feof($myfile)){
      echo fgetc($myfile);
}
fclose($myfile)
?>