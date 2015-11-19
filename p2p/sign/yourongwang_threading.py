#coding:gbk
import sys
import urllib
import urllib2
import cookielib
import re
import time,datetime
import threading

class Yourongwang(threading.Thread):

	def __init__(self, username, password):
		threading.Thread.__init__(self)
		self.username = username
		self.password = password
		self.status = None
		self.cj = None
		self.opener = None

	def run(self):
		# 获取Cookiejar对象（存在本机的cookie消息）
		self.cj = cookielib.CookieJar()
		# 自定义opener,并将opener跟CookieJar对象绑定
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
		# 安装opener
		urllib2.install_opener(self.opener)

		# Step1:获取token
		token_url = 'http://www.yrw.com/security/login'
		token_request = urllib2.Request(token_url)
		token_html = self.opener.open(token_request).read()

		xToken = ""
		token_anwser = re.search('name="xToken" value="(.*?)"', token_html)
		if token_anwser:
			xToken = token_anwser.group(1)
			#print xToken
		else:
			result = "登录失败：获取token失败！"
			self.setStatus(result)
			return result

		# Step2:登录
		login_url = "https://www.yrw.com/security/logined"

		login_data = {	"xToken" : xToken, \
						"username": self.username, \
						"password": self.password, \
						"pngCode": "", \
						"loginSource": "0" \
					}
		#print login_data

		login_post_data = urllib.urlencode(login_data) 

		login_headers = {	"Referer" : "https://www.yrw.com/security/login", \
							"Host" : "www.yrw.com", \
							"Accept" : "*/*", \
							"X-Requested-With" : "XMLHttpRequest", \
							"Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8", \
							"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.69 Safari/537.36" \
						}

		login_request = urllib2.Request(login_url, login_post_data, login_headers)

		login_response = self.opener.open(login_request).read().decode('utf8').encode('gbk')
		#print login_response

		if login_response.find('"success":true') == -1:
			result = "登录失败！"
			self.setStatus(result)
			return result

		# Step3:签到
		sign_url = "https://www.yrw.com/member/check/?_=" + str(int(time.mktime(datetime.datetime.now().timetuple()))) + "000"
		#print sign_url
		sign_request = urllib2.Request(sign_url)
		sign_response = self.opener.open(sign_request).read()
		#print sign_response
		#sign_response = '{"error":false,"page":null,"result":{"checkDate":1441268468855,"checkSource":0,"createTime":null,"gainPopularity":2,"id":null,"memberId":110850038887,"popularityDouble":1},"resultCode":null,"resultCodeEum":null,"resultCodeList":[],"resultList":null,"success":true}'

		result1 = ""

		gainPopularity = ""
		sign_anwser = re.search('"gainPopularity":(.*?),', sign_response)
		if sign_anwser:
			gainPopularity = sign_anwser.group(1)
			result1 = "今日签到获得" + gainPopularity + "人气值。"
		else:
			result1 = "今日已经签到过！"

		# Step4：获取总人气值数据
		home_url = "https://www.yrw.com/member/home"
		home_request = urllib2.Request(home_url)
		home_html = self.opener.open(home_request).read()  #用多线程的话不要用urlopen()
		#print home_html

		result2 = ""

		totalPopularity = ""
		home_anwser = re.search('<dd><span class="f-ff-din"><a href="/coupon/reputation">(.*?)</a></span>', home_html)
		if home_anwser:
			totalPopularity = home_anwser.group(1)
			result2 = "总人气值为" + totalPopularity + "。"

		result = result1 + result2

		self.status = result


if __name__ == '__main__':

	reload(sys)
	sys.setdefaultencoding("gbk")

	print "\n【" + datetime.datetime.now().strftime("%Y-%m-%d") + "】";

	threads = []

	for line in file("有融网账号密码.txt"):
		line = line.strip()
		parts = line.split(" ")
		if len(parts) == 2:
			threads.append(Yourongwang(parts[0], parts[1]))

	for t in threads:
		t.start()

	for t in threads:
		t.join()

	for t in threads:
		print t.username + "\t" + t.status


