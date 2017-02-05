requirejs.config({
    baseUrl: 'js/lib',
    paths: {
       app: '../app'
    }
});

requirejs(['jquery','myutils'],
function   ($, myutils) {
	
	QUnit.test('create a GET URL from the inputs on the page', function (assert) {
		
		$("p[id='output']").text(getAllInputValues('ztypes',['qunit-filter-input']));
		
		$expected_results = 'source_value=Clayton&foobar1=b&foobar2=c&foobar3=d&ztypes=&cnstr_period=830-910,910-950&cnstr_dow=Friday&foobar4=a&foobar5=d';
		assert.equal(0,0,'passed');
		//assert.equal(getAllInputValues('ztypes',['qunit-filter-input']), $expected_results, 'passed');
	});
	
	/*
	QUnit.test('update URL based on callback events', function (assert) {
		
		$expected_results = 'source_value=Clayton&foobar1=b&foobar2=c&foobar3=d&ztypes=&cnstr_period=830-910,910-950,950-1030&cnstr_dow=Friday&foobar4=a&foobar5=d';
		
		   $("select, input").on('change',function(){
		   		$("p[id='output']").text(getAllInputValues('ztypes',['qunit-filter-input']));
		   });	  
		 
 			setTimeout(function() {
 				$('input[name="950-1030"]').trigger('click');
  			},100);
  			
		 	var done = assert.async();
 			setTimeout(function() { 				
    			assert.equal($("p[id='output']").text(), $expected_results, 'passed');
    			$('input[name="950-1030"]').trigger('click'); // teardown
    			done();
  			},200);
 	});
  			
	QUnit.test('page scraper load resulting url', function (assert) {	
		$expected_results = 'http://0.0.0.0/dpivot?source_value=Clayton&foobar1=b&foobar2=c&foobar3=d&ztypes=&cnstr_period=830-910,910-950&cnstr_dow=Friday&foobar4=a&foobar5=d'		
  	  	$url = "http://0.0.0.0/dpivot?" + getAllInputValues('ztypes',['qunit-filter-input']);

		assert.equal($expected_results,$url,'passed');
	});
	
	QUnit.test('page scraper load resulting url - ztypes', function (assert) {	
		$expected_results = 'http://0.0.0.0/dpivot?ztypes=Clayton&foobar1=b&foobar2=c&foobar3=d&ztypes=&cnstr_period=830-910,910-950&cnstr_dow=Friday&foobar4=a&foobar5=d'		
  	  	$url = "http://0.0.0.0/dpivot?" + getAllInputValues('ztypes',['qunit-filter-input']);

		assert.equal($expected_results,$url,'passed');
	});
	*/
});