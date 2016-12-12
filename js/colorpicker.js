$(document).ready(function() {
  $('select,input').on('change', function() {
    var rval = $( "#rinput" ).val();
    var gval = $( "#ginput" ).val();
    var bval = $( "#binput" ).val();
    
    var rgb = "rgb(" +rval.toString(16)+","+gval.toString(16)+","+bval.toString(16)+")";
    
    console.log(rgb)
    
    $('input').each(function(index, value) {
      $( "#output" ).css("background-color",rgb)
    });
  });
});
