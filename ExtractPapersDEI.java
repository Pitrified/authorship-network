//Da fare:




//import java.util.Scanner;
//import java.io.FileReader;
//import java.io.FileNotFoundException;
//import java.io.IOException;
//package org.apache.commons.io;
import java.lang.*;
import java.io.*;
import java.util.*;

//import org.apache.commons.io.*;

public class ExtractPapersDEI
{
  public static void main(String[] args)
  {
    
    String idAutori = "AutoriDEI.txt";
    String papersFile = "PaperAuthorAffiliations10.txt";
    String output = "PaperAutAffDEI2.txt";
    
    //Carico gli id in una HashSet
    
    FileReader reader = null;
    Scanner sc = null;
    
    Set<String> setID = new HashSet<String>();
    
    try {
      reader = new FileReader(idAutori);
      sc = new Scanner(reader);
      Scanner parse = null;
      
      while (sc.hasNextLine()) {
        String autoreDEI = sc.nextLine();
        parse = new Scanner(autoreDEI);
        //System.out.println("Prossimo ID + autore DEI:|"+autoreDEI+"|");
        //carico il nome nella tabella
        setID.add(parse.next());
      }
      
      System.out.println("Ci sono "+setID.size()+" autori al DEI. Alcuni sono infiltrati.");
      
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
    
    
    //Da PaperAuthorAffiliation estraggo i paper del DEI (e degli omonimi)
    
    
    reader = null;
    sc = null;
    //List<String> autoriTrovati = new LinkedList<String>();
    //File out = new File("output.txt");
    BufferedWriter writer = null;
    
    int i=1;
    int j=1;
    
    
    try {
      reader = new FileReader(papersFile);
      sc = new Scanner(reader);
      writer = new BufferedWriter(new FileWriter(output));
      
      Scanner parse = null;
      while (sc.hasNextLine()) {
        String line = sc.nextLine();
        //System.out.println(line);
        
        //Pigghia una riga, estrae l'ID autore (2^ colonna) e cerca contains
        parse = new Scanner(line);
        String paperID = parse.next();
        String authorID = parse.next();
        //while(parse.hasNext()) {
        //  nome = nome.concat(" "+parse.next());
        //}
        
        //Se c'è scribacchia in un file ID autore
        if(setID.contains(authorID)) {
          System.out.println(j+"a istanza alla riga "+i+":\t"+line);
          //autoriTrovati.add(line);
          writer.write(line+"\r\n");
          j=j+1;
        }
        
        //System.out.println("ID: "+ID+"\tNome:|"+nome+"|\t\t\tautore DEI? "+setDEI.contains(nome));
        i=i+1;
      }
      
      //writeLines(out, autoriTrovati);
      //System.out.println(autoriTrovati);
      
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
    
    
    //lo ordino per paper
    
    //qualcun altro farà un check di chi sono le affiliation
    
    //System.out.println("Ciao, Mondo di Java!");
  }
}