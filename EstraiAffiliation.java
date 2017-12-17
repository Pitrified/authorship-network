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

public class EstraiPaperDEI
{
  public static void main(String[] args)
  {
    //da PaperAutAffDEI estraggo le affiliation
    //se non c'è l'ID dell'affiliation nel set, la aggiungo al file AffiliationPadovaPadua
    
    
    
    String PaperAutAffDeiID = "PaprAutAffDEI.txt";
    String paperList = "Paprs.txt";
    String output = "PaprDEI.txt";
   
   
    //Carico gli id dei paper in una HashSet
    
    FileReader reader = null;
    Scanner sc = null;
    
    Set<String> setIDPaper = new HashSet<String>();
    
    try {
      reader = new FileReader(PaperAutAffDeiID);
      sc = new Scanner(reader);
      Scanner parse = null;
      
      while (sc.hasNextLine()) {
        String PaperAutAffRecord = sc.nextLine();
        parse = new Scanner(PaperAutAffRecord); //estrae l'IDpaper
        //System.out.println("Prossimo record:|"+PaperAutAffRecord+"|");
        //carico l'ID del paper nella tabella
        setIDPaper.add(parse.next());
      }
      
      System.out.println("Ci sono "+setIDPaper.size()+" paper in PaperAutAffDEI.");
      
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
    
    
    //Da Paper estraggo i paper scritti da un omonimo in AutoriDEI di una PersonaDEI
    
    
    reader = null;
    sc = null;
    //List<String> autoriTrovati = new LinkedList<String>();
    //File out = new File("output.txt");
    BufferedWriter writer = null;
    
    int i=1;  //riga analizzata
    int j=1;  //corrispondenze trovate
    
    
    try {
      //cerchiamo IN reader
      reader = new FileReader(paperList);
      sc = new Scanner(reader);
      writer = new BufferedWriter(new FileWriter(output));
      
      Scanner parse = null;
      while (sc.hasNextLine()) {
        String line = sc.nextLine();
        //System.out.println(line);
        
        //Pigghia una riga, estrae l'ID paper (1^ colonna) e cerca contains
        parse = new Scanner(line);
        String paperID = parse.next();
        
        //Se c'è copia il paper DEI 
        if(paperID != null && setIDPaper.contains(paperID)) {
          if (i%1000000==0) {System.out.println(j+"a istanza alla riga "+i+":\t"+line);};
          //autoriTrovati.add(line);
          writer.write(line+"\r\n");
          j=j+1;
        }
        
        //System.out.println("Paper: "+paperID+"\tAutore: "+authorID+"\tAffiliation: "+affID);
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
    //*/
    //System.out.println("Ciao, Mondo di Java!");
  }
}