<?php

$FlAG_DEBUG = false;
//$FlAG_DEBUG = true;

if($FlAG_DEBUG == true) {
    echo can_invest_huirendai()."\n";
}

/*************************************************************************************************************************/

function can_invest_huirendai() { //��վ������Ҫע���޸�

	$buf = file_get_contents("http://m.huirendai.com/invest");
	$buf = mb_convert_encoding($buf, "gbk", "utf-8");
	//echo $buf;

	$is_find = false;

	while( ($buf = strstr($buf, '<li><a href="/invest/borrow/detail/')) != false ) { //��Ŀ��ͷ���

		$item_buf = substr($buf, 0, strpos($buf, '<div class="process"')); //��Ŀ��β���
		//echo $item_buf."\n";

		$item_buf = str_replace("\n", "", $item_buf);
		$item_buf = str_replace("\r", "", $item_buf);
		$item_buf = str_replace("\t", "", $item_buf);
		$item_buf = str_replace(" ", "", $item_buf);
		//echo $item_buf."\n\n\n\n";

		if(strstr($item_buf, '<strong>+5%</strong>') != false) {
			$buf = strstr($buf, '<div class="process"'); //��Ŀ��β���
			continue;
		}

		//echo $item_buf."\n";

		$rate = 0;

		if( ($line_str = strstr($item_buf, '<spanclass="rate">')) != false) {
			$s = substr($line_str, 0, strpos($line_str, '/span>'));
			//echo $s."\n";
			preg_match("|>(.*)%<|U", $s, $out);
			if(count($out) > 0) {
				$rate = trim($out[1]);
				echo "rate:".$rate."; ";
			}
		}

		$qixian1 = 0;

		if( ($line_str = strstr($item_buf, '����<strong>')) != false) {
			$s = substr($line_str, 0, strpos($line_str, '/strong></span><span>��Ͷ���'));
			//echo $s."\n";
			preg_match("|>(.*)����|U", $s, $out);
			if(count($out) > 0) {
				$qixian1 = trim($out[1]);
				echo "qixian1:".$qixian1."; ";
			}
		}

		$money = 0;
		if( ($line_str = strstr($item_buf, '��Ͷ���<strong>')) != false) {
			$s = substr($line_str, 0, strpos($line_str, '/strong></span></div>'));
			preg_match("|>(.*)Ԫ|U", $s, $out);
			if(count($out) > 0) {
				$money = trim($out[1]);
				echo "money:".$money."\n";
			}
		}

		if($qixian1 != 0 && $qixian1 == 1 && $rate != 0 && $rate < 9.0 && $money > 2000) {
			//return true;
			$is_find = true;
		}

		$buf = strstr($buf, '<div class="process"'); //��Ŀ��β���
	}

	if($is_find == true) {
		return true;
	}

	return false;
}

?>
