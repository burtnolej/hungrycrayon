

var ztypes = new Array();
var url = "";

function buildurl() {
 	url = "http://".concat(Globals.server_name,"/",Globals.script_name,"?");
   	
   	ztypes = new Array();
   		
   	$('select').each(function (index, value) {
	   		url = url + this.id + "=" + this.value + "&";
	   });
	    		
	  $('input').each(function (index, value) {    			
	  		if (this.checked == true) {
	  			ztypes.push(this.id);	
	  		}
	  		else {
	  			url = url + this.id + "=" + this.value + "&";
	  		}
	   });
    		
    	url = url + "ztypes=" + ztypes.join();
  return url
}

$(document).ready(function(){
   $("select, input").on('change',function(){
    	url = buildurl();
    	//console.log(url);
    	get(url);
   });
   
});

function get(url) {
	console.log(url);
	window.location = url;
}

function alertme() {
	alert("foo you");
}

function importlib(src) {
	var imported = document.createElement("script");
	imported.src = src;
	document.head.appendChild(imported);	
}