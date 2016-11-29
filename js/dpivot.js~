var ztypes = new Array();
var url = "";

$(document).ready(function(){
   $("select, input").on('change',function(){
   	
   	url = "http://".concat(Globals.server_name,"/",Globals.script_name,"?");
   	
   	ztypes = new Array();
   		
   	$('select').each(function (index, value) {
   		url = url + this.id + "=" + this.value + "&";
    	});
    		
      $('input').each(function (index, value) {    			
  			if (this.checked == true) {
  				ztypes.push(this.id);	
  			}	
    	});
    		
    	url = url + "ztypes=" + ztypes.join();
    	//console.log(url);
    	get(url);
   });
});

function get(url) {
	console.log(url);
	window.location = url;
}