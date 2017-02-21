requirejs.config({
    baseUrl: 'js/lib',
    paths: {
       app: '../app'
    }
});

requirejs(['myutils','jquery'],
	function (myutils,$) {
		$(document).ready(function(){
			setcontextmenu("div[id='wrap']","macro_updateid");

			var init_values = Array();
						
			$("input").keypress(function (e) { // get content from server on RETURN press
	 			var key = e.which;
				if(key == 13)  { // the enter key code 
					var parentel=$(this).closest("div");
					
				   makeGetDetailsRequest($(this).val(),drawform_multi,parentel);
		 			setTimeout(function() { 	init_values = getElementValues("select");},200); // store init values so can detect fields that have changed
				 }
			});
			
			$("input[id='" + Globals.editbutton + "']").on('click',function(){ 		
					var id = $("input[id='edit_source_value']").val();
					var parentel=$(this).closest("div");
					var value_changes = getElementValueChanges("select",init_values,parentel); // compare with init to get what has changed

					makeUpdateRequest(value_changes,id,alertme);
			});   
		});
	}
);
	