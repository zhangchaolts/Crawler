#coding:utf-8
import sys
import urllib
import urllib2
import cookielib
import re
import time,datetime
import string


def get():

	# ��ȡCookiejar���󣨴��ڱ�����cookie��Ϣ��
	cj = cookielib.CookieJar()
	# �Զ���opener,����opener��CookieJar�����
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	# ��װopener,�˺����urlopen()ʱ����ʹ�ð�װ����opener����
	urllib2.install_opener(opener)


	url='http://www.oalicai.com/'
	request = urllib2.Request(url)
	response = opener.open(request, timeout=1).read()
	print response



if __name__ == '__main__':

	reload(sys)
	sys.setdefaultencoding("utf-8")

	get()
