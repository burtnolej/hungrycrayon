requirejs.config({
    baseUrl: 'js/lib',
    paths: {
       app: '../app'
    }
});

requirejs(['myutils','jquery'],
	function (myutils,$) {
		
		var ztypes = new Array();
		var url = "";
		
		$(document).ready(function(){
			// first check if this is event is a submit button press
			$("input[name='button']").on('click',function(){
				url = buildurl();				
				url = url + "&page_status=submit";
				window.location = url;
			});
				
			$("select").on('change',function(){		
				// if the element that changed is on the watchlist redraw the page
				if (Globals.watch_list.indexOf(this.id)  != -1) {
					url = buildurl();
		 			window.location = url;
				}
		 	});
		});
	}
);