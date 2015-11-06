var my_usernames = [ "13158424485", "13158422410"];
var my_passwords = ["123456q", "123456q"];

var ie = WScript.createobject("InternetExplorer.Application"); 
ie.Visible = true;//设置ie界面可见

for(var i = 0; i < my_usernames.length; i++) {

	//打开登陆页面
	ie.Navigate("http://www.minxindai.com/?m=user&c=login");
	while(ie.busy){WScript.sleep(2000);}//等待页面加载完毕

	//填写账号密码进行登陆
	if(ie.document.getElementsByName("userName")[0] != undefined && ie.document.getElementsByName("password")[0] != undefined) { 
		ie.document.getElementsByName("username")[0].value = my_usernames[i];
		WScript.sleep(500);//停留一秒钟方便观察
		ie.document.getElementsByName("password")[0].value = my_passwords[i];
		WScript.sleep(500);
		ie.document.getElementById("loginBt").click();
		WScript.sleep(3000);
	}
	
	//打开个人页面
	ie.Navigate("http://www.minxindai.com/?m=center"); 
	while(ie.busy){WScript.sleep(3000);}
	
	//点击签到按钮
	if(ie.document.getElementsByClassName("sign")[0] != undefined) {
		ie.document.getElementsByClassName("sign")[0].click();
		WScript.sleep(2000);
		if(ie.document.getElementsByClassName("close")[0] != undefined) {
			ie.document.getElementsByClassName("close")[0].click();
			WScript.sleep(2000);
		}
	}
	
	//退出个人页面
	ie.Navigate("http://www.minxindai.com/?m=user&a=logout "); 
	while(ie.busy){WScript.sleep(3000);}
}

ie.quit()