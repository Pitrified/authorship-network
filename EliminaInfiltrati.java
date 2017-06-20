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

public class EliminaInfiltrati
{
  public static void main(String[] args)
  {
    //nella lista di paper di autori del DEI e infiltrati
    //cerco l'affiliation (se c'è) nella lista di affiliation di padova
    //se c'è copio
    
    
    
    String affiliation = "PadovaPadua.txt";
    String paperList = "PaperAutAffDEI.txt";
    String output = "PaperRealiDEI.txt";
   
   
    //Carico gli id delle affiliation in una HashSet
    
    FileReader reader = null;
    Scanner sc = null;
    
    Set<String> setIDAffiliation = new HashSet<String>();
    
    try {
      reader = new FileReader(affiliation);
      sc = new Scanner(reader);
      Scanner parse = null;
      
      while (sc.hasNextLine()) {
        String affRecord = sc.nextLine();
        parse = new Scanner(affRecord); //estrae l'IDaffiliation
        System.out.println("Prossimo record ID affiliation:|"+affRecord+"|");
        //carico il nome nella tabella
        setIDAffiliation.add(parse.next());
      }
      
      System.out.println("Ci sono "+setIDAffiliation.size()+" affiliation a PadovaPadua.");
      
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
    
    
    //Da PaperAutAffDEI estraggo i paper del DEI (e non degli omonimi) (se c'è l'affiliation)
    
    
    reader = null;
    sc = null;
    //List<String> autoriTrovati = new LinkedList<String>();
    //File out = new File("output.txt");
    BufferedWriter writer = null;
    
    int i=1;  //riga analizzata
    int j=1;  //corrispondenze trovate
    
    
    try {
      reader = new FileReader(paperList);
      sc = new Scanner(reader);
      writer = new BufferedWriter(new FileWriter(output));
      
      Scanner parse = null;
      while (sc.hasNextLine()) {
        String line = sc.nextLine();
        //System.out.println(line);
        
        //Pigghia una riga, estrae l'ID affiliation (3^ colonna) e cerca contains
        parse = new Scanner(line);
        String paperID = parse.next();    //c'è sempre
        String authorID = parse.next();   //c'è sempre
        String affID = null;
        if(parse.hasNext()) {
          affID = parse.next();
        }
        
        //Se c'è copia il paper DEI reale
        if(affID != null && setIDAffiliation.contains(affID)) {
          System.out.println(j+"a istanza alla riga "+i+":\t"+line);
          //autoriTrovati.add(line);
          writer.write(line+"\r\n");
          j=j+1;
        }
        
        System.out.println("Paper: "+paperID+"\tAutore: "+authorID+"\tAffiliation: "+affID);
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