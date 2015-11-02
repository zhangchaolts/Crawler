<?php

$FlAG_DEBUG = false;

if($FlAG_DEBUG == true) {
	$mail_list = get_mail_list("http://runningyangmao.blog.163.com/blog/static/25166910920157634424666", "ÒËÈË´û");
	print_r($mail_list);
}


/********************************************************************************************************************************/

function get_mail_list($url, $sitename) {

	$mail_list = array();

	//echo "start\n";

	$buf = file_get_contents($url);

	//echo $buf."\n";

	$buf = strstr($buf, '<div class="nbw-blog-start"></div>');

	$buf = substr($buf, 0, strpos($buf, '<div class="nbw-blog-end"></div>'));

	$text = ""; 

	while( ($buf = strstr($buf, '>')) != false ) { 
		$info = substr($buf, 1, strpos($buf, '<') - 1); 
		$text .= trim($info);
		$buf = strstr($buf, '<');
	}   
	//echo $text."\n";

	$parts1 = explode("%", $text);

	if(count($parts1) > 1) {
		foreach($parts1 as $index1 => $line) {
			$parts2 = explode("#", $line);
			if(count($parts2) >= 2) {
				if(strstr($parts2[0], "@") != false) {
					for($i = 1; $i < count($parts2); $i++) {
						if($parts2[$i] == $sitename) {
							$mail_list[] = $parts2[0]; 
						}   
					}
				}   
			}   
		}   
	}   

	return $mail_list;
}

?>
