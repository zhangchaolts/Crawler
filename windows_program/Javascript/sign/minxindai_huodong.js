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
	
	//打开活动页面
	ie.Navigate("http://www.minxindai.com/?m=event&c=jfturntab"); 
	while(ie.busy){WScript.sleep(2000);}
	

  //点击抽奖按钮
	var ptr = 0
	while(ptr < 6) {
		ptr++
		if(ie.document.getElementById("zhizhen") != undefined) {
			ie.document.getElementById("zhizhen").click();
			WScript.sleep(7000);
			if(ie.document.getElementById("cboxClose") != undefined) {
				ie.document.getElementById("cboxClose").click();
				WScript.sleep(500);
			}
		}
	}
	
	//退出个人页面
	ie.Navigate("http://www.minxindai.com/?m=user&a=logout "); 
	while(ie.busy){WScript.sleep(3000);}
}

ie.quit()