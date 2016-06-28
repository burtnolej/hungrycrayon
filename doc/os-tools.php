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

<?php require_once("navigator.html") ?>


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

<!---------------------------------------------------------------------------------->
<!---------------------------------------------------------------------------------->
<div id="xwin">
<h3>X Windows</h3>

<h4>displaying X apps on a remote display</h4> 
<tab3-5>xhost +<\tab3-5><br>
<tab3-5>export DISPLAY=blackbear:0<\tab3-5><br>
	   
<p><a href="#ul">Back to menu</a></p>
</div>
<!---------------------------------------------------------------------------------->
<!---------------------------------------------------------------------------------->
<div id="kde">
<h3>kde</h3>  	

<h4>easy resize of windows</h4> 	

Hold the Alt+Key and just click right mouse button anywhere 
in the window.
	   
<p><a href="#ul">Back to menu</a></p>
</div>
<!---------------------------------------------------------------------------------->
<!---------------------------------------------------------------------------------->
<div id="bluefish">
<h3>kde</h3>  	

Document\Wrap Text:On
Document\Line Numbers:Off

<p><a href="#ul">Back to menu</a></p>
</div>
<!---------------------------------------------------------------------------------->
<!---------------------------------------------------------------------------------->
<div id="wpsetup">
<h3>wpsetup</h3>  	

http://192.168.1.216/wordpress/index.php

cp wp_config_sample.php wp_config.php
http://192.168.1.216/wordpress/index.php

ln ~/Development/wordpress /var/www/html/wordpress
<p><a href="#ul">Back to menu</a></p>
</div>
<div id="xprop">
<h3>xprop</h3>  	

dumps all the X properties of the specified window

xprop -name -set WM_CLASS allows you to set WM_CLASS which can be picked up by kwinrules


<p><a href="#ul">Back to menu</a></p>
</div>
<!---------------------------------------------------------------------------------->
<!---------------------------------------------------------------------------------->
<div id="kdeautostart">
<h3>KDE Autostart</h3>  	

any binary in the .kde/Autostart directory will get launched; so if trying to run 2 firefoxes
and put them in different locations; put a link to firefox in there and a script called whatever


#!/bin/sh

// need to sleep to make sure first instance is launched otherwise new-window directive does not
// work properly
sleep 3

// tells kde which desktop to use
// new window directive allows you create another firefox window instance - othewise tries
// to start 2 full apps which is not allowed

kstart --desktop 1 /usr/bin/firefox -new-window www.google.com &

#/usr/bin/firefox -new-window www.google.com &
sleep 3

// need to try to give the new window a different name so that the config in kwinrulesrc can
// pick it out. can specify by class
<p><a href="#xprop">xprop</a></p> -name "Google - Mozilla Firefox" -f WM_CLASS 8s -set WM_CLASS "
Foobar"

problem is that the class is being set too late - after windows config has been applied

am looking for ways to rebuild each app so can specify WM_CLASS to use at launch time

<p><a href="#ul">Back to menu</a></p>
</div>
<!---------------------------------------------------------------------------------->
<!---------------------------------------------------------------------------------->
<div id="kdeconfig">
<h3>KDE Config</h3>  	

System Settings \ Global Keyboard SHortcuts \ Kwin

Window to desktop 1 - Ctrl+Shift+F1
Window to desktop 2 - Ctrl+Shift+F2 

Keep window on all desktops - Ctrl+Shift+PrintScreen

Ctrl+11 = SHow desktopn grid

See windowss on all deskto
Meta + / Meta - to zoom



all desktop top right nvpy
all desktop bottom right firefox/chromium

personal planning
1 desktop top left librecalc resume-tags
1 desktop bottom left librecalc resume-tags
1 desktop top middle librecalc resume-tags
1 desktop bottom middle left librecalc resume-tags

system
2 desktop top left konsole
2 desktop bottom left konsole
2 desktop top middle konsole
2 desktop bottom middle konsole

dev
3 bluefish left konsole
3 bluefish middle konsole

blog
6 bluefish left blog.html
<p><a href="#ul">Back to menu</a></p>
</div>
<!---------------------------------------------------------------------------------->
<!---------------------------------------------------------------------------------->
<div id="ldconfig">
<h3>ldconfig</h3>  	

Basically accomplishes the same thing as LD_LIBRARY_PATH but is more permanent and more ubiqutous as shared lib locations are persisted in ld.so.cache and system-wide, so no reliance on a temp login shell env. This was useful for me because apache was built as me but then would run as root. The cache is then used by the os level runtime linker.

ldconfig is clever in that it figures out what shared libs have been recently added and trys to determine ELF types

