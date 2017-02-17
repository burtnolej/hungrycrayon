
requirejs.config({
    baseUrl: 'js/lib',
    paths: {
       app: '../app'
    },
    shim: {
        'myutils': {
            deps: ['jquery'],
            exports: 'myutils'
        },
	}, 
});


define(['myutils'], function(myutils) {    	

		$(document).ready(function(){

			setcontextmenu("div[id='wrap']","macro_updateid");
			
		   $("select, input").on('change',function(){
		   		url = "http://".concat(Globals.server_name,"/",Globals.script_name,"?");
		   		url = url + getAllInputValues('ztypes',['qunit-filter-input']);

		    	console.log(url);
		    	window.location = url;
		   });	  
		})
		
});

