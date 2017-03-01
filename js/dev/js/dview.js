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
							
			$("body").on("change","select",function(){ 
				if ($(this).hasClass("view")) {
					var parentel=$(this).closest("div");
					if (this.id == 'source_type') {
						if ($('#subtmpdiv').length) {$('#subtmpdiv').remove();}
						var tmpdiv = addElement("div","subtmpdiv",{hidden:false,parentel:parentel});
	
						url = "http://localhost:8080/refdata/"+this.value + "?tag=source_value";
						makeRequestResponse(url,drawform_multi,tmpdiv);
					}
					else if (this.id == 'view_type') {
						makeViewForm(this.value,parentel);
					}
				}
			});

			$("input[id='" + Globals.viewbutton + "']").on('click',function(){ 		
				//_add($(this),Array(Globals.newbutton,"source_value"));
				_async_redraw(400);	  		
	  			//$("select[id='objtype").val('NotSelected');
			});
		   
		});
	}
);