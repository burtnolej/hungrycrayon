<?php


function draw_login() {

?>
<html>

<style>

#pic {
    display=inline-block;
    margin:0px auto;
}

#login {
    width:192px;
    margin:0px auto;
    border:none;
    margin-top:10px;
    margin-bottom:10px;
}

#input {
    display:inline-block;
    vertical-align:middle;
    margin-left:20px
    <!fpadding:10px;>
    <!line-height:30px;>
    <!background-color:#eeeeee;>
    <!height:228px;>
    float:left;
    text-align:middle;
    width: 20px
    <!border: 3px solid #73AD21;>
    <!margin: auto;>   
    font-family: Arial, Helvetica, sans-serif;
    font-size: 1em;
}

#label {
    border:none;
    vertical-align:middle;
    display:inline-block;
    float: left;
    text-align: left;
    width: 80px;
    font-family:Arial, Helvetic, sans-serif;
    font-size: 1em;
</style>

<body>
<div id=pic>
<center>
<img src="hungrycrayon.png" alt="hUnGrYcRaYoN" style="width:314px;height:228px;">
</center>
</div>

</body>

<form style="border:none" id=login action='validate-login.php?dummyfunc' method='post' accept-charset='UTF-8'>

<fieldset >

<input type='hidden' name='submitted' id='submitted' value='1'/>

<div id=login>
<div >
<label id=label for='username' >username</label>
<input id=input type='text' name='username' id='username'  size="5" />
</div>
 
<div>
<label id=label for='password' >password</label>
<input id=input type='password' name='password' id='password' size="5" />
</div>
 
<div>
<input id=label type='submit' name='submit' value='submit' />
</div>
</div>
 
</fieldset>
</form>
</html>
<?php
}

draw_login();
?>
