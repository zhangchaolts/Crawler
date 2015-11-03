<?php

$FlAG_DEBUG = false;
#$FlAG_DEBUG = true;

if($FlAG_DEBUG == true) {
    echo can_invest_huirendai()."\n";
}

/*************************************************************************************************************************/

function can_invest_huirendai() { //新站点这里要注意修改

	$buf = file_get_contents("http://www.huirendai.com/invest/index.html");
	$buf = mb_convert_encoding($buf, "gbk", "utf-8");
	//echo $buf;

	$is_find = false;

	while( ($buf = strstr($buf, '<div class="invest-item">')) != false ) { //项目开头标记

		$item_buf = substr($buf, 0, strpos($buf, 'data-modal-url="/invest/detail')); //项目结尾标记
		//echo $item_buf."\n";
		
		if(strstr($item_buf, '新用户限投一次') != false || strstr($item_buf, '满标复审') != false) {
			$buf = strstr($buf, 'data-modal-url="/invest/detail'); //项目结尾标记
			continue;
		}

		#echo $item_buf."\n";

		$rate = 0;

		if( ($line_str = strstr($item_buf, '<span class="rate">')) != false) {
			$s = substr($line_str, 0, strpos($line_str, 'em>%'));
			$s = str_replace("\n", "", $s);
			preg_match("|>(.*)<|U", $s, $out);
			if(count($out) > 0) {
				$rate = trim($out[1]);
				echo "rate:".$rate."; ";
			}
		}

		$qixian1 = 0;
		$qixian2 = 0;

		if( ($line_str = strstr($item_buf, '<span class="inves-qx">')) != false) {
			//echo $line_str."\n";
			$s = substr($line_str, 0, strpos($line_str, '<strong>'));
			//echo $s."\n";
			//$s = substr($s, strpos($line_str, '<p>') + 3);
			//echo $s."\n";
			preg_match("|>(.*)个月|U", $s, $out);
			if(count($out) > 0) {
				$qixian1 = trim($out[1]);
				echo "qixian1:".$qixian1."\n";
			}
			preg_match("|>(.*)天|U", $s, $out);
			if(count($out) > 0) {
				$qixian2 = trim($out[1]);
				echo "qixian2:".$qixian2."\n";
			}
		}

		if( ( ($qixian1 != 0 && $qixian1 == 1) || ($qixian2 != 0 && 15 <= $qixian2 && $qixian2 <= 35) ) && $rate != 0 && $rate < 12.0) {
			//return true;
			$is_find = true;
		}

		$buf = strstr($buf, 'data-modal-url="/invest/detail'); //项目结尾标记
	}

	if($is_find == true) {
		return true;
	}

	return false;
}

?>
