package other;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.ArrayList;

public class MergeFile {

	public static void main(String[] args) throws Exception {

		String input1 = "D:\\workspace\\eclipse\\HttpClient\\data\\output_filmname_fullnamelength_searchnumber.txt";
		String input2 = "D:\\workspace\\eclipse\\HttpClient\\data\\output_filmname_fullnamelength_exsit.txt";
		String output = "D:\\workspace\\eclipse\\HttpClient\\data\\output_filmname_fullnamelength_searchnumber_exsit.txt";

		BufferedReader br1 = new BufferedReader(new InputStreamReader(new FileInputStream(input1)));
		BufferedReader br2 = new BufferedReader(new InputStreamReader(new FileInputStream(input2)));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(output)));

		ArrayList<String> numberList = new ArrayList<String>();

		int ptr = 0;
		String line = "";
		while ((line = br1.readLine()) != null) {
//			ptr++;
//			if (ptr > 10000) {
//				break;
//			}
			numberList.add(line.split("#\\&#")[2]);
		}

		ptr = 0;
		while ((line = br2.readLine()) != null) {
			ptr++;
//			if (ptr > 10000) {
//				break;
//			}
			bw.write(line + "#&#" + numberList.get(ptr - 1) + "\n");
		}

		br1.close();
		br2.close();
		bw.close();
	}
}
