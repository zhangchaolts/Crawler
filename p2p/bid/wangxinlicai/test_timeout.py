#coding:utf-8
import sys
import urllib
import urllib2
import cookielib
import re
import time,datetime
import string


def get():

	# 获取Cookiejar对象（存在本机的cookie消息）
	cj = cookielib.CookieJar()
	# 自定义opener,并将opener跟CookieJar对象绑定
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	# 安装opener,此后调用urlopen()时都会使用安装过的opener对象
	urllib2.install_opener(opener)


	url='http://www.oalicai.com/'
	request = urllib2.Request(url)
	response = opener.open(request, timeout=1).read()
	print response



if __name__ == '__main__':

	reload(sys)
	sys.setdefaultencoding("utf-8")

	get()
