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

public class EliminaNonPadova
{
  public static void main(String[] args)
  {
    //nella lista di paper di autori del DEI e non DEI
    //cerco l'affiliation (se c'è) nella lista di affiliation di padova
    //se l'autore è davvero padovano, lo copio
    String CARTELLA = "Versione2\\";
    String affiliation = "PadovaPadua.txt";
    //String paperList = "PaperAutAffDEI.txt";
    String paperList = CARTELLA+"PapAutAffDEIampi.txt";
    //String output = "PaperPadovani.txt";
    String output = CARTELLA+"PaperPadovaniAmpi.txt";
   
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
    BufferedWriter writer = null;
    
    int i=1;  //riga analizzata
    int j=1;  //corrispondenze trovate
    
    
    try {
      System.out.println("Path: "+paperList);
      reader = new FileReader(paperList);
      sc = new Scanner(reader);
      writer = new BufferedWriter(new FileWriter(output));
      
      Scanner parse = null;
      while (sc.hasNextLine()) {
        String line = sc.nextLine();
        //System.out.println(line);
        
        //Estrae una riga, estrae l'ID affiliation (3^ colonna) e vede se è nel Set
        parse = new Scanner(line);
        String paperID = parse.next();    //c'è sempre
        String authorID = parse.next();   //c'è sempre
        String affID = null;
        if(parse.hasNext()) {
          affID = parse.next();
        }
        
        //Se c'è copia il paper autoctono
        if(affID != null && setIDAffiliation.contains(affID)) {
          System.out.println(j+"a istanza alla riga "+i+":\t"+line);
          //autoriTrovati.add(line);
          writer.write(line+"\r\n");
          j=j+1;
        }
        
        System.out.println("Paper: "+paperID+"\tAutore: "+authorID+"\tAffiliation: "+affID);
        i=i+1;
      }
      
      //writeLines(out, autoriTrovati);     //sarebbe bello se apache.io andasse
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
  }
}
