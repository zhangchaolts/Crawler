var my_usernames = ["账号1", "账号2"];
var my_passwords = ["密码1", "密码2"];


for(var i = 0; i < my_usernames.length; i++) {
	if(!sessionStorage[i]) {
		sessionStorage[i] = "false";
	}
}

for(var i = 0; i < my_usernames.length; i++) {
	if(sessionStorage[i] == "false") {
		sessionStorage[i] = "true";
		login(my_usernames[i], my_passwords[i]);
		break;
	}
}

function login(username, password) {
	if(document.getElementById("username-login") != undefined && document.getElementById("password-login") != undefined) {  
		document.getElementById("username-login").value = username;
		document.getElementById("password-login").value = password;
		for(var i = 0;i < document.getElementsByClassName("bannerSubmit").length; i++) {
			if(document.getElementsByClassName("bannerSubmit")[i].innerHTML == "登录") {
			document.getElementsByClassName("bannerSubmit")[i].click();
			break;
			}
		}
	}
}




