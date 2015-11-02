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
	login_url = "http://www.huirendai.com/index.php?user&q=action/login"

	login_data = {	"keywords": username, \
					"password": password, \
					"valicode": "", \
					"logintype": "user" \
				}

	login_post_data = urllib.urlencode(login_data) 

	login_headers = {	"Referer" : "http://www.huirendai.com/index.php?user&q=action/login", \
						"Host" : "www.huirendai.com", \
						"Accept" : "*/*", \
						#"HTTPS:" : "1", \
						"Origin" : "http://www.huirendai.com", \
						"Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8", \
						"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.69 Safari/537.36" \
					}

	login_request = urllib2.Request(login_url, login_post_data, login_headers)

	login_response = opener.open(login_request).read().decode('utf8').encode('gb18030')
	#print login_response
	
	if login_response.find('您的账户总资产') == -1:
		print username + "登录失败!"
		return

	# Step2:签到
	sign_url = "http://www.huirendai.com/index.php?aj&q=user/sign"

	sign_headers = {	"Referer" : "http://www.huirendai.com/index.php?user", \
						"Host" : "www.huirendai.com", \
						"Accept" : "*/*", \
						"X-Requested-With" : "XMLHttpReques", \
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

	timestamp_now_date = time.mktime(datetime.datetime.now().timetuple())
	timestamp_expired_date = time.mktime(datetime.datetime.strptime("2015-12-01 00:00:00", '%Y-%m-%d %H:%M:%S').timetuple())
	if timestamp_now_date >= timestamp_expired_date:
		print "程序过期，请去群共享中下载最新版本。"
		time.sleep(3)
		sys.exit(0)

	username_array = []
	password_array = []

	for line in file("惠人贷账号密码.txt"):
		line = line.strip()
		parts = line.split(" ")
		if len(parts) == 2:
			username_array.append(parts[0])
			password_array.append(parts[1])	

	for i in range(len(username_array)):
		sign(username_array[i], password_array[i])

	print "\n执行结束，窗口即将关闭！"
	time.sleep(2)
