<html>
<head>
<style>
#content {
    background-color:#eeeeee;
    <!--width:800px;>
    float:left;
    text-align:left;
    padding:10px;
    border: 3px solid #73AD21;
    <!margin: auto;>
}
</style>
</head>
<div id="content">

<?php require_once("navigator.html") ?>

<!---------------------------------------------------------------------------------->
<!---------------------------------------------------------------------------------->
<div name="php" id="php">
<h3>Building and Configuring PHP</h3>
<p>Usual build process of ./configure; make; sudo make install</p>
<!---------------------------------------------------------------------------------->
<h4 name ="phpdependencies" id ="phpdependencies">PHP dependencies</h4>
<p>
Depending on your OS flavour, required dependencies will vary greatly (sigh). I needed to get python libs/includes and <a href="#libxml">libxml</a> and I also needed <a href="#readline">readline</a> to enable php interactive mode (php -i); this is not linked in by default (see below). Cant understand why this doesnt come as default - the binary is called php-cli for command-line-interface after all.
</p>
<!---------------------------------------------------------------------------------->
<h4 name ="buildphp" id ="buildphp">Building PHP</h4>
<p>
You need to specify 2 directives for configure; <a href="#readline">readline</a> as just discussed and also to be explicit about where we want the main php config file to be located (<a href="#phpini">php.ini</a>).We will need to move the file there later on in the process.
<br><br>
So the command i used looked like this:
<br>
<br>
<tab2>./configure --with-config-file-path=/etc <br>
<tab3-5>  --with-readline</tab1><br>
<tab3-5>  --with-apxs=/usr/local/apache2/bin/apxs</tab1>//<br> 
<tab3-5>  --with-mysql</tab1><br>
<br>
apxs gives this option and creates /usr/local/apache2/modules/libphp5.so
<br>
</p>
<!---------------------------------------------------------------------------------->
<h4 name ="configurephp" id ="configurephp">Configuring PHP</h4>
<p><a href ="#phpini">php.ini</a> is the main one, many others can be specified. for instance, apache will use its own php.ini. for the time being i just create one and then put symlinks if an instance is needed under a different tree. 
</p>
<!---------------------------------------------------------------------------------->
<h4 name ="troubleshootingphp" id ="troubleshootingphp">Troubleshooting PHP</h4>
<p>
If you see an error complaining that phar is not enabled (PEAR package PHP_Archive not installed: generated phar will require PHP's phar extension be enabled), after you have run make - ignore it, phar will work just fine.

Make sure that any old php.ini's are removed before installing as i found they do not always get overwritten which can be confusing
</p>
<!---------------------------------------------------------------------------------->
<h4 name ="testphp" id ="testphp">Testing PHP works</h4>
<p>B
asic test to make sure it works would be to run php -a and you should get a command line prompt. But obviously the main point here is to enable php through a web server backend so lets move to that part
</p>
<p><a href="#toc">Back to menu</a></p>
</div>
<!---------------------------------------------------------------------------------->
<!---------------------------------------------------------------------------------->
<div name="apache" id="apache">
<h3>Building an installing Apache 2.0</h3>

ServerName 192.168.1.201:80

sudo kill -TERM `cat /usr/local/apache2/logs/httpd.pid`

I needed to install 

<a href="#buildessentials">build-essentials</a>
<a href="#zlib">zlib</a>
<a href="#pcre">pcre</a>

<br>
<tab2>./configure --prefix=/usr/local/apache2</tab2><br> 
<tab3-5>--enable-mods-shared=all</tab3-5><br> 
<tab3-5>--enable-deflate </tab3-5><br> 
<tab3-5>--enable-proxy </tab3-5><br> 
<tab3-5>--enable-proxy-balancer</tab3-5><br> 
<tab3-5>--enable-proxy-http</tab3-5><br> 
<tab3-5>--with-included-apr</tab3-5><br> 
<br>
<!---------------------------------------------------------------------------------->
<h4 name="httpdvapache" id ="httpdvapache">HTTPD vs Apache2</h4>
If like me, you were confused by why apache installed from apt resulted in an apache2 binary but build from source results in httpd, they are indeed the exact same product, just built with different directives. So the directives above are in line with what is used to create the bins in the apt-cache
<br>
<br>
<!---------------------------------------------------------------------------------->
Make sure you run <a href="#ldconfig">ldconfig</a>
<h4 name ="ldconfig" id ="ldconfig">ldconfig</h4>
<br>
<br>
<!---------------------------------------------------------------------------------->
<h4 name ="linkedinmodules" id ="linkedinmodules">HTTPD vs Apache2</h4>
apache2 -l
Compiled in modules:
  core.c
  mod_so.c
  mod_watchdog.c
  http_core.c
  mod_log_config.c
  mod_logio.c
  mod_version.c
  mod_unixd.c
  <br>
<br>
<!---------------------------------------------------------------------------------->

<i>start/stop</i>
sudo /usr/local/apache2/bin/apachectl start
sudo /usr/local/apache2/bin/apachectl stop
sudo /usr/local/apache2/bin/apachectl restart
<i>logs</i>

/usr/local/apache2/logs

start/stop
<!---------------------------------------------------------------------------------->
<h4 name ="makingsureitworks" id ="makingsureitworks">Making sure it works</h4>
<br> 
put this in the browser of your phone - http://192.168.1.216/test.php 
<!---------------------------------------------------------------------------------->
<h4 name ="troubleshooting" id ="troubleshooting">Troubleshooting</h4>

<table  border="1"  style="width:100%">
  <tr>
    	<td>[UFW BLOCK] in client browser syslogs</td>
    	<td>sudo ufw allow from <xx.xx.xx.xx> to any port 22</td>
   </tr>
   <tr>
    	<td>[authz_core:error] in Apache logs</td> 
    	<td>make sure authz_core_module specified in <a href="#htmldconf">httpd.conf</a></td>
   </tr>
  <tr>
    	<td>[core:crit]: Configuration Failed in Apache logs</td>
    	<td>make sure unixd_module specified in <a href="#htmldconf">httpd.conf</a></td>
   </tr>
</table> 
<!---------------------------------------------------------------------------------->
<!---------------------------------------------------------------------------------->
<h4 name="proxyserver" id="proxyserver">Proxy Server</h3>  	

LoadModule proxy_module		"/usr/local/apache2modules/mod_proxy.so"
LoadModule proxy_connect_module "/usr/local/apache2modules/mod_proxy_connect.so"
LoadModule proxy_http_module 	"/usr/local/apache2modules/mod_proxy_http.so"


Apache HTTP Server can be configured in both a forward and reverse proxy (also known as gateway) mode.

An ordinary forward proxy is an intermediate server that sits between the client and the origin server. In order to get content from the origin server, the client sends a request to the proxy naming the origin server as the target. The proxy then requests the content from the origin server and returns it to the client. The client must be specially configured to use the forward proxy to access other sites.

A typical usage of a forward proxy is to provide Internet access to internal clients that are otherwise restricted by a firewall. The forward proxy can also use caching (as provided by mod_cache) to reduce network usage.

The forward proxy is activated using the ProxyRequests directive. Because forward proxies allow clients to access arbitrary sites through your server and to hide their true origin, it is essential that you secure your server so that only authorized clients can access the proxy before activating a forward proxy.

ProxyRequests On
ProxyVia On
#ProxyPass / http://bumblebee:80/
#ProxyPass / http://192.168.1.216/

<Proxy "*">
        Require all granted
	#Require host 192.168.1.199
</Proxy>



Chain INPUT (policy ACCEPT)
target     prot opt source               destination         
ACCEPT     all  --  anywhere             anywhere            

Chain FORWARD (policy ACCEPT)
target     prot opt source               destination         

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination 


then i used on apache server as a proxy and one as an app server

works
<!---------------------------------------------------------------------------------->
<h3 name=logverbosity id=logverbosity>Log Verbosity</h3>  	

trace8 gives you everything

<p><a href="#ul">Back to menu</a></p>
</div>

<!---------------------------------------------------------------------------------->
<!---------------------------------------------------------------------------------->
<div id="PHP Debugger (phpdbg)">
<h3>phpdbg</h3>

<!---------------------------------------------------------------------------------->
<h4 name="buildingphpdbg" id ="buildingphpdbg">Building phpdbg</h4>
1st snag of trying to be clever by keeping to a simple/stable/old version of php is the lack of a shipped debugger. <a href=http://phpdbg.com/>phpdbg</a> is a nice simple/familiar/function answer but doesnt ship with the php dist until 5.6. So 

The build instructions are a little obfuscative an involving an incremental build ontop of build php once the phpdbg source has been put under the php dist. I had success with rebuilding php from scratch but including the phpdbg switch

<tab2>cd /usr/src/php-src/sapi</tab2><br>
<tab2>git clone https://github.com/krakjoe/phpdbg</tab2><br>
<tab2>cd ..</tab2><br>
<tab2>./configure --with-config-file-path=/etc </tab2><br>
<tab3-5>  --with-readline</tab3-5><br>
<tab3-5>  --with-apxs=/usr/local/apache2/bin/apxs</tab3-5>//<br> 
<tab3-5>  --with-mysql</tab3-5><br>
<tab3-5>  --enable-phpdbg</tab3-5><br>
<tab2>make install</tab2><br>
<!---------------------------------------------------------------------------------->
<h4 name="usingphpdbg" id ="usingphpdbg">Using phpdbg</h4>

launch with phpdbg <filename>

in general type help <command> for some really useful help

here are some basics (alias in brackets):

info vars // list all vars declared
info funcs // list all vars declared
break(b) #
break(b) if $var == $cond // break when a condition is met
list(l) l 2 // list next 2 lines
list(l) func(l) $funcname // list the implementation of a func
list(l) method(m) $class::$method // list a class member function
step s
eval ev $var // get current value of $var 
eval ev $var="foobar" // set a var to a new value during execution


<p><a href="#ul">Back to menu</a></p>
</div>



</div>
</html>
