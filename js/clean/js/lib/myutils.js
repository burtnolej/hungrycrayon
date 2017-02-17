

/*
isarray(obj)
compare_1darrays(arr1, arr2) 
pp(obj)
 _addElement(html_arr,hidden,parentelement,placement='bottom')
  addElement(element_type,id,options)
myTimer()
getElementValues(type)
getElementsName(type)
getElementsIds(type)
getElementValueChanges(elementtype,initvalues)
delElement(id)
makeRequest(url,alert_contents) 
writeHttpResponse()
writeHttpServiceStatus()
geturl() 
buildurl()
importlib()
 */

function isarray(obj) {
  /* returns true if the passed object is an array */
  if (Object.prototype.toString.call(obj) === '[object Array]') {
    return true;
  }
  return false;
}
function compare_1darrays(arr1, arr2) {
  /* both arguments must be 1d arrays; returns 0 if identical or 
		returns an array with the indexes of the elements that are different
		in it */
  if (!isarray(arr1) || !isarray(arr2)) {
    throw ('both arguments need to be of type array')
  } 
  else if (arr1.length != arr2.length) {
    throw ('arrays are different lengths')
  } 
  else {
    var diffs = Array();
    for (i = 0; i < arr1.length; i++) {
      if (arr1[i] != arr2[i]) {
        diffs.push(i);
      }
    }
    if (diffs.length != 0) {
      return diffs
    }
  }
  return 0
}

function pp(obj) {
  /* return a string represenation of an object*/
  return JSON.stringify(obj);
}

function _addElement(html_arr,hidden,parentelement,placement='bottom') {
	var div= document.createElement('div');

	if (hidden) { html_arr.splice(2,0," hidden ") }
	
	html_str =html_arr.join("");
	
	div.innerHTML= html_str;
	var el= div.firstChild;
	
	if (placement=="bottom") {
		if (parentelement instanceof jQuery){
			parentelement.append(el);   
		}
		else {
			parentelement.appendChild(el);   
		}
	}
	else {
		parentelement.insertBefore(el,parentelement.firstChild);   
	}
	
	return el;
}

function addElement(element_type,id,options) {

	/*var options = {
		//label:null;
		//name:null;
		hidden:false
		//subtype=null;
		//default=null;
		//classs=null;
		//parentid=null;
		//parentel=null;
		//onclick=null;
	};*/
		
	var html_arr = Array();
	var hidden = options.hidden;
	delete options['hidden'];
	
	html_arr.push('<');
	html_arr.push(element_type);
	
	/*for (var property in options) {
		if (options.hasOwnProperty(property)) {
			if (options[property] != null) {
				html_arr.push(' '+property+'="');html_arr.push(options[property]);html_arr.push('"');
			}
	    }
	}*/

	if (options.href != null) {
		html_arr.push(' href="');html_arr.push(options.href);html_arr.push('"');
	}
	
	if (options.onclick != null) {
		html_arr.push(' onclick="');html_arr.push(options.onclick);html_arr.push('"');
	}
	
	if (options.subtype != null) {
		html_arr.push(' type="');html_arr.push(options.subtype);html_arr.push('"');
	}
	
	if (options.class != null) {
		html_arr.push(' class="');html_arr.push(options.class);html_arr.push('"');
	}
	
	if (options.name != null) {
		html_arr.push(' name="');html_arr.push(options.name);html_arr.push('"');
	}
	
	html_arr.push(' id="');
	html_arr.push(id);
	html_arr.push('"');

	if (options.default != null) {
		if (element_type != "select") {
			html_arr.push(' value="');html_arr.push(options.default);html_arr.push('"');
		}
	}
	
	html_arr.push('>');
	
	if (options.label != null) {
		html_arr.push(options.label);	
	}
	
	if (options.options != null) {
		for (i = 0; i < options.options.length; i++) {
			//html_arr.push('<option>');
			html_arr.push('<option');
			
			if (options.default != null) {
				if (options.default == options.options[i]) {
					html_arr.push(" selected ");
				}
			}	
			html_arr.push('>');
			
			html_arr.push(options.options[i]);
			html_arr.push('</option>');
		}
	}
	
	html_arr.push('</');
	html_arr.push(element_type);
	html_arr.push('>');
	
	if (options.parentel != null) {
		var parentelement = options.parentel;
	}
	else {
		if (options.parentid == null) {
			var parentelement = document.body;
		}
		else {
			var parentelement = document.getElementById(options.parentid);
		}
	}

	return _addElement(html_arr,hidden,parentelement,options.placement);
}

