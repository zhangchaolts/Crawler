<?php

$FlAG_DEBUG = false;

if($FlAG_DEBUG == true) {
	$mail_list = array("43228637@qq.com");
	$sitename = "���˴�";
	send_mail($mail_list, $sitename);
}

/********************************************************************************************************************************/

function send_mail($mail_list, $sitename) {
	foreach($mail_list as $index => $mail_box) {
		$mail_title = $sitename."�б���~";
		$mail_body = "��������";
		system('echo '.$mail_body.' | mail -s "[��������]'.$mail_title.'" '.$mail_box);
	}
}

?>
