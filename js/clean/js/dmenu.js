requirejs.config({
    baseUrl: 'js/lib',
    paths: {
       app: '../app'
    }
});

requirejs(['myutils','jquery'],

	function (myutils,$) {
		$(document).ready(function(){
			//setcontextmenu("div[id='wrap']","foobar");
			setcontextmenu("div[id='wrap']","macro_updateid");
			
	});
});