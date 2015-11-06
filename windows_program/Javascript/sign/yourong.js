var my_usernames = [ "zhangxmlts", "caixllts"];
var my_passwords = ["123456q", "123456q"];

var ie = WScript.createobject("InternetExplorer.Application"); 
ie.Visible = true;//设置ie界面可见

for(var i = 0; i < my_usernames.length; i++) {

	//打开有融网登陆页面
	ie.Navigate("http://www.yourong.cn/security/login/");
	while(ie.busy){WScript.sleep(2000);}//等待页面加载完毕

	//填写账号密码进行登陆
	if(ie.document.getElementsByName("username")[0] != undefined && ie.document.getElementsByName("password")[0] != undefined) { 
		ie.document.getElementsByName("username")[0].value = my_usernames[i];
		WScript.sleep(500);//停留一秒钟方便观察
		ie.document.getElementsByName("password")[0].value = my_passwords[i];
		WScript.sleep(500);
		ie.document.getElementById("j-login-submit").click();
		WScript.sleep(2000);
	}
	
	//打开个人页面
	ie.Navigate("http://www.yourong.cn/member/home"); 
	while(ie.busy){WScript.sleep(2000);}
	
	//点击签到按钮
	if(ie.document.getElementById("j-checkin-btn") != undefined) {
		ie.document.getElementById("j-checkin-btn").click();
		WScript.sleep(6000);
	}
	
	//退出个人页面
	ie.Navigate("http://www.yourong.cn/member/logout"); 
	while(ie.busy){WScript.sleep(2000);}
}

ie.quit()