


<html>
<style>

#nav {
    padding:10px;
    line-height:30px;
    background-color:#eeeeee;
    height:2000px;
    float:left;
    text-align:left;
    width: 200px;
    border: 3px solid #73AD21;
    <!margin: auto;>   
}


#lvl1 {
    list-style:none;
    padding-left:0;
}
#lvl2 {
    list-style:none;
    padding-left:1em;
}
#lvl3 {
    list-style:none;
    padding-left:2em;
}
</style>
</html>

<?php

abstract class menu_item {
    const id = 0;
    const level = 1;
    const sub_id = 2;
    const parnt = 3;
    const source= 4;
    const tag=5;
    const label=6;
}

class menu_handler
{
	public function __construct($menu_array) {
		$this->menu_array = $menu_array;
		
		
   	foreach ($menu_array as $menu) {
			if ($parent == $menu[menu_item::id]) {
				echo '<li><a href="'.$menu[menu_item::source].
						'?name='.$menu[menu_item::tag].
						'?level='.$menu[menu_item::level].
						'">'.$menu[menu_item::label].'</a></li>';   
            }
        	}
        	
	}
	
	private function build_menu_tree(){
		
	}
   public function draw_menu($menu_array,$parent,$level){
   	// start nav panel
   	echo '<div id="nav">';   	
   	
   	// start list using parent style
   	echo '<ul id="lvl'.$level.'">';
   	
   	// draw parent list item and siblings

		$parent_level =
   	foreach ($menu_array as $menu) {
			if ($parent == $menu[menu_item::id]) {
				echo '<li><a href="'.$menu[menu_item::source].
						'?name='.$menu[menu_item::tag].
						'?level='.$menu[menu_item::level].
						'">'.$menu[menu_item::label].'</a></li>';   
            }
        	}
 
		// if item has children draw them
		
		
 			if ($parent == $menu[menu_item::parnt]) {
				echo '<li><a href="'.$menu[menu_item::source].
						'?name='.$menu[menu_item::tag].
						'?level='.$menu[menu_item::level].
						'">'.$menu[menu_item::label].'</a></li>';   
            }
        	}
        	
    	echo '</ul>';
    	echo '</div>';
	}
}

$menu_items = array(

	// 1 : menu style, to be appended to 'lvl' to match with style settings, indents etc
	// 2 : if menu is link to actual content will provides the filename; false means the link is
	//   : the parent of child links
	// 3 : html id tag or false if has children
	
   array(1,1,1,0,false,false,'PHP'),
   array(2,1,2,0,false,false,'Apache'),
   array(3,1,3,0;false,false,'HTML'),
   
   array(4,2,1,1,'build-install.php','phpdependencies','PHP Dependencies'),
   array(5,2,2,1,'build-install.php','configurephp','Configure PHP'),
   array(6,2,3,1,'build-install.php','troubleshootingphp','Troubleshooting PHP'),
   
   array(7,2,1,3,'html-html.php','httpdconf','httpdconf'),
   array(8,2,2,3,'html-html.php','htmllists','htmllists'),
   array(9,2,3,3,'html-html.php','htmltable','htmltable'),
   array(10,2,4,3,'html-html.php','htmllinks','htmllinks'),
   array(11,2,5,3,'html-html.php','htmlescaping','htmlescaping')  
);



$mnu = new menu_handler;


// level change can be calculated easilly as +/- 1 from current
#$mnu->draw_menu($menu_items,'0','1');
$mnu->draw_menu($menu_items,3,1);
?>

