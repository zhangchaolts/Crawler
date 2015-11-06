
var my_usernames = ["账号1", "账号2"];
var my_passwords = ["密码1", "密码2"];

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




