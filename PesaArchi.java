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

public class PesaArchi
{
  public static void main(String[] args)
  {
    //da
    //autore1 autore2
    //autore1 autore3
    //autore1 autore2
    //a
    //autore1 autore2 2
    //autore1 autore3 1
    //un altro modo per farlo è caricare man mano gli archi in un set
    
    
    String input = "EdgeDEI.txt";
    //input  = "PesaArchiTest.txt";
    String output = "EdgeDEIPesati1.txt";
    //output  = "PesaArchiTestOutput.txt";
   
    FileReader reader = null;
    Scanner sc = null;
    BufferedWriter writer = null;
    
    try {
      reader = new FileReader(input);
      sc = new Scanner(reader);
      writer = new BufferedWriter(new FileWriter(output));
      String line = sc.nextLine();
      int i = 0;
      
      while (sc.hasNextLine()) {
        String newLine = null;
        int weight = 1;
        do {
          newLine = sc.nextLine();            //la prossima riga forse non c'è solo la prima volta
          if(line.equals(newLine)) {          //sono uguali?
            weight=weight+1;      //alzo il peso
          }
        } while(sc.hasNextLine() && line.equals(newLine));  //se sono diversi o è finito il file esce

        writer.write(line+"\t"+weight+"\r\n");
        //System.out.println("Coppia "+line+"\t"+weight);

        line = newLine;                       //il prossimo ciclo questa sarà la line col paper
        if(!sc.hasNextLine()) {               //se è l'unica rimasta
          writer.write(line+"\t1\r\n");   //sarà un edge con peso 1
          //System.out.println("Coppia "+line+"\t"+"1");
        }
      }
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