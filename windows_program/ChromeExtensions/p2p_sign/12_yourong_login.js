
//var my_usernames = ["zhangchaolts", "wangluyaolts", "zhangxmlts", "caixllts"];
//var my_passwords = ["csujk4236238", "csujk4236238", "csujk4236238", "csujk4236238"];
var my_usernames = ["zhangchaolts"];
var my_passwords = ["csujk4236238"];

for(var i = 0; i < my_usernames.length; i++) {
	if(!sessionStorage[i]) {
		sessionStorage[i] = "false";
	}
}

for(var i = 0; i < my_usernames.length; i++) {
	if(sessionStorage[i] == "false") {
		//alert(my_usernames[i]);
		sessionStorage[i] = "true";
		login(my_usernames[i], my_passwords[i]);
		break;
		//alert("ok");
	}
}


function login(username, password) {
	if(document.getElementsByName("username")[0] != undefined && document.getElementsByName("password")[0] != undefined) { 
		document.getElementsByName("username")[0].value = username;
		document.getElementsByName("password")[0].value = password;
		document.getElementById("j-login-submit").click();
	}
}




