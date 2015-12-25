<?php

$FlAG_DEBUG = false;

if($FlAG_DEBUG == true) {
	echo can_invest_9888()."\n";
}
	
/*************************************************************************************************************************/

function can_invest_9888() { //新站点这里要注意修改

	$buf = file_get_contents("http://www.9888.cn/prdClaims/dataList.shtml?provinceId=&repayPeriod=&tradeMark=&repayMode=&pageNo=&sort=&order=&status=&id=&annualRate=&invitationSite=&queryType=&days=&invitationSiteType=&leanGuaranteeType=");
	$buf = mb_convert_encoding($buf, "gbk", "utf-8");
	//echo $buf;

	while( ($buf = strstr($buf, 'prdName')) != false ) { //项目开头标记

		$item_buf = substr($buf, 0, strpos($buf, '},')); //项目结尾标记
		//echo $item_buf."\n";

		$parts1 = explode(",", $item_buf);

		//print_r($parts1);

		$borrowAmount = -1;
		$completeLoan = -1;
		$repayPeriod = -1;
		$repayMode = -1;
		$annualRate = -1;

		foreach($parts1 as $index1 => $key_value) {
			$parts2 = explode(":", $key_value);
			if(count($parts2) == 2) {
				if($parts2[0] == '"borrowAmount"') {
					$borrowAmount = $parts2[1];
				}
                if($parts2[0] == '"completeLoan"') {
                    $completeLoan = $parts2[1];
                }
                if($parts2[0] == '"repayPeriod"') {
                    $repayPeriod = $parts2[1];
                } 
                if($parts2[0] == '"repayMode"') {
                    $repayMode = $parts2[1];
                } 
                if($parts2[0] == '"annualRate"') {
                    $annualRate = $parts2[1];
                } 
			}
		}

		if(startsWith_9888($repayPeriod, '"') == true && endsWith_9888($repayPeriod, '"') == true && strlen($repayPeriod) >= 3) {
			$repayPeriod = substr($repayPeriod, 1, strlen($repayPeriod) - 2);
		}

		echo $borrowAmount."; ".$completeLoan."; ".$repayPeriod."; ".$repayMode."; ".$annualRate."\n";

		if($borrowAmount > $completeLoan && $repayPeriod <= 25 && $repayMode == 5 && $annualRate <= 9.0) {
			return true;
		}
		
		$buf = strstr($buf, '}]}'); //项目结尾标记

	}

	return false;
}

function startsWith_9888($str, $sub) {
    return !strncmp($str, $sub, strlen($sub));
}

function endsWith_9888($str, $sub) {
    $length = strlen($sub);
    if ($length == 0) {
        return true;
    }
    return (substr($str, -$length) === $sub);
}


?>
