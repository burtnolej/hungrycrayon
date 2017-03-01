requirejs.config({
    baseUrl: 'js/lib',
    paths: {
       app: '../app'
    }
});

requirejs(['jquery','myutils'],
function   ($, myutils) {
	
 	QUnit.test('drawform widget using server', function (assert) {

			var parentel = addElement("div","divparent",{hidden:false,name:"foo"});
			
  			url = "http://0.0.0.0:8080/form/dpivot";
  			makeRequestResponse(url,drawform,parentel);
  			
  			var options = Array();
  			var done = assert.async();
 			setTimeout(function() { 		
				$("select#xaxis option").each(function() {
					options.push($(this).val());
				});
	
				assert.ok(options.length==5, 'passed');	
				options = Array();
				
				$("select#yaxis option").each(function() {
					options.push($(this).val());
				});
	
				assert.ok(options.length==5, 'passed');	
				options = Array();
				
				$("select#source_type option").each(function() {
					options.push($(this).val());
				});
	
				assert.ok(options.length==3, 'passed');	

	  			//$("div#divparent").remove(); // tearDown
				done();
  			},400);	

	});
});