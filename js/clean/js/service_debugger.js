requirejs.config({
    baseUrl: 'js/lib',
    paths: {
       app: '../app'
    }
});

requirejs(['myutils','jquery'],
	function (myutils,$) {
		
		attrs = Array("ip","port","command","objtypes","fields","pprint","constraints","omitfields","fieldnames");
		default_values = Array("0.0.0.0","8080","command/dump","period","name,pobjid",1,"","",1);
		
		var options = { hidden:false };
		
		options.name = "time";
		addElement("p","time",options);
		
		options.name = "status";
		addElement("p","status",options);
		
		options.name = "params";options.class = "params";
		addElement("div","params",options);	
		
		options.name = "history";options.class = "history";
		addElement("div","history",options);
		
		options.name = "url";options.class = "url";
		addElement("div","url",options);
		
		options.name = "message";options.class = "message";
		addElement("div","message",options);
								
		for (i=0;i<attrs.length;i++) {
		
			var options = {hidden:false};
			options.name = attrs[i];
			options.label = attrs[i];
			options.parentid = "params";
			addElement("label","lbl"+i.toString(),options);
			
			options.subtype = "text";
			options.default = default_values[i];
			options.parentid = "params";
			addElement("input","inp1"+i.toString(),options);
			
			_addElement(Array("<br>"),false,document.getElementById("params"));
		}
		
		var options = {hidden:false};
		
		options.name = "url";
		options.parentid="url";
		addElement("p","url",options);
		
		options.name = "message";
		options.parentid = "message";
		addElement("p","message",options);
		
		$(document).ready(function(){
		
			//var myVar = setInterval(myTimer, 1000);
		
			$('input[name!="submit"]').keypress(function (e) {
				var key = e.which;
				if(key == 13)  // the enter key code
			  	{	 	
		   			makeRequest(geturl(),writeHttpResponse);
		   		}
		   		else {
		   			geturl();
		   		}
			});
		});
	}
);
