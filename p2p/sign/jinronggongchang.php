<?php

$fp_in = fopen("jinronggongchang.log", "r"); 

$line_array = array();
$pos = -1;

$ptr = 0;
while(!feof($fp_in)) {
	$line = trim(fgets($fp_in, 10240));
	if(strlen($line) == 0) {
		continue;
	}
	if(strstr($line, "【") != false) {
		$pos = $ptr;
	}
	$line_array[] = $line;
	$ptr++;
}
fclose($fp_in);

$result = "";

for($i = $pos + 1; $i < count($line_array); $i++) {
	if(strstr($line_array[$i], "true") != false) {
		$result .= $line_array[$i + 1]."\n\n";
	}
}

$tel = substr($result, 0, 11);

if(strlen($tel) >= 11) {

	$mail_title = "金融工场签到获得红包啦~";

	system('echo '.$tel.' | mail -s "'.$mail_title.'" '."82213802@qq.com");
}

?>
