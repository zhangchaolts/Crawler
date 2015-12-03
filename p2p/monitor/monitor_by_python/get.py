import requests


url = r'http://www.huirendai.com/invest/index.html'
url = r'http://www.huirendai.com/invest/list?mc=&tl=&rs=&page=2'

headers = {	"Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", \
			"Accept-Encoding" : "gzip, deflate, sdch", \
			"Accept-Language" : "zh-CN,zh;q=0.8", \
			#"Cache-Control" : "max-age=0", \
			"Connection" : "keep-alive", \
			"Cookie" : "__jsluid=f29860f962601653eb207efe43107a4b; PHPSESSID=nuoj9rrrblu8rk5bf9nk7jbga0; route=233c6d25a14f7f567a4f6cf56c069cbb; __jsl_clearance=1449061087.509|0|u6v7GmfHMcNn%2FYB6%2FukbRZ78iA4%3D; HRD=HRD_SESS_9c224e2c24fa7c03063a37ab4a1a2e0b", \
			"Host" : "www.huirendai.com", \
			#"Referer" : "http://www.huirendai.com/invest/list", \
			"Upgrade-Insecure-Requests" : "1", \
			"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.69 Safari/537.36" \
		}

html = requests.get(url, headers=headers).text
print(html.encode('gbk', 'ignore').decode('gbk'))

