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

<?php 

	require_once("navigator.html");
	function httpdconf() {?>
 		<html><div id="content"><div id="htmldconf">
		<h3>httpd.conf</h3>
		
		<p>Apaches main configuration file. Changes i made were:</p>
		<br><br>
		
		<table  border="1"  style="width:100%">
		  <tr>
		    	<td>ServerRoot</td>
		    	<td>/usr/local/apache2</td>
		    	<td></td>
		   </tr>
		   <tr>
		    	<td>Listen</td> 
		    	<td>xx.xx.xx.xx:80</td>
		    	<td></td>
		   </tr>
		   <tr>
		    	<td>LoadModule</td>
		    	<td>authz_core_module</td>
			 	<td>/usr/local/apache2/modules/mod_authz_core.so</td>
			</tr>
		  	<tr>	  
		    	<td>LoadModule</td>
		    	<td>unixd_module</td>
			 	<td>/usr/local/apache2/modules/mod_unixd.so</td>    
		  	</tr>
			<tr>
		    	<td>LoadModule</td>
		    	<td>php5_module</td>
			 	<td>/usr/local/apache2/modules/libphp5.so</td>
		  	</tr>
		  	<tr>
		    	<td>ServerName</td>
		    	<td>xx.xx.xx.xx:80</td>
		    	<td></td>
			</tr>
		  	<tr>    
			 	<td>DocumentRoot</td>
		    	<td>/var/www/html</td>
		    	<td></td>
		    </tr>
		</table>
		
		<p>	&#60;Directory "/var/www/html/"</p>
		
		<table  border="1"  style="width:100%;table-layout: fixed">
		  <tr>
		    	<td style="width: 125px">Options</td>
		    	<td style="width: 125px">Indexes</td>
		    	<td style="width: 125px">FollowSymLinks</td>
		    	<td style="word-wrap:break-word";colspan="1">http://httpd.apache.org/ docs/2.4/mod/core.html#options</td>
		    	<td style="word-wrap:break-word";colspan="1">"None", "All", FollowSymLinks SymLinksifOwnerMatch ExecCGI MultiViews</td>
		   </tr>
		  <tr>
		    	<td>AllowOverride</td>
		    	<td>None</td>
		    	<td></td>
		    	<td>Controls what directives may be placed in .htaccess files.</td>
		    	<td>"All", "None" AllowOverride FileInfo AuthConfig Limit</td>
		   </tr>
		  <tr>
		    	<td>Require</td>
		    	<td>all</td>
		    	<td>granted</td> 
		     	<td>Controls who can get stuff from this server.</td>
		      	<td></td>
		   </tr>    
		</table>
		<p>	&#62;/Directory><br>
		   
		<p><a href="#ul">Back to menu</a></p>
		</div></div></html>

<?php	}	
	function htmllists() {?>
	
		<html><div id="content"><div id="htmllists">
		<h3>HTML Lists</h3>  
		<ul>
		  <li>Coffee</li>
		  <li>Tea
		    <ul>
		      <li>Black tea</li>
		      <li>Green tea</li>
		    </ul>
		  </li>
		  <li>Milk</li>
		</ul>
		<p><a href="#ul">Back to menu</a></p>
		</div></div></html>
<?php	}	
	function htmltable() {?>		

		<html><div id="content"><div id="HTML Table">
		<h3>htmltable</h3>  
		
		<table  border="1"  style="width:50%;table-layout: fixed">
		  <tr>
		    <td style="width: 125px">Jill</td>
		    <td>Smith</td> 
		    <td>50</td>
		  </tr>
		  <tr>
		    <td style="word-wrap:break-word";colspan="1">Eve Eve Eve Eve Eve Eve Eve Eve Eve Eve Eve Eve Eve Eve Eve</td>
		    <td>Jackson</td> 
		    <td>94</td>
		  </tr>
		</table>
		<p><a href="#ul">Back to menu</a></p>
		</div></div></html>
<?php	}	
	function htmlescaping() {?>	
	
		<html><div id="content"><div id="HTML Escaping">
		<h3>htmlescape</h3>  
		
		<table  border="1"   style="width:25%">
		  <tr>
		    <td>&#60</td>
		    <td>&amp;#60</td> 
		  </tr>
		  <tr>
		    <td>&#62</td>
		    <td>&amp;#62</td> 
		  </tr>
		  <tr>
		    <td>&#61</td>
		    <td>&amp;#61</td> 
		  </tr>
		</table>
		<p><a href="#ul">Back to menu</a></p>
		</div>
		
<?php	}	
	function htmllinks() {?>	
	
		<html><div id="content"><div id="HTML Linking">
		<h3>htmllinks</h3>  
		
		<h4 name ="makingsureitworks" id ="makingsureitworks">Making sure it works</h4>
				      <li><a href="build-install.html#makingsureitworks">Making sure it works</a></li>  
		
		<p><a href="#ul">Back to menu</a></p>
		</div></div></html>
		
<?php }
	if (isset($_GET['arg'])) {
  		$funcname = $_GET['arg'];
		call_user_func($funcname);
  	}
?>