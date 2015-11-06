
sign();

setTimeout(function() {
	jump();
}, 1000);

function sign() {
	for(var i = 0; i < document.getElementsByTagName("button").length; i++) {
		if(document.getElementsByTagName("button")[i].innerHTML == "签到领惠米") {
			document.getElementsByTagName("button")[i].click();
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




