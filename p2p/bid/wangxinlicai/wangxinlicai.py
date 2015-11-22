#coding:utf-8
import sys
import urllib
import urllib2
import cookielib
import re
import time,datetime

class RedirectHandler(urllib2.HTTPRedirectHandler):
	def http_error_301(self, req, fp, code, msg, headers):
		pass
	def http_error_302(self, req, fp, code, msg, headers):
		pass

def get_content_from_html(regexp_str, html):
	content = ''
	anwser = re.search(regexp_str, html)
	if anwser:
		content = anwser.group(1)
	return content

def sign(username, password):

	# 获取Cookiejar对象（存在本机的cookie消息）
	cj = cookielib.CookieJar()
	# 自定义opener,并将opener跟CookieJar对象绑定
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), RedirectHandler)
	# 安装opener,此后调用urlopen()时都会使用安装过的opener对象
	urllib2.install_opener(opener)

	# Step1:获取token和token_id
	login_url = 'https://www.firstp2p.com/user/login'
	login_html = urllib2.urlopen(login_url).read()

	token = get_content_from_html("name='token' value='(.*?)'", login_html)
	token_id = get_content_from_html("name='token_id' value='(.*?)'", login_html)

	print token
	print token_id

	# Step2:登录
	login_url_1 = "https://www.firstp2p.com/user/LoginRestrict"

	login_data_1 = {	"username" : username, \
						"country_code" : "cn" \
					}

	login_post_data_1 = urllib.urlencode(login_data_1) 

	login_headers_1 = { "Accept" : "application/json, text/javascript, */*; q=0.01", \
						#"Accept-Encoding" : "gzip, deflate", \
						"Accept-Language" : "zh-CN,zh;q=0.8", \
						"Connection" : "keep-alive", \
						"Content-Length" : "36", \
						"Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8", \
						"Host" : "www.firstp2p.com", \
						"Origin" : "https://www.firstp2p.com", \
						"Referer" : "https://www.firstp2p.com/user/login", \
						"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.69 Safari/537.36", \
						"X-Requested-With" : "XMLHttpRequest" \
					}

	login_request_1 = urllib2.Request(login_url_1, login_post_data_1, login_headers_1)
	login_response_1 = opener.open(login_request_1).read().decode('utf8').encode('gb18030')
	print login_response_1


	login_url_2 = "https://www.firstp2p.com/user/doLogin"

	login_data_2 = {	'valid_phone' : '', \
						'token_id' : token_id, \
						'token' : token, \
						'country_code' : 'cn', \
						'username' : username, \
						'password' : password \
					}

	login_post_data_2 = urllib.urlencode(login_data_2) 
	
	login_headers_2 = { "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", \
						"Accept-Language" : "zh-CN,zh;q=0.8", \
						"Cache-Control " : "max-age=0", \
						"Connection" : "keep-alive", \
						"Content-Length" : "133", \
						"Content-Type" : "application/x-www-form-urlencoded", \
						"Host" : "www.firstp2p.com", \
						"Origin" : "https://www.firstp2p.com", \
						"Referer" : "https://www.firstp2p.com/user/login", \
						"Upgrade-Insecure-Requests" : "1", \
						"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.69 Safari/537.36" \
					}

	login_request_2 = urllib2.Request(login_url_2, login_post_data_2, login_headers_2)
	try:
		login_response_2 = opener.open(login_request_2).read().decode('utf8').encode('gb18030')
	except urllib2.URLError, e:
		print e.hdrs['LogId']

	home_url = "http://www.firstp2p.com/account"
	home_request = urllib2.Request(home_url)
	home_html = opener.open(home_request).read().decode('utf8').encode('gb18030')
	#print home_html

	if home_html.find('退出') == -1:
		result = "登录失败！"
		return

	print '登录成功'

	bid_url_1 = "http://www.firstp2p.com/deal/bid/70750";
	bid_request_1 = urllib2.Request(bid_url_1)
	bid_html_1 = opener.open(bid_request_1).read().decode('utf8').encode('gb18030')

	token = get_content_from_html("name='token' value='(.*?)'", bid_html_1)
	token_id = get_content_from_html("name='token_id' value='(.*?)'", bid_html_1)
	coupon_id = get_content_from_html('name="coupon_id" value="(.*?)"', bid_html_1)

	print token
	print token_id
	print coupon_id
	
	bid_url_2 = "http://www.firstp2p.com/deal/dobid?id=70750&token_id=" + token_id + "&token=" + token + "&bid_money=100.00&coupon_id=" + coupon_id +"&coupon_is_fixed=1"
	print bid_url_2

	bid_request_2 = urllib2.Request(bid_url_2)
	bid_response_2 = opener.open(bid_request_2).read().decode('utf8').encode('gb18030')
	print bid_response_2



if __name__ == '__main__':

	reload(sys)
	sys.setdefaultencoding("utf-8")

	print "\n【" + datetime.datetime.now().strftime("%Y-%m-%d") + "】";

	sign('18211085003', 'csujk4236238')

