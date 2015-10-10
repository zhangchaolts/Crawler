package autologin;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;

public class Login2 {
	public static void main(String[] args) throws ClientProtocolException, IOException {

		HttpClient httpclient = new DefaultHttpClient();

		HttpPost httppost = new HttpPost("http://mp4ba.com");
		HttpResponse response = httpclient.execute(httppost);
		
		
		httppost.setHeader("Accept", "*/*");
		httppost.setHeader("Accept-Language", "gzip, deflate");
		httppost.setHeader("Accept-Language", "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3");
		httppost.setHeader("Cache-Control", "no-cache");
		httppost.setHeader("Connection", "keep-alive");
		httppost.setHeader("Content-Length", "106");
		httppost.setHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
		//httppost.setHeader("Cookie", "JSESSIONID=93315D1F6A91E6ACFB63E19D8C751843; SERVERID=7e90e410064f8e1dc05d20265e3a7aca|1429005422|1429004377; CNZZDATA1253600367=1357798085-1429002339-%7C1429002339; _jzqa=1.1341881568729324500.1429004377.1429004377.1429004377.1; _jzqb=1.10.10.1429004377.1; _jzqc=1; _jzqckmp=1; _qzja=1.785256955.1429004377230.1429004377230.1429004377230.1429005398341.1429005402129.0.0.0.10.1; _qzjb=1.1429004377230.10.0.0.0; _qzjc=1; _qzjto=10.1.0");
		httppost.setHeader("Host", "www.yourong.cn");
		httppost.setHeader("Pragma", "no-cache");
		httppost.setHeader("Referer", "http://www.yourong.cn/security/login");
		httppost.setHeader("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0");
		httppost.setHeader("X-Requested-With", "XMLHttpRequest");
		
		
		HttpEntity entity = response.getEntity();
		if (entity != null) {
			//InputStream instreams = entity.getContent();
			//String str = convertStreamToString(instreams);//下面的方式不会中文乱码，这种方式会造成中文乱码
			String content = EntityUtils.toString(entity);
			content = new String(content.getBytes("ISO-8859-1"), "UTF-8");
			System.out.println(content);

		}
		httppost.abort();
	}

	public static String convertStreamToString(InputStream is) {
		BufferedReader reader = new BufferedReader(new InputStreamReader(is));
		StringBuilder sb = new StringBuilder();
		String line = null;
		try {
			while ((line = reader.readLine()) != null) {
				sb.append(line + "\n");
			}
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			try {
				is.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
		return sb.toString();
	}
}