package mapReduceFromScratch;

import java.io.IOException;
import java.util.LinkedList;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Collections;

public class WordCount {
	public static ArrayList<String> readLines(String filename) {
		List<String> lines = null;
		try {
			lines = Files.readAllLines(Paths.get(filename), Charset.forName("UTF-8"));
		} catch (IOException e) {
			System.out.println("Erreur lors de la lecture de " + filename);
			System.exit(1);
		}
		return (ArrayList<String>) lines;
	}

	public static HashMap<String, Integer> count(ArrayList<String> text) {
		HashMap<String, Integer> res = new HashMap<>();
		for (String line : text) {
			String[] words = line.split(" ");
			for (String word : words) {
				if (!res.containsKey(word)) {
					res.put(word, 1);
				} else {
					res.put(word, res.get(word) + 1);
				}
			}
		}
		return res;
	}
	
	public static List<Entry<String, Integer>> hashByValueAndKey(HashMap<String, Integer> hm) {
        // creating list from hashmap elements
        List<Map.Entry<String, Integer>> li = new LinkedList<Map.Entry<String, Integer> >(hm.entrySet());
        // here we are sorting the list
        Collections.sort(li, new Comparator<Map.Entry<String, Integer>>() {
            public int compare(Map.Entry<String, Integer> o1, Map.Entry<String, Integer> o2) {
                int valueComparator = o1.getValue().compareTo(o2.getValue());
                int keyComparator = o1.getKey().compareTo(o2.getKey());
                if (valueComparator != 0) {
                    return -valueComparator;
                }
                return keyComparator;
            }
        });
        return li;
        }

	public static void main(String[] args) {
		long startTime = System.currentTimeMillis();
		// TODO Auto-generated method stub
		String filename = "/cal/homes/bsarrauste/workspace/mapReduce/forestier_mayotte.txt";
		ArrayList<String> text = readLines(filename);
		HashMap<String, Integer> map = count(text);
        List<Entry<String, Integer>> sorted = hashByValueAndKey(map);
		for (Entry<String, Integer> entry : sorted) {
			String key = entry.getKey();
			Integer value = entry.getValue();
			System.out.println(key + " : " + value);
		}
		long endTime   = System.currentTimeMillis();
		long totalTime = endTime - startTime;
		System.out.println("temps total : "+totalTime);
       
	}

}
