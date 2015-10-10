package autologin;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.CookieStore;
import org.apache.http.client.ResponseHandler;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.BasicResponseHandler;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.protocol.HTTP;

public class Login {

	private HttpResponse response = null;
	private DefaultHttpClient httpclient = null;

	private boolean login() throws ClientProtocolException, IOException {
		
		DefaultHttpClient httpclient = new DefaultHttpClient();

		HttpPost httpost = new HttpPost("http://www.baidu.com");

		httpost.setHeader("Accept", "*/*");
		httpost.setHeader("Accept-Language", "gzip, deflate");
		httpost.setHeader("Accept-Language", "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3");
		httpost.setHeader("Cache-Control", "no-cache");
		httpost.setHeader("Connection", "keep-alive");
		// httpost.setHeader("Content-Length", "106");
		httpost.setHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
		httpost.setHeader("Host", "www.yourong.cn");
		httpost.setHeader("Pragma", "no-cache");
		httpost.setHeader("Referer", "http://www.yourong.cn/security/login");
		httpost.setHeader("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0");
		httpost.setHeader("X-Requested-With", "XMLHttpRequest");

		HttpResponse response = httpclient.execute(httpost);
		System.out.println(response.toString());
		System.out.println(response.getStatusLine().getStatusCode());
		
		CookieStore cookiestore = httpclient.getCookieStore();
		System.out.println(cookiestore.toString());

		httpclient.close();
		/****************************************************************************************/
		
		DefaultHttpClient httpclient2 = new DefaultHttpClient();
		httpclient2.setCookieStore(cookiestore);

		HttpPost httpost2 = new HttpPost("http://www.yourong.cn/security/logined");

		httpost2.setHeader("Accept", "*/*");
		httpost2.setHeader("Accept-Language", "gzip, deflate");
		httpost2.setHeader("Accept-Language", "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3");
		httpost2.setHeader("Cache-Control", "no-cache");
		httpost2.setHeader("Connection", "keep-alive");
		// httpost.setHeader("Content-Length", "106");
		httpost2.setHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
		httpost2.setHeader("Host", "www.yourong.cn");
		httpost2.setHeader("Pragma", "no-cache");
		httpost2.setHeader("Referer", "http://www.yourong.cn/security/login");
		httpost2.setHeader("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0");
		httpost2.setHeader("X-Requested-With", "XMLHttpRequest");

		List<NameValuePair> nvps = new ArrayList<NameValuePair>();
		nvps.add(new BasicNameValuePair("loginSource", "0"));
		nvps.add(new BasicNameValuePair("pngCode", ""));
		nvps.add(new BasicNameValuePair("xToken", "cc17f304-da92-493e-8bc2-9c1488f09bf8"));
		nvps.add(new BasicNameValuePair("username", "zhangchaolts"));
		nvps.add(new BasicNameValuePair("password", "csujk4236238"));
		httpost2.setEntity(new UrlEncodedFormEntity(nvps, HTTP.UTF_8));
		
		HttpResponse response2 = httpclient2.execute(httpost2);
		System.out.println(response2.toString());
		System.out.println(response2.getStatusLine().getStatusCode());

		// System.out.println(getText("http://www.yourong.cn/member/home"));

		return true;
	}

	private String getText(String redirectLocation) {
		HttpGet httpget = new HttpGet(redirectLocation);
		// Create a response handler
		ResponseHandler<String> responseHandler = new BasicResponseHandler();
		String responseBody = "";
		try {
			responseBody = httpclient.execute(httpget, responseHandler);
		} catch (Exception e) {
			e.printStackTrace();
			responseBody = null;
		} finally {
			httpget.abort();
			// httpclient.getConnectionManager().shutdown();
		}
		return responseBody;
	}

	public static void main(String[] args) throws ClientProtocolException, IOException {
		Login lw = new Login();
		lw.login();
	}
}
