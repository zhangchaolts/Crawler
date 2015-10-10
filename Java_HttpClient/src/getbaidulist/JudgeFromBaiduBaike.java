package getbaidulist;

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

public class JudgeFromBaiduBaike {
	public static void main(String[] args) throws ClientProtocolException, IOException {

		String output = "D:\\workspace\\eclipse\\HttpClient\\getbaidulist\\output.txt";

		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(output)));

		HttpClient httpclient = new DefaultHttpClient();

		try {
			HttpGet httpgets = new HttpGet(
					"http://v.baidu.com/commonapi/movie2level/?callback=jQuery19105795006990551586_1397205062138&filter=true&type=%E5%96%9C%E5%89%A7&area=%E6%97%A5%E6%9C%AC&actor=&start=&complete=&order=hot&pn=1&rating=&prop=&_=1397205062139");
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
		} catch (Exception e) {
			e.printStackTrace();
		}
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