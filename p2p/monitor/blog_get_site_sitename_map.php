<?php

$FlAG_DEBUG = false;

if($FlAG_DEBUG == true) {
	$site_sitename_map = get_site_sitename_map("http://runningyangmao.blog.163.com/blog/static/25166910920157634424666");
	print_r($site_sitename_map);
}


/********************************************************************************************************************************/

function get_site_sitename_map($url) {

	$site_sitename_map = array();

	$buf = file_get_contents($url);

	$buf = strstr($buf, '<div class="nbw-blog-start"></div>');

	$buf = substr($buf, 0, strpos($buf, '<div class="nbw-blog-end"></div>'));

	$text = ""; 

	while( ($buf = strstr($buf, '>')) != false ) { 
		$info = substr($buf, 1, strpos($buf, '<') - 1); 
		$text .= trim($info);
		$buf = strstr($buf, '<');
	}   
	//echo $text."\n";

	$parts1 = explode("$", $text);

	if(count($parts1) >= 4) {
		$parts2 = explode("#", $parts1[1]);
		foreach($parts2 as $index2 => $site_sitename) {
			$parts3 = explode(":", $site_sitename);
			if(count($parts3) == 2) {
				$site_sitename_map[$parts3[0]] = $parts3[1];
			}
		}   
	}

	return $site_sitename_map;
}

?>
