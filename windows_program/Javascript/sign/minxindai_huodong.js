var my_usernames = [ "13158424485", "13158422410"];
var my_passwords = ["123456q", "123456q"];

var ie = WScript.createobject("InternetExplorer.Application"); 
ie.Visible = true;//����ie����ɼ�

for(var i = 0; i < my_usernames.length; i++) {

	//�򿪵�½ҳ��
	ie.Navigate("http://www.minxindai.com/?m=user&c=login");
	while(ie.busy){WScript.sleep(2000);}//�ȴ�ҳ��������

	//��д�˺�������е�½
	if(ie.document.getElementsByName("userName")[0] != undefined && ie.document.getElementsByName("password")[0] != undefined) { 
		ie.document.getElementsByName("username")[0].value = my_usernames[i];
		WScript.sleep(500);//ͣ��һ���ӷ���۲�
		ie.document.getElementsByName("password")[0].value = my_passwords[i];
		WScript.sleep(500);
		ie.document.getElementById("loginBt").click();
		WScript.sleep(3000);
	}
	
	//�򿪻ҳ��
	ie.Navigate("http://www.minxindai.com/?m=event&c=jfturntab"); 
	while(ie.busy){WScript.sleep(2000);}
	

  //����齱��ť
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
	
	//�˳�����ҳ��
	ie.Navigate("http://www.minxindai.com/?m=user&a=logout "); 
	while(ie.busy){WScript.sleep(3000);}
}

ie.quit()