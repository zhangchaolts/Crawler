#coding:utf-8
import sys
import urllib
import urllib2
import cookielib
import re
import time,datetime
import string

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

def remove_all_blank(html):
	html = html.replace('\n', '')
	html = html.replace('\r', '')
	html = html.replace('\t', '')
	html = html.replace(' ', '')
	return html

def judge_already_bid(html):
	is_already_bid = 'no'
	buf = html
	date_today = datetime.datetime.now().strftime("%Y-%m-%d")
	while buf.find('<divclass="tlpl25">') != -1:
		item_st_pos = buf.find('<divclass="tlpl25">')
		item_end_pos = buf.find('</em></td>')
		if item_st_pos == -1 or item_end_pos == -1:
			break
		item_html = buf[item_st_pos:item_end_pos]
		#print item_html
		if item_html.find(date_today) != -1 and item_html.find('投标冻结') != -1:
			is_already_bid = 'yes'
			break
		buf = buf[item_end_pos + len('</em></td>'):]
	return is_already_bid

def get_invest_days_id(html):
	id_7 = ''
	id_10 = ''
	id_15 = ''
	buf = html
	while buf.find('<atitle="') != -1:
		item_st_pos = buf.find('<atitle="')
		item_end_pos = buf.find('<divclass="product_btn">')
		if item_st_pos == -1 or item_end_pos == -1:
			break
		item_html = buf[item_st_pos:item_end_pos]
		#print '\n\n' + item_html

		if item_html.find('100起投') == -1:
			buf = buf[item_end_pos + len('<divclass="product_btn">'):]
			continue

		if item_html.find('新手专享') != -1:
			buf = buf[item_end_pos + len('<divclass="product_btn">'):]
			continue
		
		qixian = get_content_from_html('<iclass="f18">(.*?)</i>天', item_html)
		if qixian == '':
			buf = buf[item_end_pos + len('<divclass="product_btn">'):]
			continue
		#print 'qixian:' + qixian

		if qixian.find('7~') != 0 and qixian != '10' and qixian != '15':
			buf = buf[item_end_pos + len('<divclass="product_btn">'):]
			continue

		left_money = get_content_from_html('剩余可投：</span>(.*?)元', item_html)
		left_money = left_money.replace(',', '') 
		if string.atof(left_money) <= 100000.0:
			buf = buf[item_end_pos + len('<divclass="product_btn">'):]
			continue
		#print 'left_money:' + left_money

		id = get_content_from_html('href="/deal/(.*?)"target=', item_html)
		if id != '':
			if qixian.find('7~') != -1:
				id_7 = id
			if qixian == '10':
				id_10 = id	
			if qixian == '15':
				id_15 = id
			if qixian == '30':
				id_30 = id

		buf = buf[item_end_pos + len('<divclass="product_btn">'):]

	if id_7 != '':
		return (7, id_7)
	elif id_10 != '':
		return (10, id_10)
	elif id_15 != '':
		return (15, id_15)
	elif id_15 != '':
		return (30, id_30)

	return (0, '')
		

