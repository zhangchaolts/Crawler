#coding=gbk

import sys
import urllib
import urllib2
import cookielib
import re
import time,datetime

FW = open("log/minxindai_" + datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S") +  ".txt", "w")

def sign(username, password):

	# ��ȡCookiejar���󣨴��ڱ�����cookie��Ϣ��
	cj = cookielib.CookieJar()
	# �Զ���opener,����opener��CookieJar�����
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	# ��װopener,�˺����urlopen()ʱ����ʹ�ð�װ����opener����
	urllib2.install_opener(opener)

	# Step1:��¼
	login_url = "http://www.minxindai.com/?m=user&c=login&a=ulogin"

	login_data = {	"nickName": username, \
					"password": password, \
					"verifycode": "", \
					"chkboxautologin": "false" \
				}

	login_post_data = urllib.urlencode(login_data) 

	login_headers = {	"Referer" : "http://www.minxindai.com/?m=user&c=login", \
						"Host" : "www.minxindai.com", \
						"Accept" : "*/*", \
						"Origin" : "http://www.minxindai.com", \
						"Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8", \
						"X-Requested-With" : "XMLHttpRequest", \
						"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.69 Safari/537.36" \
					}

	login_request = urllib2.Request(login_url, login_post_data, login_headers)

	login_response = opener.open(login_request).read().decode('utf8').encode('gb18030')
	#print login_response
	#if login_response != "0":
	#	print "��¼ʧ��!"
	#	return

	homepage_url = "http://www.minxindai.com/?m=center";
	homepage_html = urllib2.urlopen(homepage_url).read().decode('utf8').encode('gb18030')
	#print homepage_html

	if homepage_html.find('�˳�') == -1:
		print "��¼ʧ��!"
		return

	# Step2:ǩ��
	sign_url = "http://www.minxindai.com/?c=sign"

	sign_headers = {	"Referer" : "http://www.minxindai.com/?m=event&c=jfturntab", \
						"Host" : "www.minxindai.com", \
						"Accept" : "*/*", \
						"Origin" : "http://www.minxindai.com", \
						"X-Requested-With" : "XMLHttpReques",
						"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.69 Safari/537.36" \
					}

	sign_request = urllib2.Request(sign_url, urllib.urlencode({}), sign_headers)
	sign_response = opener.open(sign_request).read().decode('unicode_escape').encode('gb18030')
	#print sign_response

	jifen = ""
	sign_anwser = re.search('���\<i\>(.*?)\<', sign_response)
	if sign_anwser:
		jifen = sign_anwser.group(1)
		print username + "����ǩ����û���:" + jifen
		FW.write(username + "����ǩ����û���:" + jifen + "\n")
	else:
		print username + "�����Ѿ�ǩ����!"
		FW.write(username + "�����Ѿ�ǩ����!" + "\n")

	# Step3:�齱
	lottery_url = "http://www.minxindai.com/?m=event&c=jfturntab&a=islottery"

	lottery_headers = {	"Accept" : "*/*", \
						"Host" : "www.minxindai.com", \
						"Origin" : "http://www.minxindai.com", \
						"Referer" : "http://www.minxindai.com/?m=event&c=jfturntab", \
						"X-Requested-With" : "XMLHttpReques", \
						"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.69 Safari/537.36", \
						"X-Requested-With" : "XMLHttpRequest" \
					}

	lottery_request = urllib2.Request(lottery_url, urllib.urlencode({}), lottery_headers)
	lottery_response = opener.open(lottery_request).read().decode('unicode_escape').encode('gb18030')
	print lottery_response
	FW.write(lottery_response + "\n")

	ptr = 0
	while lottery_response.find("���Ļ��ֲ���") == -1 and lottery_response.find("����ĳ齱����������") == -1 and ptr < 10:
		ptr += 1
		lottery_request = urllib2.Request(lottery_url, urllib.urlencode({}), lottery_headers)
		lottery_response = opener.open(lottery_request).read().decode('unicode_escape').encode('gb18030')
		print lottery_response
		FW.write(lottery_response + "\n")

	print
	FW.write("\n")


if __name__ == '__main__':

	reload(sys)
	sys.setdefaultencoding("gbk")

	username_array = ["18211085003", "15646563977", "13158424485", "13158422410", "13240912500", "13240912700"]
	password_array = ["csujk4236238", "csujk4236238", "csujk4236238", "csujk4236238", "csujk4236238", "csujk4236238"]
	#username_array = ["13158422410"]
	#password_array = ["csujk4236238"]

	print "\n��" + datetime.datetime.now().strftime("%Y-%m-%d") + "��";
 
	for i in range(len(username_array)):
		sign(username_array[i], password_array[i])

	FW.close()
