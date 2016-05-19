<?php

$FlAG_DEBUG = false;
$FlAG_DEBUG = true;

if($FlAG_DEBUG == true) {
    echo can_invest_mindai()."\n";
}

/*************************************************************************************************************************/

function can_invest_mindai() { //新站点这里要注意修改

	$buf = file_get_contents("https://www.mindai.com/grtzlc?app_type=youxuan&ui_type=inline&order=default&currentPage=1");
	$buf = mb_convert_encoding($buf, "gbk", "utf-8");
	//echo $buf;

	$is_find = false;

	while( ($buf = strstr($buf, '<div class="sma_sign">')) != false ) { //项目开头标记

		$item_buf = substr($buf, 0, strpos($buf, '<a href="tender!borrow_content')); //项目结尾标记
		//echo $item_buf."\n";

		$item_buf = str_replace("\n", "", $item_buf);
		$item_buf = str_replace("\r", "", $item_buf);
		$item_buf = str_replace("\t", "", $item_buf);
		$item_buf = str_replace(" ", "", $item_buf);
		echo $item_buf."\n\n\n\n";

		if(strstr($item_buf, '"status":"OPENED"') == false) {
			$buf = strstr($buf, '{"id":"'); //项目结尾标记
			continue;
		}

		//echo $item_buf."\n";

		$qixian1 = 0;

		if( ($line_str = strstr($item_buf, '"duration":{"year":0,')) != false) {
			$s = substr($line_str, 0, strpos($line_str, ',"corpName"'));
			//echo $s."\n";
			preg_match("|\"day\":(.*)}|U", $s, $out);
			if(count($out) > 0) {
				$qixian1 = trim($out[1]);
				echo "qixian1:".$qixian1."; ";
			}
		}

		$money = 0;
		if( ($line_str = strstr($item_buf, '"balanceAmount":')) != false) {
			$s = substr($line_str, 0, strpos($line_str, '"investRule":'));
			preg_match("|\"balanceAmount\":(.*),|U", $s, $out);
			if(count($out) > 0) {
				$money = trim($out[1]);
				echo "money:".$money."\n";
			}
		}

		if($qixian1 != 0 && $qixian1 <= 40  && $money >= 20000) {
			//return true;
			$is_find = true;
		}

		$buf = strstr($buf, '<a href="tender!borrow_content'); //项目结尾标记
	}

	if($is_find == true) {
		return true;
	}

	return false;
}

?>
