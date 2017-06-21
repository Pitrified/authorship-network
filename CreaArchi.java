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

public class CreaArchi
{
  public static void main(String[] args)
  {
    //da  (già ordinato per paper) !!!!!
    //paper1 autore1
    //paper1 autore2
    //paper1 autore3
    //paper2 autore1
    //paper2 autore2
    //a (arco in ordine lessicografico)
    //autore1 autore2
    //autore1 autore3
    //autore1 autore2    
    
    String input = "PaperAutAffDEIOrdinatiPAPER.txt";
    input  = "PaperPadovani.txt";
    input  = "PaperPadovaniCompleti.txt";
    //input  = "CreaArchiTest.txt";
    String output = "EdgeDEI1.txt";
    output = "EdgePadovani.txt";
    output = "EdgePadovaniCompleti.txt";
    //output = "CreaArchiOutput.txt";
   
    FileReader reader = null;
    Scanner sc = null;
    BufferedWriter writer = null;
    
    try {
      reader = new FileReader(input);
      sc = new Scanner(reader);
      writer = new BufferedWriter(new FileWriter(output));
      Scanner parse = null;
      Scanner newParse = null;
      String line = sc.nextLine();
      int i = 0;
      
      while (sc.hasNextLine()) {
        //estraggo gli autori che hanno lavorato ad un paper
        List<String> autori = new LinkedList<String>();   //lista di autori di thePaper
        parse = new Scanner(line);
        String thePaper = parse.next();       //paper che esaminiamo
        autori.add(parse.next());             //in autori ora c'è il primo autore
        String nextPaper = null;
        String newLine = null;
        do {
          newLine = sc.nextLine();            //la prossima riga forse non c'è solo la prima volta
          newParse = new Scanner(newLine);
          nextPaper = newParse.next();        //paper della prossima riga
          if(thePaper.equals(nextPaper)) {    //sono uguali?
            autori.add(newParse.next());      //aggiungo l'autore
          }
        } while(sc.hasNextLine() && thePaper.equals(nextPaper));  //se sono diversi o è finito il file esce
        line = newLine;                       //il prossimo ciclo questa sarà la line col paper
        //System.out.println("paper "+thePaper+" con autori "+autori+" sono in "+autori.size());
        
        //trasformo la lista di autori in archi
        if(autori.size()==1){i=i+1;}
        while(autori.size()>1) {
          String primoAutore = autori.remove(0);
          //System.out.println("Rimosso "+primoAutore+" con autori "+autori+" sono in "+autori.size());
          ListIterator<String> altriAutori = autori.listIterator();
          while(altriAutori.hasNext()) {
            String prossimoAutore = altriAutori.next();
            String arco = null;
            if(primoAutore.compareTo(prossimoAutore)<0) {         //li salvo in ordine
              arco = primoAutore+"\t"+prossimoAutore+"\r\n";
            } else {
              arco = prossimoAutore+"\t"+primoAutore+"\r\n";
            }
            writer.write(arco);
            System.out.println("Coppia "+arco+"\b");
          }
        }
      }
      System.out.println(i+" paper hanno un autore singolo");      
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