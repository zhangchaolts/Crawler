<?php

$FlAG_DEBUG = false;
#$FlAG_DEBUG = true;

if($FlAG_DEBUG == true) {
	echo can_invest_gujinsuo()."\n";
}
	
/*************************************************************************************************************************/

function can_invest_gujinsuo() { //��վ������Ҫע���޸�

	$buf = file_get_contents("https://www.gujinsuo.com.cn/index.html");
	$buf = mb_convert_encoding($buf, "gbk", "utf-8");
	//echo $buf;

	while( ($buf = strstr($buf, '<div class="gjs_fjbinner_bg"></div>')) != false ) { //��Ŀ��ͷ���

		$item_buf = substr($buf, 0, strpos($buf, '<i class="after"></i></a>')); //��Ŀ��β���
		//echo $item_buf."\n";

		$qixian = 0;

		if( ($line_str = strstr($item_buf, 'Ͷ������')) != false) {
			$s = str_replace("\n", "", $line_str);
			$s = str_replace("\r", "", $s);
			//echo $s."\n";
			preg_match('/"span3">(.*?)&nbsp;��</', $s, $out);
			if(count($out) > 0) {
				$qixian = trim($out[1]);
				echo "qixian:".$qixian."\n";
			}
		}

		$jindu = 0;
		if( ($line_str = strstr($item_buf, 'progress progress-warning progress-striped h10')) != false) {
			$s = str_replace("\n", "", $line_str);
			$s = str_replace("\r", "", $s);
			//echo $s."\n";
			preg_match('/>&nbsp;(.*?)%</', $s, $out);
			if(count($out) > 0) {
				$jindu = trim($out[1]);
				echo "jindu:".$jindu."\n";
			}
		}

		if($qixian != 0 && $qixian <= 38 && $jindu > 0 && $jindu < 95) {
			return true;
		}

		$buf = strstr($buf, '<i class="after"></i></a>'); //��Ŀ��β���

	}

	return false;
}


?>
