<?php

$FlAG_DEBUG = false;
//$FlAG_DEBUG = true;

if($FlAG_DEBUG == true) {
	echo can_invest_yourong()."\n";
}
	
/*************************************************************************************************************************/

function can_invest_yourong() { //��վ������Ҫע���޸�

	$buf = file_get_contents("https://www.yrw.com/products/list-all-all-investing-1.html");
	$buf = mb_convert_encoding($buf, "gbk", "utf-8");
	#echo $buf;

	while( ($buf = strstr($buf, '<div class="m-pbox-wrap">')) != false ) { //��Ŀ��ͷ���

		$item_buf = substr($buf, 0, strpos($buf, '����Ͷ��</a>')); //��Ŀ��β���
		//echo $item_buf."\n";

		if(strstr($item_buf, 'u-newCustomer-tag') != false || strstr($item_buf, '������') != false || strstr($item_buf, '������') != false) {
			$buf = strstr($buf, '����Ͷ��</a>'); //��Ŀ��β���
			continue;
		}
		
		$qixian = 0;

		if( ($line_str = strstr($item_buf, '<strong class="u-pbox-data">')) != false) {
			//echo $line_str."\n";
			$s = substr($line_str, 0, strpos($line_str, 'class="f-fs18">��</span>'));
			//echo $s."\n";
			$s = substr($s, strpos($line_str, '<em class="f-ff-amount f-fs38"'));
			//echo $s."\n";
			preg_match("|>(.*)<|U", $s, $out);
			if(count($out) > 0) {
				$qixian = trim($out[1]);
				echo "qixian:".$qixian."\n";
			}
		}

		if($qixian != 0 && $qixian > 20 && $qixian <= 35) {
			return true;
		}

		$buf = strstr($buf, '����Ͷ��</a>'); //��Ŀ��β���

	}

	return false;
}


?>
