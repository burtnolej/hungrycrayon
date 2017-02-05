requirejs.config({
    baseUrl: 'js/lib',
    paths: {
       app: '../app'
    }
});

requirejs(['myutils','jquery'],
	function (myutils,$) {
		$(document).ready(function(){
			
			var initvalues = getElementValues("select");
			var results = Array();
					
			// first check if this is event is a submit button press
			$("input[name='button']").on('click',function(){
				
				url = buildurl();
				url = url + "&page_status=submit";
				
				// add the changes to 
				results = getElementValueChanges("select",initvalues);
				url = url + "&value_changes="+results.join(",");
				window.location = url;
			});
				
			$("select, input").on('change',function(){
				// if the element that changed is on the watchlist redraw the page
				if (Globals.watch_list.indexOf(this.id)  != -1) {
					url = buildurl();
		 			window.location = url;
				}
		 	});
		});
	}
);