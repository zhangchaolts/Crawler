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
	
	//�򿪸���ҳ��
	ie.Navigate("http://www.minxindai.com/?m=center"); 
	while(ie.busy){WScript.sleep(3000);}
	
	//���ǩ����ť
	if(ie.document.getElementsByClassName("sign")[0] != undefined) {
		ie.document.getElementsByClassName("sign")[0].click();
		WScript.sleep(2000);
		if(ie.document.getElementsByClassName("close")[0] != undefined) {
			ie.document.getElementsByClassName("close")[0].click();
			WScript.sleep(2000);
		}
	}
	
	//�˳�����ҳ��
	ie.Navigate("http://www.minxindai.com/?m=user&a=logout "); 
	while(ie.busy){WScript.sleep(3000);}
}

ie.quit()