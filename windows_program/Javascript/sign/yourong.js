var my_usernames = [ "zhangxmlts", "caixllts"];
var my_passwords = ["123456q", "123456q"];

var ie = WScript.createobject("InternetExplorer.Application"); 
ie.Visible = true;//����ie����ɼ�

for(var i = 0; i < my_usernames.length; i++) {

	//����������½ҳ��
	ie.Navigate("http://www.yourong.cn/security/login/");
	while(ie.busy){WScript.sleep(2000);}//�ȴ�ҳ��������

	//��д�˺�������е�½
	if(ie.document.getElementsByName("username")[0] != undefined && ie.document.getElementsByName("password")[0] != undefined) { 
		ie.document.getElementsByName("username")[0].value = my_usernames[i];
		WScript.sleep(500);//ͣ��һ���ӷ���۲�
		ie.document.getElementsByName("password")[0].value = my_passwords[i];
		WScript.sleep(500);
		ie.document.getElementById("j-login-submit").click();
		WScript.sleep(2000);
	}
	
	//�򿪸���ҳ��
	ie.Navigate("http://www.yourong.cn/member/home"); 
	while(ie.busy){WScript.sleep(2000);}
	
	//���ǩ����ť
	if(ie.document.getElementById("j-checkin-btn") != undefined) {
		ie.document.getElementById("j-checkin-btn").click();
		WScript.sleep(6000);
	}
	
	//�˳�����ҳ��
	ie.Navigate("http://www.yourong.cn/member/logout"); 
	while(ie.busy){WScript.sleep(2000);}
}

ie.quit()