function drawxmldbselect(objtype,colname) {
 			var options = {hidden:false};

			options.name = objtype;options.class = "message";
			addElement("div","message",options);

			url = "http://0.0.0.0:8080/list/"+objtype+"?&pagenum=1&pagelen=20&ztypes=" + colname;
	
			_makeRequest(url,writeHttpResponse,"message");

 			function x (callback) {
 					setTimeout(function() { 			
 						var el = document.getElementById("message");
 						var xmlDoc = (new DOMParser()).parseFromString(el.textContent, "text/xml");
				 		callback(xmlDoc,objtype);
				 		delElement("message");
  			},200)};
  			
  			x(drawxmlselect);
}
  			
function drawxmlselect($xml,elname) 
{	
	elements= $xml.getElementsByTagName("value");
	
	optionsarr = Array("NotSelected","all");
	for (i=0;i<elements.length;i++) {
		optionsarr.push(elements[i].childNodes[0].nodeValue.toString());
	}
	
	var options = {hidden:false,name:elname,options:optionsarr};				 
	addElement("select",elname,options);
}
			
function drawcselectp(elname,options)
// options, values (array), parentel (element) comment (str)
// and class which is appended to the select class list
// this is used to identify this select as being part of some broader group
{	
	// create a label
	var _options = {hidden:false,
									class:"label",
									label:elname,
									parentel:options.parentel};			
	label = addElement("p","",_options)
	
	// create a span
	var _options = {hidden:false,
									class:"select",
									parentel:options.parentel};			
	spanel = addElement("span",elname+"span",_options)
	
	// create the select
	
	$selectclass = "custom";
	if (options.class != null) {
		$selectclass = $selectclass + " " + options.class;
	}

	var _options = {hidden:false,
									name:elname,
									options:options.values,
									parentel:spanel,
									//class:"custom"};				 
									class:$selectclass};		
							
	if (options.default != null) {
		_options.default = options.default;
	}
	
	addElement("select",elname,_options);
	
	if (options.comment != null) {
		// create a span
		var _options = {hidden:false,class:"comment"};			
		spancomel = addElement("span","com"+elname,_options)
		
		// create a p
		var _options = {hidden:false,class:"select",parentel:spancomel,label:options.comment};			
		spanel = addElement("p","",_options)
	}
}

function drawcselect(values,elname,comment=null) 
{	
	// create a label
	var options = {hidden:false,class:"label",label:elname};			
	label = addElement("p","",options)
	
	// create a span
	var options = {hidden:false,class:"select"};			
	spanel = addElement("span",elname+"span",options)
	
	// create the select
	var options = {hidden:false,name:elname,options:values,parentid:elname+"span",class:"custom"};				 
	addElement("select",elname,options);
	
	if (comment != null) {
		// create a span
		var options = {hidden:false,class:"comment"};			
		spancom = addElement("span","com"+elname,options)
		
		// create a p
		var options = {hidden:false,class:"select",parentid:"com"+elname,label:comment};			
		spanel = addElement("p","",options)
	}
}

function drawform_multi($xml,$parentel=null) {
	
		// $xml is a string containing xml
		// $parentel is the parent object that the form needs to become a child of
		// $parentel can be a jscript or a jquery object
		
		/* takes this format 	as $xml; multiple obj types in 1 record
		<root>
			<item>
				<objtype>recordtype</objtype>
				<value>subject</value>
				<value>wp</value>
				<value>ap</value>
			</item>
			<item>
				<objtype>subject</objtype>
		</root>'*/

		var xmlDoc = (new DOMParser()).parseFromString($xml, "text/xml");
		
		
		// look for default values in the xml tree
		var defaults = {};
		var itemelements= xmlDoc.getElementsByTagName("item");
		
		for (var i=0;i<itemelements.length;i++) {
			vt= itemelements[i].getElementsByTagName("valuetype")[0].childNodes[0].nodeValue.toString();
			val = itemelements[i].getElementsByTagName("value")[0].childNodes[0].nodeValue.toString();
			defaults[vt] = val;
		}
		
		//var itemelements= xmlDoc.getElementsByTagName("item");
		var itemelements= xmlDoc.getElementsByTagName("refitem");
		
		for (var i=0;i<itemelements.length;i++) {
			vt= itemelements[i].getElementsByTagName("objtype")[0].childNodes[0].nodeValue.toString();
			values = Array();
			var valelements = itemelements[i].getElementsByTagName("value");		
			for (var j=0;j<valelements.length;j++) {	
				values.push(valelements[j].childNodes[0].nodeValue.toString());
			}
			
			var options = {hidden:false,name:vt,values:values,class:"new"};		
			//var options = {hidden:false,name:vt,values:values};		
			
			if ($parentel != null) {
				options.parentel = $parentel;
			}
						
			if (vt in defaults) {
				options.default = defaults[vt];
			}
			
			drawcselectp(vt,options);
			
			addElement("br","",{parentel:$parentel});
		}
}

