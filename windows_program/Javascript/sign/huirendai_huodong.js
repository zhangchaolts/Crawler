var my_usernames = [ "zhangxm0713", "caixl0713"];
var my_passwords = ["123456q", "123456q"];

var ie=WScript.createobject("InternetExplorer.Application"); 
ie.Visible=true;//设置ie界面可见

for(var i = 0; i < my_usernames.length ; i++) {

	//打开惠人贷登陆页面
	ie.Navigate("http://www.huirendai.com/index.php?user&q=action/login");
	while(ie.busy){WScript.sleep(2000);}//等待页面加载完毕
	
	//填写账号密码进行登陆
	if(ie.document.getElementById("keywords") != undefined && ie.document.getElementById("password") != undefined) { 
		ie.document.getElementById("keywords").value = my_usernames[i];
		WScript.sleep(500);//停留一秒钟方便观察
		ie.document.getElementById("password").value = my_passwords[i];
		WScript.sleep(500);
		ie.document.getElementById("btnSubmit").click();
		WScript.sleep(2000);
	}
	
	//打开活动页面
	ie.Navigate("http://www.huirendai.com/index.php?activity&q=award"); 
	while(ie.busy){WScript.sleep(2000);}
	
	//点击抽奖按钮
	var ptr = 0
	while(ptr < 10) {
		ptr++
		if(ie.document.getElementById("lotteryBtn") != undefined) {
			ie.document.getElementById("lotteryBtn").click();
			WScript.sleep(5000);
			if(ie.document.getElementsByClassName("close")[0] != undefined) {
				ie.document.getElementsByClassName("close")[0].click();
				WScript.sleep(500);
			}
		}
	}
	
	//退出个人页面
	ie.Navigate("http://www.huirendai.com/?user&q=action/logout"); 
	while(ie.busy){WScript.sleep(2000);}
}

ie.quit()