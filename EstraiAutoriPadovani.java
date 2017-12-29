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

public class EstraiAutoriPadovani
{
  public static void main(String[] args)
  {
    //carico gli autori da PaperPadovani in un set
    //scorro AutoriDEI, se il loro ID è nel set
    //Salvo ID e autore in AutoriPadovani
    
    //String paperPadova = "PaperPadovani.txt";
    String paperPadova = "PaperPadovaniAmpi.txt";
    //String autoriDEI = "AutoriDEI.txt";
    String autoriDEI = "AutoriDEIampi.txt";
    //String output = "AutoriPadovani.txt";
    String output = "AutoriPadovaniAmpi.txt";
   
    //Carico gli id delle affiliation in una HashSet
    
    FileReader reader = null;
    Scanner sc = null;
    
    Set<String> setAutoriPadovani = new HashSet<String>();
    
    try {
      reader = new FileReader(paperPadova);
      sc = new Scanner(reader);
      Scanner parse = null;
      
      while (sc.hasNextLine()) {
        String paperLine = sc.nextLine();
        
        parse = new Scanner(paperLine); //estrae l'autore
        //System.out.println("Prossimo paperPadovano:|"+paperLine+"|");
        String paperID = parse.next();
        setAutoriPadovani.add(parse.next());
      }
      
      System.out.println("Ci sono "+setAutoriPadovani.size()+" PaperPadovani.");
      
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
    
    //da AutoriDEI estraggo AutoriPadovani, se hanno un pubblicato un PaperPadovano
    
    reader = null;
    sc = null;
    BufferedWriter writer = null;
    
    int i=1;  //riga analizzata
    int j=1;  //corrispondenze trovate
    
    
    try {
      reader = new FileReader(autoriDEI);
      sc = new Scanner(reader);
      writer = new BufferedWriter(new FileWriter(output));
      
      Scanner parse = null;
      while (sc.hasNextLine()) {
        String line = sc.nextLine();
        //System.out.println(line);
        
        //Estrae una riga, estrae l'ID autore (1^ colonna) e vede se è nel Set
        parse = new Scanner(line);
        String authorID = parse.next();
        
        //
        if(setAutoriPadovani.contains(authorID)) {
          System.out.println(j+"a istanza alla riga "+i+":\t"+line);
          //autoriTrovati.add(line);
          writer.write(line+"\r\n");
          j=j+1;
        }
        
        //System.out.println("Autore: "+authorID+"\tNome: "+parse.next());
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
