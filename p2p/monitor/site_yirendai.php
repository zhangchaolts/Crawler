<?php

$FlAG_DEBUG = false;

if($FlAG_DEBUG == true) {
	echo can_invest_yirendai()."\n";
}

/*************************************************************************************************************************/

function can_invest_yirendai() { //��վ������Ҫע���޸�

	$buf = file_get_contents("http://www.yirendai.com/finance/list/1");
	$buf = mb_convert_encoding($buf, "gbk", "utf-8");
	//echo $buf;

	$ptr = 0;

	while( ($buf = strstr($buf, '<div class="ydy_banner ydy_banner_two clearfix">')) != false ) { //��Ŀ��ͷ���

		$ptr++;

		$item_buf = substr($buf, 0, strpos($buf, 'value="����"')); //��Ŀ��β���
		//echo $item_buf."\n";

		$name = "";

		if( ($line_str = strstr($item_buf, 'href="/finance/view')) != false) {  //�ؼ����ݵĿ�ͷ���
			$s = substr($line_str, 0, strpos($line_str, 'span>')); //�ؼ����ݵĽ�β���
			$s = str_replace("\n","", $s);
			//echo $s."\n";
			preg_match("|>(.*)<|", $s, $out);
			if(count($out) > 0) {
				$name = trim($out[1]);
				echo "name:".$name."; ";
			}
		}

		$qixian = 0;

		if( ($line_str = strstr($item_buf, '<span class="months"><')) != false) {
			$s = substr($line_str, 0, strpos($line_str, '/em>'));
			preg_match("|em>(.*)<|U", $s, $out);
			if(count($out) > 0) {
				$qixian = trim($out[1]);
				echo "qixian:".$qixian."\n";
			}
		}

		if($qixian != 0 && $qixian == 1 && $name == "�ڽڸ�") {
			return true;
		}

		$buf = strstr($buf, 'value="����"'); //��Ŀ��β���

	}

	return false;
}


?>
