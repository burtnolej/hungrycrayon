		// make sure full frame output line
		if (strpos($frame,':') !== false) {
			
				// split frame by colon into 3 vars
				list($fullpath, $rest) = explode(":",substr($frame,3));
				
				// find the start of the args in the non path section
				$open_bracket_posn = strpos($rest,'(');
					
				// put args into an array
				$args = explode(" ",substr($rest,$open_bracket_posn+1,-1));
				
				// output stuff
				echo basename($fullpath).PHP_EOL;
				print_r($args);
		}
	}
	