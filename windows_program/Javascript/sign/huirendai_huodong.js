var my_usernames = [ "zhangxm0713", "caixl0713"];
var my_passwords = ["123456q", "123456q"];

var ie=WScript.createobject("InternetExplorer.Application"); 
ie.Visible=true;//����ie����ɼ�

for(var i = 0; i < my_usernames.length ; i++) {

	//�򿪻��˴���½ҳ��
	ie.Navigate("http://www.huirendai.com/index.php?user&q=action/login");
	while(ie.busy){WScript.sleep(2000);}//�ȴ�ҳ��������
	
	//��д�˺�������е�½
	if(ie.document.getElementById("keywords") != undefined && ie.document.getElementById("password") != undefined) { 
		ie.document.getElementById("keywords").value = my_usernames[i];
		WScript.sleep(500);//ͣ��һ���ӷ���۲�
		ie.document.getElementById("password").value = my_passwords[i];
		WScript.sleep(500);
		ie.document.getElementById("btnSubmit").click();
		WScript.sleep(2000);
	}
	
	//�򿪻ҳ��
	ie.Navigate("http://www.huirendai.com/index.php?activity&q=award"); 
	while(ie.busy){WScript.sleep(2000);}
	
	//����齱��ť
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
	
	//�˳�����ҳ��
	ie.Navigate("http://www.huirendai.com/?user&q=action/logout"); 
	while(ie.busy){WScript.sleep(2000);}
}

ie.quit()