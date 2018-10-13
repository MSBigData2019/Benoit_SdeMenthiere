package mapReduceFromScratch;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.util.concurrent.TimeUnit;

public class MASTER {
	public static void main(String[] args) throws IOException, InterruptedException {
		// TODO Auto-generated method stub
		ProcessBuilder pb = new ProcessBuilder("ssh","bsarrauste@c45-24", "java", "-jar", "/tmp/bsarrauste/slave.jar");
		//pb.inheritIO();
		Process p = pb.start();
		InputStream is = p.getInputStream();
		BufferedInputStream bis = new BufferedInputStream(is);
		InputStreamReader isr = new InputStreamReader(bis);
		BufferedReader br = new BufferedReader(isr);
		String line = null;
		boolean b = p.waitFor(10, TimeUnit.SECONDS);
		//System.out.println(b);
		if (b!=false) {
		while ((line = br.readLine()) != null) {
            System.out.println(line);
            
		}
		
		//if (b) {
		
        //    }
		}else {
			System.out.println("Timeout");
			//p.destroy();
		}
//		String line2 = null;
//		while ((line2 = br2.readLine()) != null) {
//            System.out.println(line2);
//	
//		}
		}
	

}
