#coding=gbk

import sys
import urllib
import urllib2
import cookielib
import re
import time,datetime
import string   
import multiprocessing

def sign(queue, line_ptr, username, password):

	# 获取Cookiejar对象（存在本机的cookie消息）
	cj = cookielib.CookieJar()
	# 自定义opener,并将opener跟CookieJar对象绑定
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	# 安装opener,此后调用urlopen()时都会使用安装过的opener对象
	urllib2.install_opener(opener)

	print username + " start ..."

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
		result = "登录失败！"
		queue.put(str(line_ptr) + " " + result)
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

	result1 = ""

	jifen = ""
	sign_anwser = re.search('获得\<i\>(.*?)\<', sign_response)
	if sign_anwser:
		jifen = sign_anwser.group(1)
		result1 = "今日签到获得" + jifen + "积分。"
	else:
		result1 = "今日已经签到过!"


	result2 = ""
	home_url = "http://www.minxindai.com/?m=event&c=jfturntab"
	home_html = urllib2.urlopen(home_url).read()
	#print home_html

	result2 = ""

	totalPopularity = ""
	home_anwser = re.search('<span class="counts">(.*?)</span>', home_html)
	if home_anwser:
		totalPopularity = home_anwser.group(1)
		result2 = "总积分为" + totalPopularity + "。"

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

	result3 = "未抽中实物奖品。"

	ptr = 0
	while lottery_response.find("您的积分不足") == -1 and lottery_response.find("今天的抽奖次数已用完") == -1 and ptr < 10:
		ptr += 1
		lottery_request = urllib2.Request(lottery_url, urllib.urlencode({}), lottery_headers)
		lottery_response = opener.open(lottery_request).read().decode('unicode_escape').encode('gb18030')
		print lottery_response
		jp_anwser = re.search(',"name":"(.*?)"', lottery_response)
		if jp_anwser:
			jp = jp_anwser.group(1)
			if jp.find("谢谢参与") != -1 and jp.find("积分") != -1 and jp.find("加息券") != -1 and jp.find("现金券") != -1:
				result3 = "恭喜抽中" + jp + "！"

	result = result1 + result2 + result3
	print username + " " + result
	queue.put(str(line_ptr) + " " + result)
	return


def get_status_list(queue):
	status_list = [None] * queue.qsize()
	while queue.empty() != True:
		parts = queue.get().split(" ")
		if len(parts) == 2:
			ptr = string.atoi(parts[0])
			status_list[ptr] = parts[1]
	return status_list
    
        
def sign_all(account_list):
	queue = multiprocessing.Queue()
	jobs = []
	for i in xrange(len(account_list)):
		job = multiprocessing.Process(target=sign, args=(queue, i, account_list[i][0], account_list[i][1]))
		jobs.append(job)
		job.start()
	for job in jobs:
		job.join()
	return get_status_list(queue)


if __name__ == '__main__':

	reload(sys)
	sys.setdefaultencoding("gbk")
    
	print "\n【" + datetime.datetime.now().strftime("%Y-%m-%d") + "】";
        
	account_list = []
	for line in file("民信贷账号密码.txt"):
		line = line.strip()
		parts = line.split(" ")
		if len(parts) == 2:
			account_list.append([parts[0], parts[1]])
    
	status_list = sign_all(account_list)
    
	for status in status_list:
		print status.encode('gbk')
