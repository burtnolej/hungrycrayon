<html>
    <body>
        <form method="get" action="<?php echo $_SERVER['PHP_SELF']?>" >

            <input type="submit" name="on" value="on">
            <input type="submit" name="off" value="off">

        </form>
    </body>
</html>
<?php
	
    if(isset($_GET['on'])) {
        onFunc();
    }
    if(isset($_GET['off'])) {
        offFunc();
    }

    function onFunc(){
        echo "Button on Clicked";
        echo $_SERVER['PHP_SELF'];
    }
    function offFunc(){
        echo "Button off clicked";
    }
?>