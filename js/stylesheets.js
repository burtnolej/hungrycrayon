
requirejs.config({
    baseUrl: 'js/lib',
    paths: {
       app: '../app'
    },
});

define(['jquery'], function($) {
	
//function   ($) {
	
	$('head').html('<link rel="stylesheet" type="text/css" href="css/select.css" /><link rel="stylesheet" type="text/css" href="css/div.css" /><link rel="stylesheet" type="text/css" href="css/switch.css" /><link rel="stylesheet" type="text/css" href="css/menu.css" />');
	}
);