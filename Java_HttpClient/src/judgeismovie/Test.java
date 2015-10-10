package judgeismovie;

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
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;

public class Test {
	public static void main(String[] args) throws ClientProtocolException, IOException {


		HttpClient httpclient = new DefaultHttpClient();



				HttpGet httpgets = new HttpGet("http://baike.baidu.com/view/5267.htm");
				HttpResponse response = httpclient.execute(httpgets);
				HttpEntity entity = response.getEntity();
				if (entity != null) {
					// InputStream instreams = entity.getContent();
					// String str = convertStreamToString(instreams);//下面的方式不会中文乱码，这种方式会造成中文乱码
					String content = EntityUtils.toString(entity);

					content = new String(content.getBytes("ISO-8859-1"), "UTF-8");
					System.out.println(content);
				
				}
				
				httpgets.abort();
	
	}

}