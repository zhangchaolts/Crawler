<?php
/*
	参数：
	$from_name - 发信人姓名
	$from_mail - 发信人email
	$subject - 邮件标题
	$body - 邮件内容
	$mode - 邮件类型，html或txt //一般是html
	$maillist - 收信人邮箱，多个邮箱用";"分隔/或array
	$attfilename - 附件文件名(只测试相对路径OK)，没有留空
	$method - post或get 方式（一般post），注意附件太大会被截断（get 方式保留2000字节，post方式保留了10000字节）
	
*/

	$from_mail = $argv[1];
	$from_name = $argv[2];
	$maillist = $argv[3];
	$subject = $argv[4];
	$body_file = $argv[5];
	$attfilename = $argv[6];

	$fp_in = fopen($body_file, "r");
	$mail_body = "";
	while(!feof($fp_in)) {
        	$line = fgets($fp_in, 1024);
        	$mail_body .= $line;
	}
	fclose($fp_in);

	if(strlen($mail_body) > 2000) {
		$mail_body=substr($mail_body, 0, 2000);
	}

	sendmail($from_mail,$from_name,$subject,$mail_body,$maillist,$attfilename);

	function sendmail($from_mail,$from_name,$subject,$body,$maillist,$attfilename="",$method="post",$mode="txt"){
		if(is_array($maillist))
			$maillist=implode(";",$maillist);
		
		$maillist_e	=	urlencode($maillist);
		if($mode == "html")
			$body=str_replace("\n","<br>",$body);

		$body_e		=	urlencode($body);
		
		/*read attachment*/	
		$attbody_e="";
		$attfilename_e="";
		if(empty($attfilename)){/*no file*/
			$attbody="";	
		}else{
			$attbody	=	file_get_contents($attfilename);
			if($attbody == false)
				$attbody="";
			else{
				if($method=="get" && strlen($attbody)>2000)
					$attbody=substr($attbody,0,2000);
				else if($method=="post" && strlen($attbody)>10000)
					$attbody=substr($attbody,0,10000);
				$attbody_e=urlencode($attbody);
			}
			$attfilename_e	=	urlencode($attfilename);
		}
		$subject_e	=	urlencode($subject);

		if($method == "get"){
			$url="http://portal.sys.sogou-op.org/portal/tools/send_mail.php?uid=${from_mail}&fr_name=${from_name}&fr_addr=${from_mail}&title=$subject_e&body=$body_e&mode=$mode&maillist=$maillist&attname=$attfilename_e&attbody=$attbody_e";
			#echo "$url\n";
			file_get_contents($url);
		}else{ //post
			$mail_data=array(
			'uid' => $from_mail,
			'fr_name'=> $from_name,
			'fr_addr'=> $from_mail,
			'title' => $subject,
			'body' => $body,
			'mode' => $mode,
			'maillist' => $maillist,
			'attbody' => $attbody,
			'attname' => $attfilename
			);
			$ch = curl_init();
			curl_setopt($ch, CURLOPT_URL, "http://portal.sys.sogou-op.org/portal/tools/send_mail.php");
			curl_setopt($ch, CURLOPT_POST, 1);
			curl_setopt($ch, CURLOPT_POSTFIELDS, $mail_data);
			curl_setopt($ch, CURLOPT_TIMEOUT, 30);
			curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
			curl_setopt($ch, CURLOPT_HEADER, 0);
			$response = curl_exec($ch);
			curl_close($ch);
		}
	}
?>
