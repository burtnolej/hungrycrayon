requirejs.config({
    baseUrl: 'js/lib',
    paths: {
       app: '../app'
    }
});


// Start the main app logic.
/*requirejs(['app/add_element'],
function   (add_element) {
		var options = {hidden:false,
									 name:"time",
									 label:"foobar"};
		add_element("p","time",options);
});*/


requirejs(['myutils'],
	function (myutils) {
		foobar();
		foobar2();
		
	}
);