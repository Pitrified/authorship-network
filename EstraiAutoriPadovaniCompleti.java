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

public class EstraiAutoriPadovaniCompleti
{
  public static void main(String[] args)
  {
    //filtro PaperAutAffDEI e tengo i paper scritti da autori che hanno almeno un paper con affiliation padovana
    //in PaperPadovaniCompleti alcuni paper non avranno affiliation
    
    //String autoriPadovani = "AutoriPadovani.txt";
    String autoriPadovani = "AutoriPadovaniAmpi.txt";
    //String paperAutAff = "PaperAutAffDEI.txt";
    String paperAutAff = "PapAutAffDEIampi.txt";
    //String output = "PaperPadovaniCompleti.txt";
    String output = "PaperPadovaniCompletiAmpi.txt";
   
    //Carico gli id autori in una HashSet
    
    FileReader reader = null;
    Scanner sc = null;
    
    Set<String> setAutoriPadovani = new HashSet<String>();
    
    try {
      reader = new FileReader(autoriPadovani);
      sc = new Scanner(reader);
      Scanner parse = null;
      
      while (sc.hasNextLine()) {
        String autore = sc.nextLine();
        
        parse = new Scanner(autore); //estrae l'ID autore
        //System.out.println("Prossimo paperPadovano:|"+paperLine+"|");
        //String autoreID = parse.next();
        setAutoriPadovani.add(parse.next());
      }
      
      System.out.println("Ci sono "+setAutoriPadovani.size()+" autori padovani.");
      
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
    
    //da PaperAutAffDEI estraggo PaperPadovaniCompleti, scritti tutti da autori padovani
    
    reader = null;
    sc = null;
    BufferedWriter writer = null;
    
    int i=1;  //riga analizzata
    int j=0;  //corrispondenze trovate
    
    
    try {
      reader = new FileReader(paperAutAff);
      sc = new Scanner(reader);
      writer = new BufferedWriter(new FileWriter(output));
      
      Scanner parse = null;
      while (sc.hasNextLine()) {
        String line = sc.nextLine();
        //System.out.println(line);
        
        //Estrae una riga, estrae l'ID autore (2^ colonna) e vede se è nel Set
        parse = new Scanner(line);
        String paperID = parse.next();
        String authorID = parse.next();
        
        //
        if(setAutoriPadovani.contains(authorID)) {
          //System.out.println(j+"a istanza alla riga "+i+":\t"+line);
          //autoriTrovati.add(line);
          writer.write(line+"\r\n");
          j=j+1;
        }
        
        //System.out.println("Autore: "+authorID+"\tNome: "+parse.next());
        i=i+1;
      }
      
      //writeLines(out, autoriTrovati);     //sarebbe bello se apache.io andasse
      System.out.println(setAutoriPadovani.size()+" hanno pubblicato "+j+" paper.");
      
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
  }
}
