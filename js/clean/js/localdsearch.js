
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
	} 
});

define(['myutils','tabSlideOut'], function(myutils,tabSlideOut) {
	
//requirejs(['myutils','jquery','tabSlideOut'],    
//    function(myutils,$,tabSlideOut){
    	
		$(document).ready(function(){
			
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
     	

		   $("select, input").on('change',function(){
		    	url = buildurl();
		    	window.location = url;
		   });	  
		})
		
		//widths = Array('220','220','220');
		//cpTableColWidths('table2','table1');
		//cpTableColWidths('table1','table2');
		//setTableColWidths(widths,'table2');
		//setTableColWidths(widths,'table1');
		
		//dumparray(getTableColWidths('table1'));
		

		
		
});

