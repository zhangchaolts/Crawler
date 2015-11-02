#coding=gbk

import sys
import urllib
import urllib2
import cookielib
import re
import time,datetime


def sign(username, password):

	# 获取Cookiejar对象（存在本机的cookie消息）
	cj = cookielib.CookieJar()
	# 自定义opener,并将opener跟CookieJar对象绑定
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	# 安装opener,此后调用urlopen()时都会使用安装过的opener对象
	urllib2.install_opener(opener)

	# Step1:登录
	login_url = "http://huirendai.com/user/loginajaxex"

	login_data = {	"username": username, \
					"password": password, \
					"captcha": "", \
					"coop_id": "", \
					"coop_name": "", \
					"autologin": "0", \
					"logintype": "" \
				}

	login_post_data = urllib.urlencode(login_data) 

	login_headers = {	"Referer" : "http://huirendai.com/user/login", \
						"Host" : "huirendai.com", \
						"Accept" : "*/*", \
						"HTTPS:" : "1",
						"Origin" : "http://huirendai.com", \
						"Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8", \
						"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.69 Safari/537.36" \
					}

	login_request = urllib2.Request(login_url, login_post_data, login_headers)

	login_response = opener.open(login_request).read().decode('utf8').encode('gb18030')
	#print login_response
	
	if login_response.find('"m":"\u767b\u5f55\u6210\u529f"') == -1:
		print "登录失败!"
		return

	# Step2:签到
	sign_url = "http://www.huirendai.com/index.php?aj&q=user/sign"

	sign_headers = {	"Referer" : "http://www.huirendai.com/index.php?user", \
						"Host" : "www.huirendai.com", \
						"Accept" : "*/*", \
						"X-Requested-With" : "XMLHttpReques",
						"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.69 Safari/537.36" \
					}

	sign_request = urllib2.Request(sign_url, urllib.urlencode({}), sign_headers)
	sign_response = opener.open(sign_request).read().decode('utf8').encode('gb18030')
	#print sign_response

	#sign_response = '{"code":"00000","msg":"\u7b7e\u5230\u6210\u529f","data":{"TODAY_FLAG":"Y","SERIES_DAY":"39","NEXT_POINTS":0,"CURR_POINTS":"6","TODAY":16682}}'

	CURR_POINTS = ""
	sign_anwser = re.search('"CURR_POINTS":"(.*?)",', sign_response)
	if sign_anwser:
		CURR_POINTS = sign_anwser.group(1)
		print username + "今日签到获得惠米:" + CURR_POINTS
	else:
		print username + "今日已经签到过!"


if __name__ == '__main__':

	reload(sys)
	sys.setdefaultencoding("gbk")

	username_array = ["zhangchao822", "wangluyao1215", "zhangxm0713", "caixl0713"]
	password_array = ["csujk4236238", "csujk4236238", "csujk4236238", "csujk4236238"]
	#sername_array = ["zhangchao822", "wangluyao1215", "zhangxm0713"]
	#password_array = ["csujk4236238", "csujk4236238", "csujk4236238"]

	print "\n【" + datetime.datetime.now().strftime("%Y-%m-%d") + "】";

	for i in range(len(username_array)):
		sign(username_array[i], password_array[i])
