<?php

$FlAG_DEBUG = false;
#$FlAG_DEBUG = true;

if($FlAG_DEBUG == true) {
	echo can_invest_yourong_notice()."\n";
}
	
/*************************************************************************************************************************/

function can_invest_yourong_notice() { //��վ������Ҫע���޸�

	$buf = file_get_contents("https://www.yrw.com/products/list-all-investing-1.html");
	$buf = mb_convert_encoding($buf, "gbk", "utf-8");
	#echo $buf;

	while( ($buf = strstr($buf, ' <h2 class="u-side-title">����Ԥ��</h2>')) != false ) { //��Ŀ��ͷ���

		$item_buf = substr($buf, 0, strpos($buf, ' <h3 class="u-side-title">�û�����Ͷ��</h3>')); //��Ŀ��β���
		#echo $item_buf."\n";

		$item_buf = str_replace("\n","", $item_buf);
		$item_buf = str_replace("\r","", $item_buf);
		$item_buf = str_replace(" ","", $item_buf);
		#echo $item_buf."\n";

		$title = "";
		preg_match('|target="_blanck">(.*?)</a></strong>|U', $item_buf, $out);
		if(count($out) > 0) {
			$title = trim($out[1]);
			echo "title:".$title."\n";
		}

		$qixian = 0;
		preg_match('|����������<strong>(.*?)��</strong>|U', $item_buf, $out);
		if(count($out) > 0) {
			$qixian = trim($out[1]);
			echo "qixian:".$qixian."\n";
		}

		$publish_time = "";
		preg_match('|����ʱ�䣺<strong>(.*?)</strong>|U', $item_buf, $out);
		if(count($out) > 0) {
			$publish_time = trim($out[1]);
			#echo "publish_time:".$publish_time."\n";
		}
		if ($publish_time != "") {
			$publish_time = substr($publish_time, strlen("2015-11-11"));
			echo "publish_time:".$publish_time."\n";
		}

		if(strstr($title, '������') == false && $qixian != 0 && $qixian <= 32) {
			return true;
		}

		$buf = strstr($buf, ' <h3 class="u-side-title">�û�����Ͷ��</h3>'); //��Ŀ��β���
	}

	return false;
}


?>
