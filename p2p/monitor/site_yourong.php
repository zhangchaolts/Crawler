<?php

$FlAG_DEBUG = false;

if($FlAG_DEBUG == true) {
	echo can_invest_yourong()."\n";
}
	
/*************************************************************************************************************************/

function can_invest_yourong() { //��վ������Ҫע���޸�

	$buf = file_get_contents("http://www.yourong.cn/products/list-all-investing-1.html");
	$buf = mb_convert_encoding($buf, "gbk", "utf-8");
	//echo $buf;

	while( ($buf = strstr($buf, '<div class="m-pbox-wrap">')) != false ) { //��Ŀ��ͷ���

		$item_buf = substr($buf, 0, strpos($buf, '<div class="u-pbox-footer">')); //��Ŀ��β���
		//echo $item_buf."\n";

		$qixian = 0;

		if( ($line_str = strstr($item_buf, '<strong class="u-pbox-data">')) != false) {
			//echo $line_str."\n";
			$s = substr($line_str, 0, strpos($line_str, '/em><span class="f-fs18">��</span>'));
			//echo $s."\n";
			$s = substr($s, strpos($line_str, '<em class="f-ff-amount f-fs38"'));
			//echo $s."\n";
			preg_match("|>(.*)<|U", $s, $out);
			if(count($out) > 0) {
				$qixian = trim($out[1]);
				echo "qixian:".$qixian."\n";
			}
		}

		if($qixian != 0 && $qixian <= 27) {
			return true;
		}

		$buf = strstr($buf, '<div class="u-pbox-footer">'); //��Ŀ��β���

	}

	return false;
}


?>