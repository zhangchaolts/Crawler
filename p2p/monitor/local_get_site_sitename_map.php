<?php

$FlAG_DEBUG = false;
#$FlAG_DEBUG = true;

if($FlAG_DEBUG == true) {
	$site_sitename_map = get_site_sitename_map("local_info");
	print_r($site_sitename_map);
}


/********************************************************************************************************************************/

function get_site_sitename_map($url) {

	$site_sitename_map = array();

	$buf = file_get_contents($url);

	$text = str_replace("\n","", $buf);

	$parts1 = explode("$", $text);

	if(count($parts1) >= 4) {
		$parts2 = explode("#", $parts1[1]);
		foreach($parts2 as $index2 => $site_sitename) {
			$parts3 = explode(":", $site_sitename);
			if(count($parts3) == 2) {
				$site_sitename_map[$parts3[0]] = trim($parts3[1]);
			}
		}   
	}

	return $site_sitename_map;
}

?>
