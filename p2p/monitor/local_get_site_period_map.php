<?php

$FlAG_DEBUG = false;
#$FlAG_DEBUG = true;

if($FlAG_DEBUG == true) {
	$site_period_map = get_site_period_map("local_info");
	print_r($site_period_map);
}


/********************************************************************************************************************************/

function get_site_period_map($url) {

	$site_period_map = array();

	$buf = file_get_contents($url);

	$text = str_replace("\n","", $buf);

	$parts1 = explode("$", $text);

	if(count($parts1) >= 4) {
		$parts2 = explode("#", $parts1[2]);
		foreach($parts2 as $index2 => $site_period) {
			$parts3 = explode(":", $site_period);
			if(count($parts3) == 2) {
				$site_period_map[$parts3[0]] = $parts3[1];
			}
		}   
	}

	return $site_period_map;
}

?>
