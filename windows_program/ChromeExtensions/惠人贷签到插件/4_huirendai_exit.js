setTimeout(function() {
	exit();
}, 1000);

function exit() {
	for(var i = 0;i < document.getElementsByTagName("a").length; i++) {
		if(document.getElementsByTagName("a")[i].innerHTML == "[退出]") {
			document.getElementsByTagName("a")[i].click();
			break;
		}
	}
}

function exit2() {
	for(var i = 0;i < document.getElementsByClassName("login-out").length; i++) {
		alert(333);
		if(document.getElementsByClassName("login-out")[i].innerHTML == "[退出]") {
			document.getElementsByClassName("login-out")[i].click();
			break;
		}
	}
}