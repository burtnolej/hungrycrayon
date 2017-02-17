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
		
		$expected_results = 'source_value=Clayton&foobar1=b&foobar2=c&foobar3=&ztypes=adult&cnstr_period=830-910,910-950&cnstr_dow=Friday&foobar4=a&foobar5=d';
		//assert.equal(0,0,'passed');
		assert.equal(getAllInputValues('ztypes',['qunit-filter-input']), $expected_results, 'passed');
	});
	

	QUnit.test('update URL based on callback events', function (assert) {
		
		$expected_results = 'source_value=Clayton&foobar1=b&foobar2=c&foobar3=&ztypes=adult&cnstr_period=830-910,910-950,950-1030&cnstr_dow=Friday&foobar4=a&foobar5=d';
		
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
 	
	
 	QUnit.test('send a URL and get response', function (assert) {
 		
	 	$expected_results = '<root><parser><value>drawentryform</value></parser><item id="1"><value /><valuetype>code</valuetype></item><item id="2"><value /><valuetype>name</valuetype></item></root>';
				
 			var options = {hidden:false};

			options.name = "message";options.class = "message";
			addElement("div","message",options);

			$url = 'http://localhost:8080/new/subject?source_value=subject'
			
			_makeRequest($url,writeHttpResponse,"message");

		 	var done = assert.async();
 			setTimeout(function() { 			
 				var el = document.getElementById("message");
				var result = el.textContent;
    			assert.equal(result, $expected_results, 'passed');
    			done();
  			},200);

	});
	
 	QUnit.test(' parse some XML', function (assert) {

			var expected_results = Array("foobar","barfoo");
			
  			var xmlDoc = (new DOMParser()).parseFromString("<root><child>foobar</child><child>barfoo</child></root>", "text/xml");
			var results = Array();

			elements= xmlDoc.getElementsByTagName("child");
			
  			assert.equal(elements[0].childNodes[0].nodeValue.toString(),"foobar", 'passed');
  			assert.equal(elements[1].childNodes[0].nodeValue.toString(),"barfoo", 'passed');
	});
		
 	QUnit.test('draw form widget using server provided xml', function (assert) {

			$xml = '<root><parser><value>drawentryform</value></parser><item id="1"><value /><valuetype>code</valuetype></item><item id="2"><value /><valuetype>name</valuetype></item></root>';
  			var xmlDoc = (new DOMParser()).parseFromString($xml, "text/xml");

			drawentryform(xmlDoc);
	
			assert.equal($('input[id="code"]').attr('name'),"code",'passed');
			assert.equal($('input[id="name"]').attr('name'),"name",'passed');
	});

	 		
 	QUnit.test('get ref data', function (assert) {
		
			$expected_results = '<root><row><cell><bgcolor>#ffffff</bgcolor><valuetype>col</valuetype><fgcolor>#000000</fgcolor><value>student</value></cell></row><row><cell><bgcolor>#ffffff</bgcolor><valuetype>row</valuetype><fgcolor>#000000</fgcolor><value>Peter</value></cell></row><row><cell><bgcolor>#ffffff</bgcolor><valuetype>row</valuetype><fgcolor>#000000</fgcolor><value>Coby</value></cell></row></root>';

 			var options = {hidden:false};

			options.name = "getrefdata";options.class = "message";
			addElement("div","getrefdata",options);
			
			url = "http://0.0.0.0:8080/list/lesson?&pagenum=1&pagelen=2&ztypes=student";
	
			_makeRequest(url,writeHttpResponse,"getrefdata");

		 	var done = assert.async();
 					setTimeout(function() { 			
 						var el = document.getElementById("getrefdata");
				 		assert.equal(el.textContent, $expected_results, 'passed');
				 		delElement("getrefdata");
				 		done();
  			},1000);
  			  			
	});
	
 	QUnit.test('get ref data select', function (assert) {
			drawxmldbselect("student","name")

  			var done = assert.async();
 			setTimeout(function() { 		
 				var options = Array();
				$("select#student option").each(function() {
					options.push($(this).val());
				});

				assert.equal(options.length,22, 0, 'passed');	

	  			$("select#student").remove(); // tearDown
				done();
  			},400);	
	});
	
 	QUnit.test('draw form widget using server provided xml  - 1 widget', function (assert) {

			$xml = '<root><parser><value>drawform</value></parser><item id="6"><value /><valuetype>subject</valuetype><options>a,b,c,d</options></item></root>';
		
			 var xmlDoc = (new DOMParser()).parseFromString($xml, "text/xml");

			drawform(xmlDoc);
			
			var options = Array();
			var expected_results = Array('a','b','c','d');
			
			$("select#subject option").each(function() {
				options.push($(this).val());
			});

			// tearDown
			$("select#subject").remove();
			
			assert.equal(compare_1darrays(options,expected_results), 0, 'passed');
	});
	
	
 	QUnit.test('draw form widget using server provided xml  - 2 widget', function (assert) {

			$xml = '<root><parser><value>drawform</value></parser><item id="6"><value /><valuetype>subject</valuetype><options>i,j,k,l</options></item><item id="7"><value /><valuetype>student</valuetype><options>e,f,g,h</options></item></root>';
		
			 var xmlDoc = (new DOMParser()).parseFromString($xml, "text/xml");

			drawform(xmlDoc);
			
			var options = Array();
			var expected_results = Array('i','j','k','l');
			
			$("select#subject option").each(function() {
				options.push($(this).val());
			});

			assert.equal(compare_1darrays(options,expected_results), 0, 'passed');
			
			var options = Array();
			var expected_results = Array('e','f','g','h');
			
			$("select#student option").each(function() {
				options.push($(this).val());
			});

			// tearDown
			$("select#subject").remove();
			$("select#student").remove();
			
			assert.equal(compare_1darrays(options,expected_results), 0, 'passed');
	});
	
 	QUnit.test('draw form widget using server provided xml  - real example', function (assert) {
	
			$xml = '<root><item><objtype>recordtype</objtype><value>subject</value><value>wp</value><value>ap</value></item><item><objtype>period</objtype><value>830-910</value><value>910-950</value></item><item><objtype>adult</objtype><value>Amelia</value><value>Stan</value></item><item><objtype>student</objtype><value>Clayton</value></item><item><objtype>dow</objtype><value>TU</value><value>WE</value></item><item><objtype>subject</objtype><value>Humanities</value><value>Math</value><value>Physics</value><value>English</value></item></root>';
			
			var parentel = addElement("div","divparent",{hidden:false,name:"foo"});
			
			drawform_multi($xml,parentel);
			
			var options = Array();
			var expected_results = Array('subject','wp','ap');
			
			$("select#recordtype option").each(function() {
				options.push($(this).val());
			});

			assert.equal(compare_1darrays(options,expected_results), 0, 'passed');
			
			var options = Array();
			var expected_results = Array('830-910','910-950');
			
			$("select#period option").each(function() {
				options.push($(this).val());
			});

			assert.equal(compare_1darrays(options,expected_results), 0, 'passed');
			
			var options = Array();
			var expected_results = Array('Amelia','Stan');
			
			$("select#adult option").each(function() {
				options.push($(this).val());
			});

			assert.equal(compare_1darrays(options,expected_results), 0, 'passed');
			
			var options = Array();
			var expected_results = Array('Clayton');
			
			$("select#student option").each(function() {
				options.push($(this).val());
			});

			assert.equal(compare_1darrays(options,expected_results), 0, 'passed');
			
			var options = Array();
			var expected_results = Array('TU','WE');
			
			$("select#dow option").each(function() {
				options.push($(this).val());
			});

			assert.equal(compare_1darrays(options,expected_results), 0, 'passed');
			
			var options = Array();
			var expected_results = Array('Humanities','Math','Physics','English');
			
			$("select#subject option").each(function() {
				options.push($(this).val());
			});

			$("div#divparent").remove(); // tearDown 
			
			assert.equal(compare_1darrays(options,expected_results), 0, 'passed');
	});
	
 	QUnit.test('draw form widget using server  - real example', function (assert) {

			var parentel = addElement("div","divparent",{hidden:false,name:"foo"});
			
  			url = "http://localhost:8080/refdata/all";
  			makeRequestResponse(url,drawform_multi,parentel);
  			
  			var options = Array();
  			var done = assert.async();
 			setTimeout(function() { 		
				$("select#subject option").each(function() {
					options.push($(this).val());
				});
	
				assert.ok(options.length > 0, 'passed');	

	  			$("div#divparent").remove(); // tearDown
				done();
  			},400);	
	});
	
 	QUnit.test('draw form widget using server  - real example get url from selections', function (assert) {

			expected_results = 'http://localhost:8080/add/lesson?recordtype=subject&period=830-910&adult=Aaron&student=Nathaniel&dow=Monday&subject=ELA&';
			
			var parentel = addElement("div","divparent",{hidden:false,name:"foo"});
			
  			url = "http://localhost:8080/refdata/all";
  			makeRequestResponse(url,drawform_multi,parentel);
  			
  			var options = Array();
  			var done = assert.async();
 			setTimeout(function() { 		
	
				url = "http://localhost:8080/add/lesson?"
				
				var selectsobj = $("div#divparent select");
				
				selectsobj.each(function() {
					url = url + this.name + "=" + this.value + "&";
				});
				
				assert.equal(url,expected_results, 'passed');	
				
	  			//$("div#divparent").remove(); // tearDown
				done();
  			},400);	
  			
  			var button = addElement("button","submit",{hidden:false,name:"submit",label:"submit",parentel:parentel});
	});
});