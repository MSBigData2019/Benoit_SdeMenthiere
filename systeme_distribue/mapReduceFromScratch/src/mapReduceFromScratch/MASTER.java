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
		String filename = "/home/b/msbgd/git/systeme_distribue/mapReduceFromScratch/adress_ip.txt";
		ArrayList<String> text = readLines(filename);
		ArrayList<Process> liste = new ArrayList<>();
		//System.out.println(text);
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
					"/home/b/msbgd/git/systeme_distribue/mapReduceFromScratch/s"+i+".txt",
					"bsarrauste@"+ip+":/tmp/bsarrauste/splits");
			System.out.println("copy s"+i+" on "+ip);
			i+=1;
			spb.inheritIO();
			spb.start();
			//pb.inheritIO();
			Process p = pb.start();
			liste.add(p);
			//System.out.println(ip);
			}
		
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
