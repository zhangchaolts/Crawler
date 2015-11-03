<?php

$FlAG_DEBUG = false;
//$FlAG_DEBUG = true;

if($FlAG_DEBUG == true) {
	echo can_invest_firstp2p()."\n";
}

/*************************************************************************************************************************/

function can_invest_firstp2p() { //新站点这里要注意修改

	//$buf = file_get_contents("http://www.firstp2p.com/deals?p=1&cate=0");

	$cnt=0;   
	while($cnt < 5 && ($buf = file_get_contents("http://www.firstp2p.com/deals?p=1&cate=0")) === FALSE) $cnt++;

	$buf = mb_convert_encoding($buf, "gbk", "utf-8");
	//echo $buf;

	$is_find = false;

	while( ($buf = strstr($buf, '<a title="')) != false ) { //项目开头标记

		$item_buf = substr($buf, strlen('<a title="'), strpos($buf, '<div class="product_btn">')); //项目结尾标记
		//echo $item_buf."\n";

		$is_100 = false;
		if(strstr($item_buf, '100起投') != false) {
			$is_100 = true;
		}

		$qixian = "";

		if( ($line_str = strstr($item_buf, '<span>投资期限：</span>')) != false) {
			//echo $line_str."\n";
			$s = substr($line_str, 0, strpos($line_str, '/i>天</em>'));
			//echo $s."\n";
			$s = substr($s, strpos($line_str, '<i class="f18"'));
			//echo $s."\n";
			preg_match("|>(.*)<|U", $s, $out);
			if(count($out) > 0) {
				$qixian = trim($out[1]);
			}
		}
		echo "qixian:".$qixian."; ";

		$left_money = 0;

		if( ($line_str = strstr($item_buf, '<span>剩余可投：</span')) != false) {
			//echo $line_str."\n";
			$s = substr($line_str, strpos($line_str, '剩余可投：</span'));
			//echo $s."\n";
			preg_match("|>(.*)元<|U", $s, $out);
			if(count($out) > 0) {
				$left_money = $out[1];
				echo "left_money:".$left_money."; ";
			}
		}

		echo "is_100:";
		echo var_dump($is_100);

		if($is_100 == true && $qixian != "" && (startsWith($qixian, "7~") == true || $qixian == "10" || $qixian == "15" || $qixian == "20" || $qixian == "30") && $left_money != '0.00') {
			//return true;
			$is_find = true;
		}

		$buf = strstr($buf, '<div class="product_btn">'); //项目结尾标记

	}

	if($is_find == true) {
		return true;
	}

	return false;
}


function startsWith($str, $sub) {
	return !strncmp($str, $sub, strlen($sub));
}

?>
