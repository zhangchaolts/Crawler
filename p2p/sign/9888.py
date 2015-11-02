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

	# Step1:获取token
	token_url = 'https://passport.9888.cn/passport/login'
	token_html = urllib2.urlopen(token_url).read()

	xToken = ""
	token_anwser = re.search('name="lt" value="(.*?)"', token_html)
	if token_anwser:
		xToken = token_anwser.group(1)
		#print xToken
	else:
		print "获取token失败!"
		return

	# Step2:登录
	login_url = "https://passport.9888.cn/passport/login"

	login_data = {	"username": username, \
					"password": password, \
					"lt": xToken, \
					"execution": "e1s1", \
					"_eventId": "submit" \
				}

	login_post_data = urllib.urlencode(login_data) 

	login_headers = {	#"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", \
						#"Accept-Encoding": "gzip, deflate", \
						"Accept-Language": "zh-CN,zh;q=0.8", \
						#"Cache-Control": "max-age=0", \
						#"Connection": "keep-alive", \
						#"Content-Length" : "117", \
						"X-Requested-With" : "XMLHttpRequest", \
						#"Content-Type" : "application/x-www-form-urlencoded", \
						"Host" : "passport.9888.cn", \
						#"Origin" : "https://passport.9888.cn", \
						"Referer" : "https://passport.9888.cn/passport/login", \
						"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.69 Safari/537.36" \
					}

	login_request = urllib2.Request(login_url, login_post_data, login_headers)

	login_response = opener.open(login_request).read()
	#print login_response
	if login_response.find("http://www.9888.cn?islogin=true&pc=1") == -1:
		print "登录失败!"
		return

	#非得打开这个网页才能正常签到
	homepage_url = "http://www.9888.cn/account/home.shtml";
	homepage_html = urllib2.urlopen(homepage_url).read().decode('utf8').encode('gb18030')
	#print homepage_html
	#if homepage_html.find('退出') == -1:
	#	print "登录失败!"
	#	return

	# Step3:签到
	sign_url = "http://www.9888.cn/account/signMethod.do?_" + str(int(time.mktime(datetime.datetime.now().timetuple()))) + "000"
	#print sign_url

	sign_request = urllib2.Request(sign_url)
	sign_response = opener.open(sign_request).read()
	print sign_response

	gainPopularity = ""
	sign_anwser = re.search('"returnAmount":(.*?),', sign_response)
	if sign_anwser:
		gainPopularity = sign_anwser.group(1)
		print username + "今日签到获得工豆:" + gainPopularity
	else:
		print username + "今日已经签到过!"


if __name__ == '__main__':

	reload(sys)
	sys.setdefaultencoding("gbk")

	username_array = ["18211085003", "15646563977", "13141330862", "13141330987", "13240912500", "13240912700"]
	password_array = ["csujk4236238", "csujk4236238", "csujk4236238", "csujk4236238", "csujk4236238", "csujk4236238"]
	#username_array = ["13158422410"]
	#password_array = ["csujk4236238"]

	print "\n【" + datetime.datetime.now().strftime("%Y-%m-%d") + "】";
 
	for i in range(len(username_array)):
		sign(username_array[i], password_array[i])
