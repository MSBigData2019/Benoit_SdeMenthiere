package mapReduceFromScratch;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

public class SLAVE {
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
	public static void map (String file) throws InterruptedException{
//		System.out.println("mode map");
		String filename = "/tmp/bsarrauste/splits/"+file;
		ArrayList<String> text = readLines(filename);
		ProcessBuilder pb = new ProcessBuilder("mkdir","/tmp/bsarrauste/maps/");
		//pb.inheritIO();
		try {
			Process p = pb.start();
			p.waitFor(3, TimeUnit.SECONDS);
			
		} catch(IOException e) {
			e.printStackTrace();
			System.out.println("already exist");	
		}
		String output = "";
		ArrayList<String> list = new ArrayList<>();
		for (String line : text) {
			for (String mot : line.split(" ")) {
				output += mot+" 1\n";
				if(!list.contains(mot)) {
					list.add(mot);
					System.out.println(mot);
					}
			}
		}
        final String chemin = "/tmp/bsarrauste/maps/UM"+file.charAt(1)+".txt";
//        System.out.println(chemin);
        final File fichier = new File(chemin); 
        try {
            // Creation du fichier
            fichier .createNewFile();
            // creation d'un writer (un écrivain)
            final FileWriter writer = new FileWriter(fichier);
            try {
                writer.write(output);
            } finally {
                // quoiqu'il arrive, on ferme le fichier
                writer.close();
            }
        } catch (Exception e) {
            System.out.println("Impossible de creer le fichier");
        }
	}
	public static void shuffle(String[] args) throws InterruptedException {
//		System.out.println("mode shuffle");
		String word = args[1];
		String outputFile = args[2];
		String output = "";
		for (int i = 3; i < args.length; i++) {
			ArrayList<String> file = readLines(args[i]);
			for (String line : file) {

				if ((word+" 1").equals(line)) {
					output+=line+"\n";
				}
			}
		}
//      System.out.println(chemin);
		final File fichier = new File(outputFile); 
		try {
          // Creation du fichier
          fichier .createNewFile();
          // creation d'un writer (un écrivain)
          final FileWriter writer = new FileWriter(fichier);
          try {
              writer.write(output);
          } finally {
              // quoiqu'il arrive, on ferme le fichier
              writer.close();
          }
      } catch (Exception e) {
          System.out.println("Impossible de creer le fichier");
      }
	}
	public static void reduce(String[] args) throws InterruptedException {
//		System.out.println("mode reduce");
		ProcessBuilder pb = new ProcessBuilder("mkdir","/tmp/bsarrauste/reduces/");
		//pb.inheritIO();
		try {
			Process p = pb.start();
			p.waitFor(3, TimeUnit.SECONDS);
			
		} catch(IOException e) {
			e.printStackTrace();
			System.out.println("already exist");	
		}
		String word = args[1];
		String inputFile = args[2];
		String outputFile = args[3];
		ArrayList<String> file = readLines(inputFile);
			
//      System.out.println(chemin);
		final File fichier = new File(outputFile); 
		try {
          // Creation du fichier
          fichier .createNewFile();
          // creation d'un writer (un écrivain)
          final FileWriter writer = new FileWriter(fichier);
          System.out.println(file.size());
          try {
              writer.write(word+" "+file.size());
          }
          catch (Exception ex){
              System.out.println("Impossible de d'ecrire"+ word+" "+file.size()+" dans le fichier");

          }finally {
          
              // quoiqu'il arrive, on ferme le fichier
              writer.close();
          }
		} catch (Exception e) {
          System.out.println("Impossible de creer le fichier");
          }
		}
	
	public static void main(String[] args) throws InterruptedException {
		String mode = args[0];
//		System.out.println(mode);
		if (mode.equals("0")) {
			String file = args[1];
			map(file);
	    }
		if (mode.equals("1")) {
			shuffle(args);
		}
		if (mode.equals("2")) {
			reduce(args);
		}
		
	}

}
