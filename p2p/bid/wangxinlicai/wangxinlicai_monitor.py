#coding:utf-8
import sys
import urllib
import urllib2
import cookielib
import re
import time,datetime
import string
import os
import wangxinlicai_bid

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

		if hour < 9:
			break
		elif hour < 11:
			want_invest_days = 7
		elif hour < 14:
			want_invest_days = 10
		elif hour < 20:
			want_invest_days = 15
		#else:
		#	want_invest_days = 30
		print "want_invest_days:" + str(want_invest_days)

		can_invest_days = get_invest_days()
		print "can_invest_days:" + str(can_invest_days)

		is_all_finished = True

		if can_invest_days <= want_invest_days: 	
			for line in file("��������˺�����.txt"):
				line = line.strip()
				parts = line.split(" ")
				if len(parts) == 2:
					result = wangxinlicai_bid.bid(parts[0], parts[1], want_invest_days, 'no')
					if result != "�����Ѿ�Ͷ�����ˣ�" and result != "Ͷ�ʳɹ�":
						is_all_finished = False

		if is_all_finished == True:
			break

		if hour >= 20 and is_all_finished == False:
			mail_title = 'firstp2p is not all finished'
			mail_content = ''
			mail_box = '82213802@qq.com'
			os.system('echo ' + mail_content + ' | mail -s "' + mail_title + '" ' + mail_box)
			break

		time.sleep(300)


