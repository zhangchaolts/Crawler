

exit();


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

