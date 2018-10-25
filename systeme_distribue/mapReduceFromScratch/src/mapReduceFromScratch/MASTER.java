package mapReduceFromScratch;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Hashtable;
import java.util.List;
import java.util.concurrent.TimeUnit;

public class MASTER {
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

	public static void main(String[] args) throws IOException, InterruptedException {
		// TODO Auto-generated method stub
		String filename = "/home/b/git/systeme_distribue/mapReduceFromScratch/adress_ip.txt";
		ArrayList<String> text = readLines(filename);
		ArrayList<Process> liste = new ArrayList<>();
		//System.out.println(text);
		HashMap<String, ArrayList<String>> dic= new HashMap<>();
		int i = 0;
		for (String ip : text) {
			ProcessBuilder pb = new ProcessBuilder("ssh", "-o StrictHostKeyChecking=no","bsarrauste@"+ip, "mkdir","/tmp/bsarrauste/splits/");
			try {
				Process p = pb.start();
				boolean b = p.waitFor(3, TimeUnit.SECONDS);
				
			} catch(IOException e) {
				e.printStackTrace();
				System.out.println("already exist");	
			}
			ProcessBuilder spb = new ProcessBuilder("scp",
					"/home/b/git/systeme_distribue/mapReduceFromScratch/s"+i+".txt",
					"bsarrauste@"+ip+":/tmp/bsarrauste/splits");
//			System.out.println("copy s"+i+" on "+ip);
			spb.inheritIO();
			spb.start();
			//pb.inheritIO();
			Process p = pb.start();
			liste.add(p);
			//System.out.println(ip);
			ProcessBuilder pb_slave = new ProcessBuilder("ssh","-o StrictHostKeyChecking=no","bsarrauste@"+ip, "java", "-jar", "/tmp/bsarrauste/slave.jar","0","s"+i+".txt");
//			pb.inheritIO();
			Process p_slave = pb_slave.start();
			p.waitFor(10, TimeUnit.SECONDS);
			System.out.println("UM"+i+" - "+ip);
			i+=1;
			InputStream is = p_slave.getInputStream();
			BufferedInputStream bis = new BufferedInputStream(is);
			InputStreamReader isr = new InputStreamReader(bis);
			BufferedReader br = new BufferedReader(isr);
			String line = null;
			boolean b = p.waitFor(10, TimeUnit.SECONDS);
			//System.out.println(b);
			if (b!=false) {
			while ((line = br.readLine()) != null) {
	            //System.out.println(line);
	            ArrayList<String> value = dic.get(line);
	            if (value != null) {
	            	value.add("UM"+i);
	            	dic.put(line, value);
	            } else {
	            	ArrayList<String> init = new ArrayList<>();
	            	init.add("UM"+i);
//	            	value = value.add(init);
	            	dic.put(line, init);
	            }
	            
			}
			}
		}
		System.out.println(dic);
		
	}
//	public static void main(String[] args) throws IOException, InterruptedException {
//		// TODO Auto-generated method stub
//		ProcessBuilder pb = new ProcessBuilder("ssh","bsarrauste@c45-25", "java", "-jar", "/tmp/bsarrauste/slave.jar");
//		pb.inheritIO();
//		Process p = pb.start();
//		InputStream is = p.getInputStream();
//		BufferedInputStream bis = new BufferedInputStream(is);
//		InputStreamReader isr = new InputStreamReader(bis);
//		BufferedReader br = new BufferedReader(isr);
//		String line = null;
//		boolean b = p.waitFor(10, TimeUnit.SECONDS);
//		//System.out.println(b);
//		if (b!=false) {
//		while ((line = br.readLine()) != null) {
//            System.out.println(line);
//            
//		}
		
		//if (b) {
		
        //    }
//		}else {
//			System.out.println("Timeout");
			//p.destroy();
//		}
//		String line2 = null;
//		while ((line2 = br2.readLine()) != null) {
//            System.out.println(line2);
//	
//		}
//		}
	

}
	
