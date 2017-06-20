//Da fare:
//try con resources
//parse.next() è pericoloso



//import java.util.Scanner;
//import java.io.FileReader;
//import java.io.FileNotFoundException;
//import java.io.IOException;
//package org.apache.commons.io;
import java.lang.*;
import java.io.*;
import java.util.*;

//import org.apache.commons.io.*;

public class ExtractAuthorsID
{
  public static void main(String[] args)
  {
    String inputAutoriDEI = "PersoneDei.txt";
    String listaAuthors = "Authors.txt";
    String output = "AutoriDEI.txt";
    
    
    //Apre File PersoneDei1 in modo normale che sono belli e ordinati
    //Crea HashSet
    FileReader reader = null;
    Scanner sc = null;
    
    Set<String> setDEI = new HashSet<String>();
    
    try {
      reader = new FileReader(inputAutoriDEI);
      sc = new Scanner(reader);
      
      while (sc.hasNextLine()) {
        String autoreDEI = sc.nextLine();
        //System.out.println("Prossimo autore DEI:|"+autoreDEI+"|");
        //carico il nome nella tabella
        setDEI.add(autoreDEI);
      }
      
      System.out.println("Ci sono "+setDEI.size()+" autori al DEI.");
      
    } catch(Exception e){
      System.err.println("Error: "+e.getMessage());
    } finally {
      if (reader != null) {
        try {
          reader.close();
        } catch(IOException ioe) {
          System.err.println("Error: "+ioe.getMessage());
        }
      }
      if (sc != null) {
        sc.close();
      }
    }    
    
    //Apre Author con buffer
    
    reader = null;
    sc = null;
    List<String> autoriTrovati = new LinkedList<String>();
    //File out = new File("output.txt");
    BufferedWriter writer = null;
    
    int i=1;
    int j=1;
    
    
    try {
      reader = new FileReader(listaAuthors);
      sc = new Scanner(reader);
      writer = new BufferedWriter(new FileWriter(output));
      
      Scanner parse = null;
      while (sc.hasNextLine()) {
        String line = sc.nextLine();
        //System.out.println(line);
        
        //Pigghia una riga, estrae il nome (2^ colonna) e cerca contains
        parse = new Scanner(line);
        String ID = parse.next();
        String nome = parse.next();
        while(parse.hasNext()) {
          nome = nome.concat(" "+parse.next());
        }
        
        //Se c'è scribacchia in un file ID autore
        if(setDEI.contains(nome)) {
          System.out.println(line+"\t\t"+j+"a istanza alla riga "+i);
          autoriTrovati.add(line);
          writer.write(line+"\r\n");
          j=j+1;
        }
        
        //System.out.println("ID: "+ID+"\tNome:|"+nome+"|\t\t\tautore DEI? "+setDEI.contains(nome));
        i=i+1;
      }
      
      //writeLines(out, autoriTrovati);
      System.out.println(autoriTrovati);
      
    } catch(Exception e){
      System.err.println("Error: "+e.getMessage());
    } finally {
      if (reader != null) {
        try {
          reader.close();
        } catch(IOException ioe) {
          System.err.println("Error: "+ioe.getMessage());
        }
      }
      if (writer != null) {
        try {
          writer.close();
        } catch(IOException ioe) {
          System.err.println("Error: "+ioe.getMessage());
        }
      }
      if (sc != null) {
        sc.close();
      }
    }    
    
    
    
    //System.out.println("Ciao, Mondo di Java!");
  }
}