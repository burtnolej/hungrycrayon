
var ztypes = new Array();
var url = "";

$(window).load(function(){
	//$(document).ready(function(){
	console.log("foobar")
	url = buildurl();
 	console.log(url);
 	get(url);
});

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

function get(url) {
	console.log(url);
	window.location = url;
}