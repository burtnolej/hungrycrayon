<!DOCTYPE html>
<html>
<head>
<style>
#nav_master {
    background-color:black;
    color:white;
    text-align:left;
    padding:5px;
    width: 500px;
    margin: auto;
    border: 3px solid #73AD21;
}

#nav {
    padding:10px;
    line-height:30px;
    background-color:#eeeeee;
    height:2000px;
    float:left;
    text-align:left;
    width: 200px;
    border: 3px solid #73AD21;
    <!margin: auto;>   
}
#content {
    background-color:#eeeeee;
    <!width:550px;>
    float:left;
    text-align:left;
    padding:10px;
    border: 3px solid #73AD21;
    <!margin: auto;>
}

#ul {
    list-style:none;
    padding-left:0;
}
#ul1 {
    list-style:none;
    padding-left:1em;
}
#ul2 {
    list-style:none;
    padding-left:2em;
}

tab1 { padding-left: 4em; }
tab2 { padding-left: 8em; }
tab3 { padding-left: 12em; }
tab3-5 { padding-left: 12.6em; }            
</style>

<?php require_once("navigator.html");
require_once("build-install.php");
require_once("html-html.php");
require_once("libraries-modules.php");
?>
<div id="content">
<!---------------------------------------------------------------------------------->
<!---------------------------------------------------------------------------------->
<div id="overview">
<h3>Overview</h3>

For reference i am running Ubuntu 14.04.1 on a Mac.

UFW as a firewall

Get the version for your environment from here : <a href=http://php.net/downloads.php>php.net</a>
<br><br>	
I went with the earliest stable still maintained version (5.5.36), as i do not need anything flash 
at this point (or at least am not aware of the need) and do not want to complicate things unless I have to.
<br><br>
Although you can of course get most things from an apt repository,I have preferred to install from php (and others) from 
scratch, as it will give more flexibility to link more extensions in statically down the track, control
precise config and generally is a better way to learn what's going on under the hood (providing you have
the time and patience). We will need to build in other extensions like Curl, OpenSSL etc later and we 
will come back to this then
<br><br>
The 2 main pieces of software we are going to install are <a href="#php">php</a> and <a href="#apache">apache</a>
both of which actually depend on each other. So in tackling php first we will need some basics of apache in place
so will have to duck and dive a bit.

<p><a href="#toc">Back to menu</a></p>
</div>