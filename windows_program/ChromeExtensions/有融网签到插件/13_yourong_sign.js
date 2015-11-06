
sign();

setTimeout(function() {
	jump();
}, 5000);

//exit();

function sign() {
	if(document.getElementById("j-checkin-btn") != undefined) {
		document.getElementById("j-checkin-btn").click();
		//sleep(5000);
	}
}

function jump(){
	for(var i = 0;i < document.getElementsByTagName("a").length; i++) {
		if(document.getElementsByTagName("a")[i].innerHTML == "我的优惠") {
			document.getElementsByTagName("a")[i].click();
			break;
		}
	}
}

function exit() {
	for(var i = 0;i < document.getElementsByTagName("a").length; i++) {
		if(document.getElementsByTagName("a")[i].innerHTML == "退出") {
			document.getElementsByTagName("a")[i].click();
			break;
		}
	}
}

function sleep(sleepTime) {
	for(var start = Date.now(); Date.now() - start <= sleepTime; ) { } 
}




