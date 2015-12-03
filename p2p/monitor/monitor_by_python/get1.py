#coding=gbk

import sys
import urllib
import urllib2
import cookielib
import re
import time,datetime

def check():

	# 获取Cookiejar对象（存在本机的cookie消息）
	cj = cookielib.CookieJar()
	# 自定义opener,并将opener跟CookieJar对象绑定
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	# 安装opener,此后调用urlopen()时都会使用安装过的opener对象
	urllib2.install_opener(opener)

	# Step1:登录
	listpage_url = "http://www.huirendai.com/invest/list"

	listpage_post_data = urllib.urlencode({}) 

	listpage_headers = {	"Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", \
							"Accept-Encoding" : "gzip, deflate, sdch", \
							"Accept-Language" : "zh-CN,zh;q=0.8", \
							"Cache-Control" : "max-age=0", \
							"Connection" : "keep-alive", \
							"Cookie" : "Hm_lvt_a6dce16fcb09032d6e3ecb74e997d718=1444701463,1444791748; _jzqx=1.1444701463.1447400984.5.jzqsr=huirendai%2Ecom|jzqct=/index%2Ephp.jzqsr=huirendai%2Ecom|jzqct=/index%2Ephp; _qzja=1.1924528070.1444701463461.1446815830738.1447400983862.1447401020033.1447401038745..0.0.216.20; _jzqa=1.2921265156550503000.1444701463.1446815831.1447400984.20; OZ_1U_1967=vid=v61c6517525585.0&ctime=1447728986&ltime=1447728985; HRD_HYM=WzE0NDg1NTM1OTksWzAsMCw0LDBdXQ%3D%3D; __jsluid=f29860f962601653eb207efe43107a4b; PHPSESSID=nuoj9rrrblu8rk5bf9nk7jbga0; route=233c6d25a14f7f567a4f6cf56c069cbb; _gat=1; __jsl_clearance=1449061087.509|0|u6v7GmfHMcNn%2FYB6%2FukbRZ78iA4%3D; _ga=GA1.2.1387717844.1444701463; Hm_lvt_bceee2b1f1301c05c14cfe39f8a6f061=1448285373,1448535638,1448974596,1449023347; Hm_lpvt_bceee2b1f1301c05c14cfe39f8a6f061=1449061063; HRD=HRD_SESS_9c224e2c24fa7c03063a37ab4a1a2e0b", \
							"Host" : "www.huirendai.com", \
							"Referer" : "http://www.huirendai.com/invest/list", \
							"Upgrade-Insecure-Requests" : "1", \
							"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.69 Safari/537.36" \
						}

	listpage_request = urllib2.Request(listpage_url, headers=listpage_headers)

	listpage_response = opener.open(listpage_request).read().decode('utf8').encode('gb18030')
	
	print listpage_response


if __name__ == '__main__':

	reload(sys)
	sys.setdefaultencoding("gbk")

	check()


