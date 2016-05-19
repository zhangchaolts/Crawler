<?php

$FlAG_DEBUG = false;
#$FlAG_DEBUG = true;

if($FlAG_DEBUG == true) {
	echo can_invest_dtd365()."\n";
}
	
/*************************************************************************************************************************/

function can_invest_dtd365() { //新站点这里要注意修改

	$buf = file_get_contents("http://www.dtd365.com/invest/index.html?borrow_type=&page=1&order=pubdate_up");
	//$buf = mb_convert_encoding($buf, "gbk", "utf-8");
	//echo $buf;

	while( ($buf = strstr($buf, '<h2 class="p2pItemTit">')) != false ) { //项目开头标记

		$item_buf = substr($buf, 0, strpos($buf, 'btn_bottow_cando')); //项目结尾标记
		//echo $item_buf."\n\n";

		$item_buf = str_replace("\n", "", $item_buf);
		$item_buf = str_replace("\r", "", $item_buf);
		//echo $item_buf."\n\n\n\n";

		if(strstr($item_buf, '猴年') != false) {
			$buf = strstr($buf, 'btn_bottow_cando'); //项目结尾标记
			continue;
		}

		$qixian_month = "";
		$qixian_day = "";

		if( ($part_str = strstr($item_buf, '借款金额')) != false) {
			preg_match('/<p><strong>(.*?)个月</', $part_str, $out);
			if(count($out) > 0) {
				$qixian_month = trim($out[1]);
				echo "qixian_month:".$qixian_month."\n";
			}
			preg_match('/<p><strong>(.*?)天</', $part_str, $out);
			if(count($out) > 0) {
				$qixian_day = trim($out[1]);
				echo "qixian_day:".$qixian_day."\n";
			}
		}

		$jindu = 0;

		if( ($part_str = strstr($item_buf, 'k_schedule')) != false) {
			preg_match('/<small>(.*?)%/', $part_str, $out);
			if(count($out) > 0) {
				$jindu = trim($out[1]);
				echo "jindu:".$jindu."\n";
			}
		}

		if( ( ($qixian_month != "" && $qixian_month >= 2) || ($qixian_day != "" && $qixian_day >= 60) ) && ($jindu > 0 && $jindu < 95) ) {
			return true;
		}

		$buf = strstr($buf, 'btn_bottow_cando'); //项目结尾标记

	}

	return false;
}


?>
