package mapReduceFromScratch;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

public class DEPLOY {
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
		String filename = "/home/benoit/eclipse-workspace/mapReduceFromScratch/adress_ip.txt";
		ArrayList<String> text = readLines(filename);
		ArrayList<Process> liste = new ArrayList<>();
		System.out.println(text);
		ArrayList<String> success_ip = new ArrayList<>();
		for (String ip : text) {
			ProcessBuilder pb = new ProcessBuilder("ssh", "bsarrauste@"+ip, "hostname");
			//pb.inheritIO();
			Process p = pb.start();
			liste.add(p);
			}
		for (Process p :liste) {
			InputStream is = p.getInputStream();
			InputStreamReader isr = new InputStreamReader(is);
			BufferedReader br = new BufferedReader(isr);
			String line = null;
			while ((line = br.readLine()) != null) {
	            System.out.println(line);
	            success_ip.add(line);
			}
		
		}
		System.out.println(success_ip);
		for (String ip : success_ip) {
			ProcessBuilder pb = new ProcessBuilder("ssh","bsarrauste@"+ip,"mkdir","/tmp/bsarrauste/");
			try {
				Process p = pb.start();
				boolean b = p.waitFor(3, TimeUnit.SECONDS);
				
			} catch(IOException e) {
				e.printStackTrace();
				System.out.println("already exist");	
			}
			
			ProcessBuilder spb = new ProcessBuilder("scp",
					"/home/benoit/eclipse-workspace/mapReduceFromScratch/slave.jar",
					"bsarrauste@"+ip+":/tmp/bsarrauste/");
			//pb.inheritIO();
			
			Process sp = spb.start();
				
			
			//pb.inheritIO();
			}

	}

}
