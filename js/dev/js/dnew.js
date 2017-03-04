requirejs.config({
    baseUrl: 'js/lib',
    paths: {
       app: '../app'
    }
});

function _add(_this,exclude) {
	var url = "";
		
	_this.closest("div").find("select").each(function() {
		if (!exclude.contains(this.id)) { // ignore source_value select
			url = url + this.name + "=" + this.value + "&";
		}	
	});
	
	_this.closest("div").find("input").each(function() {
		if (!exclude.contains(this.id)) { 
			url = url + this.name + "=" + this.value + "&";
		}
	});

	makeAddRequest($("select[id='objtype").val(),url,alertme)
}

function _async_redraw(delay) {
	setTimeout(function() { 			
		pageurl = buildurl();
		window.location = pageurl;
  	},delay);	
}

requirejs(['myutils','jquery'],
	function (myutils,$) {
		var url = "";		
		$(document).ready(function(){
			
			// set context menu
			setcontextmenu("ul[class='nav']"); 
			
			//  scrape values and submit new to server		
			$("input[id='" + Globals.newbutton + "']").on('click',function(){ 		
				_add($(this),Array(Globals.newbutton,"source_value"));
				_async_redraw(400);	  		
	  			$("select[id='objtype").val('NotSelected');
			});
			
			// get content from server on objtype selection
			$("select").on('change',function(){ 
		   		if ($(this).hasClass("new")) {
		   			var parentel=$(this).closest("div");
					makeGetNewForm(this.value,parentel)
				}
		 	});
		});
	}
);