<p><a href="#ul">Back to menu</a></p>
</div>



<!---------------------------------------------------------------------------------->
<!---------------------------------------------------------------------------------->\
<div id="apt">
<h3>apt</h3>  	

Is essentially a front end to <p><a href="#dpkg">dpkg</a></p>; it provides the ability
to retreive software from various repositories then relys on dpkg (on debian based platforms)
to configure and install

apt-cache seach <package name> // " wildc*rds" work

<h4>troubleshooting</h4>
got me out of a funky dpkg state
sudo apt-get -m --reinstall install python python-minimal dh-python

<p><a href="#ul">Back to menu</a></p>
</div>

<!---------------------------------------------------------------------------------->
<!---------------------------------------------------------------------------------->\
<div id="dpkg">
<h3>dpkg</h3>  	

Higher level tool than <p><a href="#configure">configure</a></p> but lower level than
other higher level tools like <p><a href="#apt">apt</a></p>

dpkg installed debian style packages (.deb) onto a computer




  PKG_CONFIG_PATH
              directories to add to pkg-config's search path
  PKG_CONFIG_LIBDIR
              path overriding pkg-config's built-in search path
  --instdir=<directory>      Change installation dir without changing admin dir.
dpkg --list shows all packages
dpkg -L libxml2-dev | grep .pc

              
<p><a href="#ul">Back to menu</a></p>
</div>

<!---------------------------------------------------------------------------------->
<!---------------------------------------------------------------------------------->
<div id="configure">
<h3>configure</h3>  
<!---------------------------------------------------------------------------------->
<!---------------------------------------------------------------------------------->
Simply put, configure matches the libraries on the build machine with the ones the 
program requires before compiling. It also can manage priority and hierarchy and
dependencies. So it will use the best possible option and only give a failure when
it has to.

<h4> Troubleshooting </h4>
configure creates a config.log after each run which is is useful to get more info if
a failure has occurs. Either through looking at configure --help or inspecting the script
itself you can find the set of switches available for this particular app so if
there is a dependency that is hard to resolve but would provide functionality that
you dont need, you can exclude it 

./configure --disable-python to stop getting zend build error

<p><a href="#ul">Back to menu</a></p>
</div>
<!---------------------------------------------------------------------------------->
<!---------------------------------------------------------------------------------->

<div id="pkg-config">
<h3>pkg-config</h3>  	

pkg-config is a tool that helps you when compiling apps and libraries. via the use of 
meta-data files *.pc; the app developer is giving hints to the build system on what compiler
options are required to build. this prevents the need to hard code references to dependencies.
pkg-config is used by higher level functions like <p><a href="#configure">configure</a></p>
to manage dependencies

<h4> Troubleshooting </h4>
The only issue i have come across using this is when pkg-config (usually being invoked via
<p><a href="#configure">configure</a></p>) cannot find a .pc file. This is easilly 
resolved when the file is located by appending its path to PKG_CONFIG_LIBDIR

<h4> Example meta data file; pango.pc</h4>

In this example, pango.pc was actually in location /usr/lib/x86_64-linux-gnu/pkg-config.
The config file tells pkg-config that the required libraries are in /usr/lib/x86_64-linux-gnu
and includes/c-files are in /usr/include


<table  border="1"  style="width:100%">
  <tr>
    	<td>prefix</td>
    	<td>/usr</td>
   </tr>
   <tr>
    	<td>exec_prefix</td> 
    	<td>${prefix}</td>
   </tr>
   <tr>
    	<td>libdir</td>
    	<td>usr/lib/x86_64-linux-gnu</td>
	</tr>
  	<tr>	  
    	<td>includedir</td>
    	<td>${prefix}/include</td>
  	</tr>
	<tr>
    	<td>pango_module_version</td>
    	<td>1.8.0</td>
  	</tr>
   	<tr>
    	<td>Name</td>
    	<td>pango</td>
	</tr>
  	<tr>
    	<td>Description</td>
    	<td>Internationalized text handling</td>
	</tr>
  	<tr>    
	 	<td>Version</td>
    	<td>1.36.3</td>
    </tr>
  	<tr>    
	 	<td>Requires</td>
    	<td>glib-2.0 gobject-2.0</td>
    </tr>
  	<tr>    
	 	<td>Requires.private</td>
    	<td>gmodule-no-export-2.0</td>
    </tr>
  	<tr>    
	 	<td>Libs</td>
    	<td>-L${libdir} -lpango-1.0 </td>
    </tr>
  	<tr>    
	 	<td>Cflags</td>
    	<td>-I${includedir}/pango-1.0</td>
    </tr>
</table>
</div>