

function _addElement(html_arr,hidden,parentelement,placement='bottom') {
	var div= document.createElement('div');

	if (hidden) { html_arr.splice(2,0," hidden ") }
	
	html_str =html_arr.join("");
	
	div.innerHTML= html_str;
	var el= div.firstChild;
	
	if (placement=="bottom") {
		parentelement.appendChild(el);   
	}
	else {
		parentelement.insertBefore(el,parentelement.firstChild);   
	}
	
	return el;
}

function addElement(element_type,id,options) {
	// for building paragraph, button etc
	var html_arr = Array();
	var hidden = options.hidden;
	delete options['hidden'];
	
	html_arr.push('<');html_arr.push(element_type);
	
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
	
	if (options.subtype != null) {
		html_arr.push(' type="');html_arr.push(options.subtype);html_arr.push('"');
	}
	
	if (options.default != null) {
		html_arr.push(' value="');html_arr.push(options.default);html_arr.push('"');
	}
	
	if (options.class != null) {
		html_arr.push(' class="');html_arr.push(options.class);html_arr.push('"');
	}
	
	if (options.name != null) {
		html_arr.push(' name="');html_arr.push(options.name);html_arr.push('"');
	}
	
	html_arr.push(' id="');html_arr.push(id);html_arr.push('"');
	html_arr.push('>');
	
	if (options.label != null) {html_arr.push(options.label);	}
	
	html_arr.push('</');html_arr.push(element_type);html_arr.push('>');
	
	if (options.parentid == null) {
		parentelement = document.body;
	}
	else {
		parentelement = document.getElementById(options.parentid);
	}
	
	_addElement(html_arr,hidden,parentelement,options.placement)
}