<?php

$FlAG_DEBUG = false;

if($FlAG_DEBUG == true) {
	echo can_invest_solarbao()."\n";
}
	
/*************************************************************************************************************************/

function can_invest_solarbao() { //新站点这里要注意修改

	$buf = file_get_contents("http://www.solarbao.com/licai/meicheng/page1");
	$buf = mb_convert_encoding($buf, "gbk", "utf-8");
	//echo $buf;

	while( ($buf = strstr($buf, 'licai-product-style')) != false ) { //项目开头标记

		$item_buf = substr($buf, 0, strpos($buf, '/ul>')); //项目结尾标记
		//echo $item_buf."\n";

		$qixian = 0;

		if(strstr($item_buf, '<span>天') != false) {
			$line_str = substr($item_buf, 0, strpos($item_buf, '<span>天'));
			//echo $line_str."\n";
			$parts1 = explode('<p class="licai-number key-highlight">', $line_str);
			if(count($parts1) >= 2) {
				$qixian = $parts1[count($parts1) - 1];
				echo "qixian:".$qixian."; ";
			}
		}

		$can_invest = false;

		//echo $item_buf."\n";	
		if( ($line_str = strstr($item_buf, '<span class="licai-product-right">')) != false) {
			//echo $line_str."\n";
			preg_match("|可投：(.*)块|U", $line_str, $out);
			if(count($out) > 0) {
				//echo $out[1]."\n";
				if($out[1] > 0) {
					$can_invest = true;
				}
				echo var_dump($can_invest);
			}
		}

		if($qixian != 0 && $qixian <= 15 && $can_invest == true) {
			return true;
		}

		$buf = strstr($buf, '/ul>'); //项目结尾标记

	}

	return false;
}


?>
