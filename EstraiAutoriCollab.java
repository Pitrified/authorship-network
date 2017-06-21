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

public class EstraiAutoriCollab
{
  public static void main(String[] args)
  {
    //carico gli autori da EdgeDEIPesati in un set
    //scorro AutoriDEI, se il loro ID è nel set
    //Salvo ID e autore in AutoriCollab
    
    String edgeCollab = "EdgeDEIPesati.txt";
    String autoriDEI = "AutoriDEI.txt";
    String output = "AutoriCollab.txt";
   
    //Carico gli id degli autori in una HashSet
    
    FileReader reader = null;
    Scanner sc = null;
    
    Set<String> SetAutoriCollab = new HashSet<String>();
    
    try {
      reader = new FileReader(edgeCollab);
      sc = new Scanner(reader);
      Scanner parse = null;
      
      while (sc.hasNextLine()) {
        String edgeLine = sc.nextLine();
        
        parse = new Scanner(edgeLine); //estrae l'autore
        //System.out.println("Prossimo edgeCollab:|"+edgeLine+"|"); 
        SetAutoriCollab.add(parse.next());      //ci sono due autori per edge
        SetAutoriCollab.add(parse.next());
      }
      
      System.out.println("Ci sono "+SetAutoriCollab.size()+" edgeCollab. (autori che hanno pubblicato insieme");
      
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
    
    //da AutoriDEI estraggo AutoriPadovani, se hanno un pubblicato un edgeCollab insieme
    
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
        if(SetAutoriCollab.contains(authorID)) {
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
