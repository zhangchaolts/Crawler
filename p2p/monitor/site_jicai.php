<?php

$FlAG_DEBUG = false;

if($FlAG_DEBUG == true) {
	echo can_invest_jicai()."\n";
}
	
/*************************************************************************************************************************/

function can_invest_jicai() { //��վ������Ҫע���޸�

	$buf = file_get_contents("https://m.jicai.com/product/list");
	$buf = mb_convert_encoding($buf, "gbk", "utf-8");
	//echo $buf;

	while( ($buf = strstr($buf, '/product/detail')) != false ) { //��Ŀ��ͷ���

		$item_buf = substr($buf, 0, strpos($buf, '</ul>')); //��Ŀ��β���
		//echo $item_buf."\n";

		$qixian = 0;

		if( ($line_str = strstr($item_buf, 'plist-day')) != false) {
			$s = substr($line_str, 0, strpos($line_str, '/p>'));
			//echo $s."\n";
			preg_match("|>(.*)<|U", $s, $out);
			if(count($out) > 0) {
				$qixian = trim($out[1]);
				//echo "qixian:".$qixian."\n";
			}
		}

		$left = 0;
		if( ($line_str = strstr($item_buf, 'plist-num')) != false) {
            $s = substr($line_str, 0, strpos($line_str, '/p>'));
            //echo $s."\n";
            preg_match("|>(.*)<|U", $s, $out);
            if(count($out) > 0) {
                $left = trim($out[1]);
                //echo "left:".$left."\n";
            }  
		}

		if($left != '0') {
			echo "qixian:".$qixian."\n";
			echo "left:".$left."\n";
		}

		if($qixian != 0 && $qixian <= 35 && $left != '0') {
			return true;
		}

		$buf = strstr($buf, '</ul>'); //��Ŀ��β���

	}

	return false;
}


?>
