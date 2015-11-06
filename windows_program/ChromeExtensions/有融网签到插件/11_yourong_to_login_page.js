

exit();
to_login_page();

function exit() {
	for(var i = 0;i < document.getElementsByTagName("a").length; i++) {
		if(document.getElementsByTagName("a")[i].innerHTML == "退出") {
			document.getElementsByTagName("a")[i].click();
			break;
		}
	}
}

function to_login_page(){
	for(var i = 0;i < document.getElementsByTagName("a").length; i++) {
		if(document.getElementsByTagName("a")[i].innerHTML == "登录") {
			document.getElementsByTagName("a")[i].click();
			break;
		}
	}
}



