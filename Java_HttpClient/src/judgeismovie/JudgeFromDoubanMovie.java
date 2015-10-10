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

public class JudgeFromDoubanMovie {
	public static void main(String[] args) throws ClientProtocolException, IOException {

		String input = "D:\\workspace\\eclipse\\HttpClient\\data\\F.txt";
		String output = "D:\\workspace\\eclipse\\HttpClient\\data\\F_Rejudge.txt";

		BufferedReader br = new BufferedReader(new InputStreamReader(new FileInputStream(input)));

		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(output)));

		HttpClient httpclient = new DefaultHttpClient();

		ArrayList<String> errorLogList = new ArrayList<String>();

		int ptr = 0;
		String line = "";
		while ((line = br.readLine()) != null) {
			ptr++;
			if (ptr <= 280) {
				continue;
			}
			System.out.println(ptr);

			String[] terms = line.split("#\\&#");

			String title = java.net.URLEncoder.encode(terms[0], "utf-8");
			String exist = "F";

			try {
				HttpGet httpgets = new HttpGet("http://movie.douban.com/search/" + title);
				HttpResponse response = httpclient.execute(httpgets);
				HttpEntity entity = response.getEntity();
				if (entity != null) {
					String content = EntityUtils.toString(entity);
					// content = new String(content.getBytes("ISO-8859-1"), "UTF-8");
					// System.out.println(content);
					if (content.indexOf("alt=\"" + terms[0] + "\"") != -1) {
						exist = "T";
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