#coding=gbk

import sys
import urllib
import urllib2
import cookielib
import re
import time,datetime

def sign(username, password):

	# ��ȡCookiejar���󣨴��ڱ�����cookie��Ϣ��
	cj = cookielib.CookieJar()
	# �Զ���opener,����opener��CookieJar�����
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	# ��װopener,�˺����urlopen()ʱ����ʹ�ð�װ����opener����
	urllib2.install_opener(opener)

	# Step1:��ȡtoken
	token_url = 'http://www.yrw.com/security/login'
	token_html = urllib2.urlopen(token_url).read()

	xToken = ""
	token_anwser = re.search('name="xToken" value="(.*?)"', token_html)
	if token_anwser:
		xToken = token_anwser.group(1)
		#print xToken
	else:
		print "��ȡtokenʧ��!"
		return

	# Step2:��¼
	login_url = "https://www.yrw.com/security/logined"

	login_data = {	"xToken" : xToken, \
					"username": username, \
					"password": password, \
					"pngCode": "", \
					"loginSource": "0" \
				}

	login_post_data = urllib.urlencode(login_data) 

	login_headers = {	"Referer" : "https://www.yrw.com/security/login", \
						"Host" : "www.yrw.com", \
						"Accept" : "*/*", \
						"X-Requested-With" : "XMLHttpRequest", \
						"Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8", \
						"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.69 Safari/537.36" \
					}

	login_request = urllib2.Request(login_url, login_post_data, login_headers)

	login_response = opener.open(login_request).read().decode('utf8').encode('gbk')
	#print login_response
	
	if login_response.find('"success":true') == -1:
		print "��¼ʧ��!"
		return

	# Step3:ǩ��
	sign_url = "https://www.yrw.com/member/check/?_=" + str(int(time.mktime(datetime.datetime.now().timetuple()))) + "000"
	#print sign_url

	sign_request = urllib2.Request(sign_url)
	sign_response = opener.open(sign_request).read()
	#print sign_response

	#sign_response = '{"error":false,"page":null,"result":{"checkDate":1441268468855,"checkSource":0,"createTime":null,"gainPopularity":2,"id":null,"memberId":110850038887,"popularityDouble":1},"resultCode":null,"resultCodeEum":null,"resultCodeList":[],"resultList":null,"success":true}'

	gainPopularity = ""
	sign_anwser = re.search('"gainPopularity":(.*?),', sign_response)
	if sign_anwser:
		gainPopularity = sign_anwser.group(1)
		print username + "����ǩ���������ֵ:" + gainPopularity
	else:
		print username + "�����Ѿ�ǩ����!"


if __name__ == '__main__':

	reload(sys)
	sys.setdefaultencoding("gbk")

	username_array = ["zhangchaolts", "wangluyaolts", "zhangxmlts", "caixllts", "13240912500", "13240912700"]
	password_array = ["csujk4236238", "csujk4236238", "csujk4236238", "csujk4236238", "csujk4236238", "csujk4236238"]
	#username_array = ["zhangchaolts", "wangluyaolts"]
	#password_array = ["csujk4236238", "csujk4236238"]

	print "\n��" + datetime.datetime.now().strftime("%Y-%m-%d") + "��";

	for i in range(len(username_array)):
		sign(username_array[i], password_array[i])
