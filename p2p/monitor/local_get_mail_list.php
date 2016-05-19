<?php

$FlAG_DEBUG = false;
#$FlAG_DEBUG = true;

if($FlAG_DEBUG == true) {
	$mail_list = get_mail_list("local_info", "有融网发标预告");
	print_r($mail_list);
}


/********************************************************************************************************************************/

function get_mail_list($url, $sitename) {

	$mail_list = array();

	$buf = file_get_contents($url);

	$text = str_replace("\n","", $buf);

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
