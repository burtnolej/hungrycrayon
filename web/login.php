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
    width:420px;
    margin:0px auto;
    border:none;
    margin-top:10px;
    margin-bottom:0px;
}

#input {
    display:inline-block;
    vertical-align:middle;
    margin-bottom:10px;
    margin-top:10px;;
    <!margin-left:260px>;
    <!fpadding:10px;>
    <!line-height:30px;>
    <!background-color:#eeeeee;>
    <!height:228px;>
    float:right;
    text-align:middle;
    width: 120px
    <!border: 3px solid #73AD21;>
    <!margin: auto;>   
    font-family: Arial, Helvetica, sans-serif;
    font-size: 2em;
}

#label {
    border:none;
    vertical-align:middle;
    display:inline-block;
    margin-left:10px;
    margin-bottom:10px;
    margin-top:10px;
    float: left;
    text-align: left;
    width: 180px;
    font-family:Arial, Helvetic, sans-serif;
    font-size: 2em;
</style>

<body>
<div id=pic>
<center>
<img src="hungrycrayon.png" alt="hUnGrYcRaYoN" style=""width:628px;height:456px;">
</center>
</div>

</body>

<br><br>
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
<center>
<input id=input type='submit' name='submit' value='enter site' />
</center>
</div>
</div>
 
</fieldset>
</form>
</html>
<?php
}

draw_login();
?>