function drawform($xml,$parentid=null) {
	// form just consists of db select boxes
	// db data retrieved from rest service
	// makes one call per objtype
	/* $xml of the format
		<root>
			<parser><value>drawform</value></parser>
			<item id="6">
				<valuetype>subject</valuetype>
				<options>i,j,k,l</options>
			</item>
		</root> */		
	   
		var elements= $xml.getElementsByTagName("valuetype");
		var values= $xml.getElementsByTagName("options");
		
		for (var i=0;i<elements.length;i++) {
			vt = elements[i].childNodes[0].nodeValue.toString();
			val = values[i].childNodes[0].nodeValue.toString();
			
			var options = {hidden:false,name:vt,options:val.split(',')};		 
			addElement("select",vt,options);
		}
}

function drawentryform($xml,$parentel=null) {
		// form just consists of list boxes
		
		var xmlDoc = (new DOMParser()).parseFromString($xml, "text/xml");
		
		elements= xmlDoc.getElementsByTagName("valuetype");
		
		for (i=0;i<elements.length;i++) {
			console.log(elements[i].childNodes[0].nodeValue.toString());
		}

		elements= xmlDoc.getElementsByTagName("item");
		
		var options = {hidden:false,class:"contain",label:"input something",parentel:$parentel};
		divparentel = addElement("div","inputdiv",options);
			
		for (i=0;i<elements.length;i++) {
			el = elements[i];
			vt= el.getElementsByTagName("valuetype");
			
			var field = vt[0].childNodes[0].nodeValue.toString();

			var options = {hidden:false,label:field,parentel:divparentel};
			addElement("label",field,options);
			var options = {hidden:false,name:field,parentel:divparentel};
			addElement("input",field,options)
		}
}

function myTimer() {
    var d = new Date();
    document.getElementById("time").innerHTML = d.toLocaleTimeString();
    makeRequest("http://0.0.0.0:8080/command/ping",writeHttpServiceStatus);
}

function getElementValues(type) {
	var values = Array();
	$(type).each(function (index, value) {
   		values.push(this.value);
	});
	return values;
}

function getElementsName(type) {
	var values = Array();
	$(type).each(function (index, name) {
   		values.push(this.name);
	});
	return values;
}

function getElementsIds(type) {
	var values = Array();
	$(type).each(function (index, id) {
   		values.push(this.id);
	});
	return values;
}

function getElementValueChanges(elementtype,initvalues) {
	newvalues = getElementValues(elementtype);
	diffvalues = compare_1darrays(initvalues,newvalues);
	ids = getElementsIds(elementtype);
	result = Array();

	for (i=0;i<diffvalues.length;i++) {
		result.push(ids[diffvalues[i]]);
		result.push(newvalues[diffvalues[i]]);
	}
	
	return result;
}

function delElement(id) {
	/* seems to be easier to write to the DOM via jscript functions rather than jquery */	
	el = document.getElementById(id);
	document.getElementById(id).parentElement.removeChild(el);
}

function makeRequestResponse(url,callback=null,arg=null) {
	// arg is a pass through to the callback
	//var options = {hidden:false};
	var options = {};
	
	options.name = "getrefdata";options.class = "message";options.hidden = "foobar";
	addElement("div","getrefdata",options);
			
	_makeRequest(url,writeHttpResponse,"getrefdata");

 	function x (_callback=null) {
 		setTimeout(function() { 			
 		$responseText = document.getElementById("getrefdata").textContent;
 		if (_callback != null) {
 			_callback($responseText,arg);
 		}
 		delElement("getrefdata");
  	},200)};

  	x(callback);
}

function _makeRequest(url,alert_contents,args=null) {
    httpRequest = new XMLHttpRequest();

    if (!httpRequest) {
      alert('Giving up :( Cannot create an XMLHTTP instance');
      return false;
    }
    httpRequest.onreadystatechange = alert_contents;
    httpRequest.open('GET', url,true);
    httpRequest.send();
    httpRequest['args'] = args;
}
    	
	
function makeRequest(url,alert_contents) {
    httpRequest = new XMLHttpRequest();

    if (!httpRequest) {
      alert('Giving up :( Cannot create an XMLHTTP instance');
      return false;
    }
    httpRequest.onreadystatechange = alert_contents;
    httpRequest.open('GET', url,true);
    httpRequest.send();
    
	element = document.getElementById("history")

    var linkid = new Date().getTime();

	var options = {
		hidden:false,
		href: url
	};
	
	options.name = "foobar";
	options.label = linkid;
	options.parentid = "history";
	options.placement = "top";

	_addElement(Array("<br>"),false,document.getElementById("history"),'top');
	addElement("a",linkid,options);
	
	
	$('a[id="'+linkid+'"]').on('click',function (id) {
   		console.log(this.href);
   		return false;
	});
}

