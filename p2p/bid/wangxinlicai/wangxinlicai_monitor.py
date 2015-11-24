#coding:utf-8
import sys
import urllib
import urllib2
import cookielib
import re
import time,datetime
import string
import wangxinlicai_bid

'''
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

def get_type(html):
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

		if item_html.find('100��Ͷ') == -1:
			buf = buf[item_end_pos + len('<divclass="product_btn">'):]
			continue

		if item_html.find('����ר��') != -1:
			buf = buf[item_end_pos + len('<divclass="product_btn">'):]
			continue
		
		qixian = get_content_from_html('<iclass="f18">(.*?)</i>��', item_html)
		if qixian == '':
			buf = buf[item_end_pos + len('<divclass="product_btn">'):]
			continue
		#print 'qixian:' + qixian

		if qixian.find('7~') != 0 and qixian != '10' and qixian != '15':
			buf = buf[item_end_pos + len('<divclass="product_btn">'):]
			continue

		left_money = get_content_from_html('ʣ���Ͷ��</span>(.*?)Ԫ', item_html)
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

		buf = buf[item_end_pos + len('<divclass="product_btn">'):]

	if id_7 != '':
		#print id_7
		return '7'
	elif id_10 != '':
		#print id_10
		return '10'
	elif id_15 != '':
		#print id_15
		return '15'

	return ''
'''

def get_invest_days():

	# ��ȡCookiejar���󣨴��ڱ�����cookie��Ϣ��
	cj = cookielib.CookieJar()
	# �Զ���opener,����opener��CookieJar�����
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	# ��װopener,�˺����urlopen()ʱ����ʹ�ð�װ����opener����
	urllib2.install_opener(opener)

	# ��ȡ��Ͷ��id
	invest_url = "http://www.firstp2p.com/deals?p=1&cate=0"
	invest_request = urllib2.Request(invest_url)
	invest_html = opener.open(invest_request).read().decode('utf8').encode('gb18030')
	invest_html = wangxinlicai_bid.remove_all_blank(invest_html)
	#print invest_html

	return wangxinlicai_bid.get_invest_days_id(invest_html)[0]


if __name__ == '__main__':

	reload(sys)
	sys.setdefaultencoding("utf-8")

	while True:

		time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		hour = string.atoi(time_now.split(' ')[1].split(':')[0])
		print "hour:" + str(hour)
		
		want_invest_days = 7

		if hour < 10:
			break
		elif hour < 14:
			want_invest_days = 7
		elif hour < 18:
			want_invest_days = 10
		elif hour < 22:
			want_invest_days = 15
		else:
			want_invest_days = 30
		print "want_invest_days:" + str(want_invest_days)

		can_invest_days = get_invest_days()
		print "can_invest_days:" + str(can_invest_days)

		is_all_finished = True

		if can_invest_days <= want_invest_days: 	
			for line in file("��������˺�����.txt"):
				line = line.strip()
				parts = line.split(" ")
				if len(parts) == 2:
					result = wangxinlicai_bid.bid(parts[0], parts[1], want_invest_days)
					if result != "�����Ѿ�Ͷ�����ˣ�" and result != "Ͷ�ʳɹ�":
						is_all_finished = False

		if is_all_finished == True:
			break

		time.sleep(300)


