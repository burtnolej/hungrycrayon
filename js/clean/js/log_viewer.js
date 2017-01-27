
requirejs.config({
    baseUrl: 'js/lib',
    paths: {
       app: '../app'
    }
});

requirejs(['jquery'],
function  ($) {
	
	function jsonCallback(json){
	  console.log(json);
	}
	
	$.ajax({
	  url: "http://localhost/tmp.json",
	  dataType: "jsonp"
	});
});
