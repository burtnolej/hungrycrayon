requirejs.config({
    baseUrl: 'js/lib',
    paths: {
       app: '../app'
    }
});

requirejs(['myutils','jquery'],
	function (myutils,$) {
		$(document).ready(function(){
			// set context menu
			//setcontextmenu("div[id='wrap']");
			setcontextmenu("div[id='wrap']","macro_updateid");

		var init_values = Array();
					
			
		$("input").keypress(function (e) {
 			var key = e.which;
			 if(key == 13)  // the enter key code
			 {
			  	var url = "http://localhost:8080/id/" + $(this).val() + "?";
			  	
		   		var parentel=$(this).closest("div");

				if ($('#tmpdiv').length) {
					$('#tmpdiv').remove();
				}
					
				var tmpdiv = addElement("div","tmpdiv",{hidden:false,parentel:parentel});

				makeRequestResponse(url,drawform_multi,tmpdiv);
				
	 			setTimeout(function() { 	
	 				init_values = getElementValues("select");		
	  			},200);
				
			 }
		});
		
		// first check if this is event is a submit button press
		$("input[id='submitfoo']").on('click',function(){
				
				id = $("input[id='source_value']").val();
				var url = "http://localhost:8080/update/"+id+"?value_changes=";
				
				pel = $(this).closest("div");
				//pel.find("select").each(function() {
				//		url = url + this.name + "," + this.value;
				//});

				// need to pass in pel
				
				var value_changes = getElementValueChanges("select",init_values);
				
				url = url +  value_changes.join(",");
				
				//console.log(url);

				makeRequestResponse(url,alertme);

	 			/*setTimeout(function() { 			
			   		pageurl = buildurl();
			   		console.log(url);
			   		window.location = pageurl;
	  			},400);	*/
	  		
	  			//$("select[id='objtype").val('NotSelected');
			});
			   
	});
});
	