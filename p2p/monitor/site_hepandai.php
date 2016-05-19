<?php

$FlAG_DEBUG = false;

if($FlAG_DEBUG == true) {
	echo can_invest_hepandai()."\n";
}
	
/*************************************************************************************************************************/

function can_invest_hepandai() { //新站点这里要注意修改

	$buf = file_get_contents("http://www.hepandai.com/product/p/1");
	$buf = mb_convert_encoding($buf, "gbk", "utf-8");
	//echo $buf;

	while( ($buf = strstr($buf, '/product/Detail')) != false ) { //项目开头标记

		$item_buf = substr($buf, 0, strpos($buf, '申请</a>')); //项目结尾标记
		//echo $item_buf."\n";

		$qixian = 0;

		if( ($line_str = strstr($item_buf, '定期通S')) != false) {
			//echo $line_str."\n";
			$s = strstr($line_str, '<li style="width: 150px; color: orange"');
			//echo $s."\n";		
			$s = substr($s, 0, strpos($s, '/li>'));
			//echo $s."\n";
			preg_match("|>(.*)天|U", $s, $out);
			if(count($out) > 0) {
				$qixian = trim($out[1]);
				echo "qixian:".$qixian."\n";
			}
		}

		if($qixian != 0 && $qixian <= 7) {
			return true;
		}

		$buf = strstr($buf, '申请</a>'); //项目结尾标记

	}

	return false;
}


?>
