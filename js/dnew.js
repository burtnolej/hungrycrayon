
var ztypes = new Array();
var url = "";

$(document).ready(function(){
	
	// first check if this is event is a submit button press
	//$("input").on('click',function(){
	$("input[name='button']").on('click',function(){
		
		console.log("first");
		url = buildurl();
		
		url = url + "&page_status=submit";
		get(url);
	});
		
	//$("select, input").on('change',function(){
	$("select").on('change',function(){

		// if the element that changed is on the watchlist redraw the page
		
		console.log("second");


		if (Globals.watch_list.indexOf(this.id)  != -1) {
			url = buildurl();
 			get(url);
		}
 	});
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