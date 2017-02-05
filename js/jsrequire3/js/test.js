requirejs.config({
    baseUrl: 'js/lib',
    paths: {
       app: '../app'
    }
});

// Start the main app logic.
requirejs(['app/alertmeshirtcolor'],
function   (alertmeshirtcolor) {
	
	QUnit.test('dummy', function (assert) {
		assert.ok(alertmeshirtcolor());
	});
	
});