def bid(username, password, bid_days):

	# 获取Cookiejar对象（存在本机的cookie消息）
	cj = cookielib.CookieJar()
	# 自定义opener,并将opener跟CookieJar对象绑定
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), RedirectHandler)
	# 安装opener,此后调用urlopen()时都会使用安装过的opener对象
	urllib2.install_opener(opener)

	print "\n" + username + " start ..."

	# 登录
	login_url_0 = 'https://www.firstp2p.com/user/login'
	login_html_0 = urllib2.urlopen(login_url_0).read()

	token = get_content_from_html("name='token' value='(.*?)'", login_html_0)
	token_id = get_content_from_html("name='token_id' value='(.*?)'", login_html_0)

	#print 'token:' + token
	#print 'token_id:' + token_id

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
	login_response_1 = opener.open(login_request_1).read().decode('unicode_escape').encode('gb18030')
	#print login_response_1

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
		e.hdrs['LogId']
		#print e.hdrs['LogId']

	home_url = "http://www.firstp2p.com/account"
	home_request = urllib2.Request(home_url)
	home_html = opener.open(home_request).read().decode('utf8').encode('gb18030')
	home_html = remove_all_blank(home_html)
	#print home_html

	if home_html.find('退出') == -1:
		result = "登录失败！"
		print result
		return result

	# 检查今天是否已经投过标
	recode_url = 'http://www.firstp2p.com/account/money?p=1'
	recode_request = urllib2.Request(recode_url)
	recode_html = opener.open(recode_request).read().decode('utf8').encode('gb18030')
	recode_html = remove_all_blank(recode_html)
	is_already_bid = judge_already_bid(recode_html)
	print 'is_already_bid:' + is_already_bid
	if is_already_bid == 'yes':
		result = "今天已经投过标了！"
		print result
		return result

	# 检查红包
	hongbao = get_content_from_html("红包金额：</th><td>(.*?)&nbsp元", home_html)
	print 'hongbao:' + hongbao
	if string.atof(hongbao) < 1.50:
		result = "账户红包小于1.5元！"
		print result
		return result

	# 检查可用余额
	money = get_content_from_html('可用余额：</th><td><emclass="color-yellow1">(.*?)&nbsp</em>元', home_html)
	print 'money:' + money
	if string.atof(money) < 100.0:
		result = "可用余额小于100.0元！"
		print result
		return result

	# 获取可投标天数和id
	invest_url = "http://www.firstp2p.com/deals?p=1&cate=0"
	invest_request = urllib2.Request(invest_url)
	invest_html = opener.open(invest_request).read().decode('utf8').encode('gb18030')
	invest_html = remove_all_blank(invest_html)
	#print invest_html
	(invest_days, invest_id) = get_invest_days_id(invest_html)
	print 'invest_days:' + str(invest_days)
	print 'invest_id:' + invest_id
	if invest_days == 0 or invest_id == '' or (invest_days != 0 and invest_days > bid_days):
		result = "无可投标的！"
		print result
		return result

	bid_url_1 = "http://www.firstp2p.com/deal/bid/" + invest_id;
	bid_request_1 = urllib2.Request(bid_url_1)
	bid_html_1 = opener.open(bid_request_1).read().decode('utf8').encode('gb18030')

	token = get_content_from_html("name='token' value='(.*?)'", bid_html_1)
	token_id = get_content_from_html("name='token_id' value='(.*?)'", bid_html_1)
	coupon_id = get_content_from_html('name="coupon_id" value="(.*?)"', bid_html_1)

	#print 'token:' + token
	#print 'token_id:' + token_id  
	#print 'coupon_id:' + coupon_id

	bid_url_2 = "http://www.firstp2p.com/deal/dobid?id=" + invest_id + "&token_id=" + token_id + "&token=" + token + "&bid_money=10000.00&coupon_id=" + coupon_id +"&coupon_is_fixed=1"
	print bid_url_2

	bid_request_2 = urllib2.Request(bid_url_2)
	bid_response_2 = opener.open(bid_request_2).read().decode('unicode_escape').encode('gb18030')
	print bid_response_2
	bid_result = get_content_from_html('"info":"(.*?)"', bid_response_2)
	print bid_result
	return bid_result


if __name__ == '__main__':

	reload(sys)
	sys.setdefaultencoding("utf-8")

	print "\n【" + datetime.datetime.now().strftime("%Y-%m-%d") + "】"

	##for line in file("网信理财账号密码.txt".decode('utf-8').encode('gbk')):
	for line in file("网信理财账号密码.txt"):
		line = line.strip()
		parts = line.split(" ")
		if len(parts) == 2:
			result = bid(parts[0], parts[1], 7)
			print parts[0] + " : " + result
