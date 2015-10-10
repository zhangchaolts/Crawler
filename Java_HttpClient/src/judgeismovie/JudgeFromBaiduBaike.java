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

public class JudgeFromBaiduBaike {
	public static void main(String[] args) throws ClientProtocolException, IOException {

		String input = "D:\\workspace\\eclipse\\HttpClient\\data\\output_filmname_fullnamelength.txt";
		String output = "D:\\workspace\\eclipse\\HttpClient\\data\\output_filmname_fullnamelength_exsit.txt";

		BufferedReader br = new BufferedReader(new InputStreamReader(new FileInputStream(input)));

		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(output)));

		HttpClient httpclient = new DefaultHttpClient();

		String[] keywords = { "电影", "影片", "剧情", "导演", "演员", "主演", "上映" };
		ArrayList<String> errorLogList = new ArrayList<String>();

		int ptr = 0;
		String line = "";
		while ((line = br.readLine()) != null) {
			ptr++;
			if (ptr <= 17365) {
				continue;
			}
			System.out.println(ptr);

			String[] terms = line.split("#\\&#");

			String title = java.net.URLEncoder.encode(terms[0], "utf-8");// 将中文编码成url
			// System.out.println(title);
			String exist = "F";

			try {
				HttpGet httpgets = new HttpGet("http://baike.baidu.com/searchword/?word=" + title + "&pic=1&sug=1&oq="
						+ title);
				HttpResponse response = httpclient.execute(httpgets);
				HttpEntity entity = response.getEntity();
				if (entity != null) {
					// InputStream instreams = entity.getContent();
					// String str = convertStreamToString(instreams);//下面的方式不会中文乱码，这种方式会造成中文乱码
					String content = EntityUtils.toString(entity);

					content = new String(content.getBytes("ISO-8859-1"), "UTF-8");
					// System.out.println(content);
					if (content.indexOf("百度百科尚未收录词条") == -1) {
						exist = "E";
						for (int i = 0; i < keywords.length; i++) {
							if (content.indexOf(keywords[i]) != -1) {
								exist = "T";
								break;
							}
						}
					}
				}
				System.out.println(line + "#&#" + exist);
				bw.write(line + "#&#" + exist + "\n");
				httpgets.abort();
			} catch (Exception e) {
				bw.write(line + "#&#" + exist + "\n");
				System.out.println("crawl error:" + line);
				errorLogList.add(line);
			}
		}

		for (int i = 0; i < errorLogList.size(); i++) {
			System.out.println("crawl error " + i + ":" + errorLogList.get(i));
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