function writeHttpResponseText(outputelement) {
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		if (httpRequest.status === 200) {
			return this.responseText;
      } else {
      		alert(httpRequest.status);
      }
	}	
}

function writeHttpResponse(element_id) {
	// httpRequest['args'] is just a convenient way to pass data around the callbacks
	// in this case it represents the a tag that links the element being created to the content it use (objtype probably))
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		if (httpRequest.status === 200) {
			var xmlTextNode = document.createTextNode(this.responseText);
			document.getElementById(httpRequest['args']).appendChild(xmlTextNode)		
      } else {
      		alert(httpRequest.status);
      }
	}	
}

function writeHttpServiceStatus() {
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		element = document.getElementById("status")
		if (httpRequest.status === 200) {
			element.innerHTML = this.responseText;
			if (this.responseText == "ping") {
				$("p[id='timer']").css("background-color", "#F00");
				element.style.backgroundColor = "green";
			}
      } else {
      		element.style.backgroundColor = "red";
      }
	}	
}
 
function geturl()  {
	names =getElementsName("input");
	values = getElementValues("input");
	url = "http://";
		
	url = "http://" + $('input[name="ip"]').attr('value');
	url = url + ":" + $('input[name="port"]').attr('value');
	url = url + "/" + $('input[name="command"]').attr('value') + "?";

	for (i=3;i<names.length;i++) {
		if ( values[i] != "") {
			url = url + names[i] + "=" + values[i] + "&";
		}
	}
	document.getElementById("url").innerHTML = url;
	return url;
}

function buildurl(fields=null,values=null) {
	// fields/values are assoc arrays of other name/values we want to put onto
	// the get url to pass back to the webpage (ie last_source_value)
 	url = "http://".concat(Globals.server_name,"/",Globals.script_name,"?");
   	
   	ztypes = new Array();
   		
   	$('select').each(function (index, value) {
	   		url = url + this.id + "=" + this.value + "&";
	   });
	    		
	  $('input').each(function (index, value) {    			
	  		if (this.checked == true) {
	  			ztypes.push(this.id);	
	  		}
	  		else {
	  			url = url + this.id + "=" + this.value + "&";
	  		}
	   });
    		
    	url = url + "ztypes=" + ztypes.join() + "&";
    	
    	if (fields != null) {
    		for (i=0;i<fields.length;i++) {
    			url = url + fields[i] + "=" + values[i] + "&";
    		}
    	}
  return url
}

function getMultiSelectValues() {
	/* scrape the DOM for any switchcontain divs; return name=value1,value2,name=value1,value2 */

		els = document.getElementsByClassName('switchtable'); //
		
		var output = Array();
		
		for (i=0;i<els.length;i++) {
		  var values = Array();
		  inputs = els[i].getElementsByTagName('input');
		  
		  for (j=0;j<inputs.length;j++) {
		    if (inputs[j].checked) {
		      values.push(inputs[j].name);
		    }
		  }
		  output.push(els[i].getAttribute('name') + "=" + values.join());
		}
		
	return(output.join("&"));	
}

function getSelectValues() {
	/* scrape the DOM for any singleswitch spans; return value1,value2 etc for names of checked boxes*/

	output = Array();
   	$('select').each(function (index, value) {
	   		output.push(this.id + "=" + this.value)
	   });

	return(output.join("&"));	
}

function getSwitchValues() {
	/* scrape the DOM for any singleswitch spans; return value1,value2 etc for names of checked boxes*/

		els = document.getElementsByName('singleswitch');
		
		var output = Array();
		
		for (i=0;i<els.length;i++) {
		  inputs = els[i].getElementsByTagName('input');
		  
		    if (inputs[0].checked) {
		      output.push(inputs[0].name);
		    }
		}
		
	return(output.join(","));	
}

function getInputValues($ignore=[]) {
	/* scrape the DOM for any singleswitch spans; return value1,value2 etc for names of checked boxes*/

	output = Array();

	$("input[type='text']").each(function (index, value) {

			if ($.inArray(this.id, $ignore)  == -1) {
	   			output.push(this.id + "=" + this.value);
	   		}
	   });

	return(output.join("&"));	
}

