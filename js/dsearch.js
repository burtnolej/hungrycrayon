/*requirejs.config({
    baseUrl: 'js/lib',
    paths: {
       app: '../app'
    }
});*/

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
        'tabSlideOut': {
            deps: ['jquery'],
            exports: 'tabSlideOut'
        },
	}, waitSeconds: 15,
});

requirejs(['myutils','jquery','tabSlideOut'],    
    function(myutils,$,tabSlideOut){
    	
		$(document).ready(function(){
			
			// set context menu
			setcontextmenu("ul[class='nav']");
			
    	$(function(){
        $('.slide-out-div-top').tabSlideOut({
            tabHandle: '.handle1',                     //class of the element that will become your tab
            leftPos: '600px',                          //position from left/ use if tabLocation is bottom or top
        });
     	});     
     	
    	$(function(){
        $('.slide-out-div-top2').tabSlideOut({
            tabHandle: '.handle2',                     //class of the element that will become your tab
            leftPos: '400px',                          //position from left/ use if tabLocation is bottom or top
        });
     	});
     	
    	$(function(){
        $('.slide-out-div-top3').tabSlideOut({
            tabHandle: '.handle3',                     //class of the element that will become your tab
            leftPos: '200px',                          //position from left/ use if tabLocation is bottom or top
        });
     	});
     	
    	$(function(){
        $('.slide-out-div-top4').tabSlideOut({
            tabHandle: '.handle4',                     //class of the element that will become your tab
            leftPos: '1000px',                          //position from left/ use if tabLocation is bottom or top
        });
     	});

		   $("select, input").on('change',function(){
		    	url = buildurl();
		    	window.location = url;
		   });	  
		})		
});

