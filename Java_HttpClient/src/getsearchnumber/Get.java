package getsearchnumber;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;

public class Get {
	public static void main(String[] args) throws ClientProtocolException, IOException {

		String input = "D:\\workspace\\eclipse\\HttpClient\\data\\output_filmname_fullnamelength.txt";
		String output = "D:\\workspace\\eclipse\\HttpClient\\data\\output_filmname_fullnamelength_searchnumber.txt";

		BufferedReader br = new BufferedReader(new InputStreamReader(new FileInputStream(input)));

		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(output)));

		HttpClient httpclient = new DefaultHttpClient();

		int ptr = 0;

		String line = "";
		while ((line = br.readLine()) != null) {
			ptr++;
			if (ptr <= 35068) {
				continue;
			}
			System.out.println(ptr);

			String[] terms = line.split("#\\&#");

			String title = java.net.URLEncoder.encode(terms[0], "utf-8");// 将中文编码成url
			// System.out.println(title);

			try {
				HttpGet httpgets = new HttpGet("http://10.12.8.167/v?tn=0&st=1&forceQuery=on&debug=on&query=" + title);
				HttpResponse response = httpclient.execute(httpgets);
				HttpEntity entity = response.getEntity();

				if (entity != null) {
					// InputStream instreams = entity.getContent();
					// String str = convertStreamToString(instreams);//下面的方式不会中文乱码，这种方式会造成中文乱码
					String content = EntityUtils.toString(entity);

					// content = new String(content.getBytes("ISO-8859-1"), "UTF-8");
					// System.out.println(content);

					Pattern pattern = Pattern.compile("找到约 (.+) 个视频");
					Matcher matcher = pattern.matcher(content);
					while (matcher.find()) {
						String result = matcher.group(1);
						System.out.println(line + "#&#" + result);
						bw.write(line + "#&#" + result + "\n");
					}
				}
				httpgets.abort();
			} catch (Exception e) {
				bw.write(line + "#&#0\n");
				System.out.println("crawl error:" + line);
			}
		}
		br.close();
		bw.close();
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