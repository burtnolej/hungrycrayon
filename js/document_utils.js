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

function _addElement(html_arr,hidden) {
	var div= document.createElement('div');

	if (hidden) { html_arr.splice(2,0," hidden ") }
	
	html_str =html_arr.join("");
	div.innerHTML= html_str;
	var el= div.firstChild;
	document.body.appendChild(el);   
	return el;
}

function addElement(type,label,name,id,hidden=false) {
	// for building paragraph, button etc
	
	var html_arr = Array();
	html_arr.push('<');
	html_arr.push(type);
	html_arr.push(' name="');
	html_arr.push(name);
	html_arr.push('"');
	
	html_arr.push(' id="');
	html_arr.push(id);
	html_arr.push('"');
	
	html_arr.push('>');
	html_arr.push(label);	
	html_arr.push('</p>');
	
	_addElement(html_arr,hidden)
}

function delElement(id) {
	/* seems to be easier to write to the DOM via jscript functions rather than jquery */	
	el = document.getElementById(id);
	document.getElementById(id).parentElement.removeChild(el);
	
}

function getElementsIds(type) {
	var values = Array();
	$(type).each(function (index, id) {
   		values.push(this.id);
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

function getElementValues(type) {
	var values = Array();
	$(type).each(function (index, value) {
   		values.push(this.value);
	});
	return values;
}

function addSelectElement(name,id,options,hidden=false) {
	var html_arr = Array();
	html_arr.push('<');
	html_arr.push('select');
	
	html_arr.push(' name="');
	html_arr.push(name);
	html_arr.push('"');
	
	html_arr.push(' id="');
	html_arr.push(id);
	html_arr.push('"');
	
	html_arr.push('>');

	for (i = 0; i < options.length; i++) {
		html_arr.push('<option>');
		html_arr.push(options[i]);
		html_arr.push('</option>');
	}
	html_arr.push('</select>');

	el = _addElement(html_arr,hidden);
	return el;
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