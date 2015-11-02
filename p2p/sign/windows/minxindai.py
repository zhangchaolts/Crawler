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
	#	print "登录失败!"
	#	return

	homepage_url = "http://www.minxindai.com/?m=center";
	homepage_html = urllib2.urlopen(homepage_url).read().decode('utf8').encode('gb18030')
	#print homepage_html

	if homepage_html.find('退出') == -1:
		print username + "登录失败!"
		return

	# Step2:签到
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
	sign_anwser = re.search('获得\<i\>(.*?)\<', sign_response)
	if sign_anwser:
		jifen = sign_anwser.group(1)
		print username + "今日签到获得积分:" + jifen
	else:
		print username + "今日已经签到过!"

	# Step3:抽奖
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

	ptr = 0
	while lottery_response.find("您的积分不足") == -1 and lottery_response.find("今天的抽奖次数已用完") == -1 and ptr < 10:
		ptr += 1
		lottery_request = urllib2.Request(lottery_url, urllib.urlencode({}), lottery_headers)
		lottery_response = opener.open(lottery_request).read().decode('unicode_escape').encode('gb18030')
		print lottery_response

	print


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
    
	for line in file("民信贷账号密码.txt"):
		line = line.strip()
		parts = line.split(" ")
		if len(parts) == 2:
			username_array.append(parts[0])
			password_array.append(parts[1])
            
	for i in range(len(username_array)):
		sign(username_array[i], password_array[i])
        
	print "\n执行结束，窗口即将关闭！"
	time.sleep(2)

