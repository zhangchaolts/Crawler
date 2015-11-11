<?php
include('blog_get_site_sitename_map.php');
include('blog_get_site_period_map.php');
include('blog_get_mail_list.php');

$url = "http://runningyangmao.blog.163.com/blog/static/25166910920157634424666";

$site_sitename_map = get_site_sitename_map($url);
print_r($site_sitename_map);

$site_period_map = get_site_period_map($url);
print_r($site_period_map);

$site_last_can_invest_timestamp_map = array();

while(true) {

	echo "----------------------------------------------------------------------------------------------------\n";

	$now_time = date("Y-m-d H:i:s");
	echo $now_time."\n\n";

	$parts1 = explode(":", $now_time);
	if(count($parts1) == 3) {
		$minute = $parts1[1];
		//echo $minute."\n";
		if($minute <= 3) {
			//echo $minute."\n";
			$site_sitename_map = get_site_sitename_map($url);
			$site_period_map = get_site_period_map($url);
		}
	}

	foreach($site_sitename_map as $site => $sitename) {
		echo "site:".$site."\n";
		$timestamp_diff = -1;
		if(isset($site_last_can_invest_timestamp_map[$site]) == true) {
			$timestamp_diff = strtotime("now") - $site_last_can_invest_timestamp_map[$site];
		}
		echo "timestamp_diff:".$timestamp_diff."\n";

		$timestamp_span_threshold = 3600;
		if(isset($site_period_map[$site]) == true) {
			$timestamp_span_threshold = $site_period_map[$site] * 60;
		}

		if($timestamp_diff == -1 || $timestamp_diff > $timestamp_span_threshold) {
			include_once("site_".$site.".php");
			$is_can_invest = call_user_func("can_invest_".$site);
			echo $sitename."is_can_invest:".$is_can_invest."\n";

			if($is_can_invest == true) {
				$mail_list = get_mail_list($url, $sitename);
				print_r($mail_list);
				//$mail_list = array("43228637@qq.com");

				$mail_title = "[¼à¿Ø]".$sitename."ÓÐ±êÀ²~";
				$mail_body = "";
				foreach($mail_list as $index1 => $mail_box) {
					system('echo '.$mail_body.' | mail -s "'.$mail_title.'" '."$mail_box");
				}

				$site_last_can_invest_timestamp_map[$site] = strtotime("now");
			}
		}

		echo "\n";
		sleep(60);
	}

}

?>
