
//var my_usernames = ["zhangchao822", "wangluyao1215", "zhangxm0713", "caixl0713"];
//var my_passwords = ["csujk4236238", "csujk4236238", "csujk4236238", "csujk4236238"];
var my_usernames = ["zhangchao822"];
var my_passwords = ["csujk4236238"];

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
	if(document.getElementById("keywords") != undefined && document.getElementById("password") != undefined) {  
		document.getElementById("keywords").value = username;
		document.getElementById("password").value = password;
		document.getElementById("btnSubmit").click();
	}
}




