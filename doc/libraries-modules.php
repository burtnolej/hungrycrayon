<!DOCTYPE html>
<html>
<head>
<style>

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

<?php require_once("navigator.html") ?>


<div id="content">
<div id="libxml">
<h3>libxml</h3>

The <a href=http://xmlsoft.org/downloads.html>XML C parser and toolkit</a>of Gnome

<p><a href="#ul">Back to menu</a></p>
</div>
<!---------------------------------------------------------------------------------->
<!---------------------------------------------------------------------------------->
<div id="readline">
<h3>readline</h3>

The <a href=https://cnswww.cns.cwru.edu/php/chet/readline/rltop.html>GNU Readline library</a> provides a set of functions for use by applications that allow users to edit command lines as they are typed in. Both Emacs and vi editing modes are available. The Readline library includes additional functions to maintain a list of previously-entered command lines, to recall and perhaps reedit those lines, 
and perform csh-like history expansion on previous commands.<br><br>

I used apt to fetch 'sudo apt-get install libreadline-dev'. 

<p><a href="#ul">Back to menu</a></p>
</div>
<!---------------------------------------------------------------------------------->
<!---------------------------------------------------------------------------------->
<div id="phpini">
<h3>php.ini</h3>


<p><a href="#ul">Back to menu</a></p>
</div>
<!---------------------------------------------------------------------------------->
<!---------------------------------------------------------------------------------->
<div id="mysql">
<h3>MySQL</h3>

    Allows PHP to query MySQL. This is an essential feature (I think). You will need to have MySQL 
    installed to enable this option.
    
<p><a href="#ul">Back to menu</a></p>
</div>
<!---------------------------------------------------------------------------------->
<!---------------------------------------------------------------------------------->
<div id="buildessentials">
<h3>build-essentials</h3>

The build-essentials is a reference for all the packages needed to compile a debian package. 
It generally includes the gcc/g++ compilers an libraries and some other utils

sudo apt-get install build-essential  
    
<p><a href="#ul">Back to menu</a></p>
</div>
<!---------------------------------------------------------------------------------->
<!---------------------------------------------------------------------------------->
<div id="pcre">
<h3>pcre</h3>

perl compaitble regular expressions
ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/
    
<p><a href="#ul">Back to menu</a></p>
</div>
<!---------------------------------------------------------------------------------->
<!---------------------------------------------------------------------------------->
<div id="zlib">
<h3>zlib</h3>

So that Apache can compress output to browsers that support it, we’re going to install Zlib first of all:

http://www.zlib.net/zlib-1.2.3 usual method for install
    
<p><a href="#ul">Back to menu</a></p>
</div>
<!---------------------------------------------------------------------------------->
<!---------------------------------------------------------------------------------->
<div id="apxs">
<h3>zlib</h3>

    APXS is for configuring compilation of an Apache module, this is required if you want to build mod_php.
    It is build as part of the apache 2.0 distribution and can be found in /usr/local/bin
    
<p><a href="#ul">Back to menu</a></p>
</div>
<!---------------------------------------------------------------------------------->
<!---------------------------------------------------------------------------------->
<div id="apr">
<h3>Apache Portable Runtime</h3>

    tar -xvf apr-1.5.2.tar.gz
tar -xvf apr-util-1.5.4.tar.gz 


./srclib as apr / apr-lib

<p><a href="#ul">Back to menu</a></p>
</div>
<!---------------------------------------------------------------------------------->
<!---------------------------------------------------------------------------------->
<div id="modphp">
<h3>mod-php</h3>

Is an Apache extension that is specified in httpd.conf and loaded at runtime. It is used by the web
server to parse and execute php code in web pages.

It is created during build of PHP by specifying the --with-apxs directive.


<p><a href="#ul">Back to menu</a></p>
</div>
