<?php

$FlAG_DEBUG = false;

if($FlAG_DEBUG == true) {
	echo can_invest_lufax()."\n";
}
	
/*************************************************************************************************************************/

function can_invest_lufax() { //新站点这里要注意修改

	$buf = file_get_contents("https://list.lufax.com/list/piaoju?lufax_ref=https%3A%2F%2Flist.lufax.com%2Flist%2Fanyi");
	$buf = mb_convert_encoding($buf, "gbk", "utf-8");
	//echo $buf;

	while( ($buf = strstr($buf, '<li class="interest-rate">')) != false ) { //项目开头标记

		$item_buf = substr($buf, 0, strpos($buf, '/a>')); //项目结尾标记
		//echo $item_buf."\n";

		$qixian = 0;

		if( ($line_str = strstr($item_buf, 'invest-period')) != false) {
			//echo $line_str."\n";
			$s = substr($line_str, 0, strpos($line_str, '</p>'));
			//echo $s."\n";
			$s = substr($s, strpos($line_str, '<p>'));
			//echo $s."\n";
			preg_match("|<p>(.*)天|U", $s, $out);
			if(count($out) > 0) {
				$qixian = trim($out[1]);
				echo "qixian:".$qixian."; ";
			}
		}

		$can_invest = false;

		//echo $item_buf."\n";	
		if( ($line_str = strstr($item_buf, 'class="list-btn')) != false) {
			//echo $line_str."\n";
			preg_match("|>(.*)<|U", $line_str, $out);
			if(count($out) > 0) {
				//echo $out[1]."\n";
				if($out[1] == "投资") {
					$can_invest = true;
				}
				echo var_dump($can_invest);
			}
		}

		if($qixian != 0 && $qixian <= 60 && $can_invest == true) {
			return true;
		}

		$buf = strstr($buf, '</a>'); //项目结尾标记

	}

	return false;
}


?>