function getAllInputValues($switchvarname,$ignore=[]) {
	
	$str=getInputValues($ignore);
	$str = $str + "&" + $switchvarname +"=" + getSwitchValues();
	$str = $str + "&" + getMultiSelectValues();
	$str = $str + "&" + getSelectValues();	
	
	return($str);
}
	
function importlib(src) {
	var imported = document.createElement("script");
	imported.src = src;
	document.head.appendChild(imported);	
}

function getTableColWidths(tableid) {
	
	/* return a 1d array containing the column widths in pixels of the table with id = tableif */
	var tablecolwidths = Array();
	
	var table = document.getElementById(tableid);
	var tablerows = table.getElementsByTagName('tr');
	var tablecols = tablerows[0].getElementsByTagName('td');
	
	for (i = 0; i < tablecols.length; i++) {
		tablecolwidths.push(tablecols[i].offsetWidth);
	}
	return tablecolwidths;
}

function setTableColWidths(widths,tableid) {
	/* take a 1d array of of integers and apply to table tableid 
	note that setting the width of top row will affect all subsequent rows*/
	
	var table = document.getElementById(tableid);
	var tablerows = table.getElementsByTagName('tr');
	var tablecols = tablerows[0].getElementsByTagName('td');
	
	for (i = 0; i < widths.length; i++) {
		newwidth = widths[i];
		tablecols[i].style.width = newwidth.toString()  + "px";
	}
}

function cpTableColWidths(fromtableid,totableid) {
	/* get the col widths from 1 table and apply to a 2nd table 
	tables need to have the same number of columns */
	
	console.log(arguments.callee.name);

	widths = getTableColWidths(fromtableid);
	setTableColWidths(widths,totableid);
} 

function alertme(message,arg=null) {
	var p= document.createElement('p');
	
	var userobjid = message.split(",")[0].split("=")[1];
	p.id = userobjid;
	
	var textNode = document.createTextNode(message);
	p.appendChild(textNode);	
	document.body.appendChild(p);
}

function dumparray(arr) {
		for (i = 0; i < arr.length; i++) {
			//console.log(i.tostring() + ":" + arr[i].tostring());
		}
}

function setElementStyle(classname,attr,attrval,timeoutlen) {
	setTimeout(function() {
		els = document.getElementsByClassName(classname);
		for (i = 0; i < els.length; i++) {
			els[i].setAttribute("style", attr + ": " + attrval + ";");
		}
  	},timeoutlen);
 }

function _updateid(id) {
	
	var url = "http://localhost:8080/id/" + id + "?";
	  	
	var parentel=$(this).closest("div");
	
	if ($('#tmpdiv').length) {
		$('#tmpdiv').remove();
	}
		
	var tmpdiv = addElement("div","tmpdiv",{hidden:false,parentel:parentel});
	
	makeRequestResponse(url,drawform_multi,tmpdiv);
	
	 setTimeout(function() { 	
	 	init_values = getElementValues("select");		
	  },200);
}

function macro_updateid (targetobjid,menuitemid) {	
	var $idel  = $("[id='"+targetobjid.id+"']").find("p");
	$("[id='source_value']").val($idel.attr('id'));
	
	document.getElementsByClassName('handle1')[0].click();
	
	var e = $.Event('keypress');
	e.which = 13;
	
	$("[id='source_value']").trigger(e);
}
					
function foobar(msg) {
	alert(msg.id);
}

function setcontextmenu(selectorstr,callback=null) {
			$("html").on("contextmenu", function(e ) {
				
				if ($("#contextmenup").length) {
						$("#contextmenup").remove();
				}
				
				var contextmenup = addElement("p","contextmenup",{hidden:true});
				
				var targetobj = $(e.target);
							
				contextmenup.innerHTML = targetobj[0].tagName  + "," + targetobj[0].id + ","  + targetobj[0].textContent 
				
				currentCSSDisplay = $(selectorstr).css("display");
			
				if (currentCSSDisplay == "block") {
					$(selectorstr).css("display","none");
				}
				else {
					$(selectorstr).css("top",e.pageY.toString());
					$(selectorstr).css("left",e.pageX.toString());
					$(selectorstr).css("display","block");
				}
				
				if (currentCSSDisplay == "none") {
					$parentel = $(selectorstr).find("ul")[0];

					$menuparent = addElement("li","foomenu",{parentel:$parentel});
					
					options = {parentel:$menuparent,label:targetobj[0].tagName}
					if (callback != null) {
						options['onclick'] = callback + "("+targetobj[0].id+")";
						options['href'] = "javascript:void(0);";
					}
					
					addElement("a","foobar",options);
				}

				e.preventDefault();
			});
}