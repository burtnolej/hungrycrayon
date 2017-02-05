requirejs.config({
    baseUrl: 'js/lib',
    paths: {
       app: '../app'
    }
});

requirejs(['myutils','jquery'],    
    function(myutils,$){
		setElementStyle('contain','display','block',10);
		setElementStyle('containswitch','display','block',10);
		setElementStyle('wideswitch','display','block',10);
		setElementStyle('borderoff','display','block',10);
		
});

