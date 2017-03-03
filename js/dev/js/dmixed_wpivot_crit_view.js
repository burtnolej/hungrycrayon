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
			var init_values = Array();
			
			// set context menu
			//setcontextmenu("ul[class='nav']"); 
			setcontextmenu("div[id='wrap']","macro_updateid");
			
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
		 	
			// get EDIT content from server on RETURN press
			$("input").keypress(function (e) { 
	 			var key = e.which;
				if(key == 13)  { // the enter key code 
					var parentel=$(this).closest("div");
					
				   makeGetDetailsRequest($(this).val(),drawform_multi,parentel);
		 			setTimeout(function() { 	init_values = getElementValues("select",parentel);},200); // store init values so can detect fields that have changed
				 }
			});
			
			// scrape values and submit edit to server
			$("input[id='" + Globals.editbutton + "']").on('click',function(){ 		
					var id = $("input[id='edit_source_value']").val();
					var parentel=$(this).closest("div");
					var value_changes = getElementValueChanges("select",init_values,parentel); // compare with init to get what has changed

					makeUpdateRequest(value_changes,id,alertme);
			});  
			
			// redraw if any non edit/new selects are changed (ie draw pivot))
			// but need to scrape across divs/popouts to get fil
			//$("select, input[type!='text']").on('change',function(){
				
				
			$("body").on("change","select, input[type!='text']",function(){		   
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
				
		   		if (!$(this).hasClass("new")) {
		   			if (!$(this).hasClass("edit")) {
		   				//if (!$(this).hasClass("view")) {
		   				
		   				url = "http://".concat(Globals.server_name,"/",Globals.script_name,"?");
			   			url = url + getAllInputValues('ztypes',['qunit-filter-input']);
			   					
		   				if ($(this).hasClass("view")) {
		   					if (this.id == "source_value") {
				   				window.location = url;
				   			}
			   			}
			   			else {
			   				console.log(url);
			   				window.location = url;
			   			}
			   		}
			   	}
		   });	 
		   
			$("input[id='" + Globals.viewbutton + "']").on('click',function(){ 		
				_async_redraw(400);	  		
			});
		});
	}
);