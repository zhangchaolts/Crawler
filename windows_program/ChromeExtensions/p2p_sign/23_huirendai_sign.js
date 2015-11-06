
sign();

setTimeout(function() {
	jump();
}, 1000);

//exit();

function sign() {
	for(var i = 0; i < document.getElementsByTagName("button").length; i++) {
		if(document.getElementsByTagName("button")[i].innerHTML == "签到领惠米") {
			document.getElementsByTagName("button")[i].click();
			sleep(1000);
			break;
		}
	}
}

function jump(){
	for(var i = 0; i < document.getElementsByTagName("a").length; i++) {
		if(document.getElementsByTagName("a")[i].innerHTML == "- 我的惠米") {
			document.getElementsByTagName("a")[i].click();
			break;
		}
	}
}

function exit() {
	for(var i = 0; i < document.getElementsByTagName("a").length; i++) {
		if(document.getElementsByTagName("a")[i].innerHTML == "退出") {
			document.getElementsByTagName("a")[i].click();
			break;
		}
	}
}

function sleep(sleepTime) {
	for(var start = Date.now(); Date.now() - start <= sleepTime; ) { } 
}




