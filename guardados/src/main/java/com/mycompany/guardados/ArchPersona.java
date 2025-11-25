/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany.guardados;

import java.io.*;
import java.nio.*;
import java.nio.file.Files;
import com.google.gson.GsonBuilder;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.List;

public class ArchPersona {
    private String direccion;
    private Gson gson = new GsonBuilder().setPrettyPrinting().create();
    
   public ArchPersona(String direccion){
       this.direccion = direccion;
       try{
           File a = new File(this.direccion);
           if(!a.exists()){
               ArrayList<Persona> lista = new ArrayList<>();
            try (FileWriter nuevo = new FileWriter(this.direccion)) {
                gson.toJson(lista, nuevo);
            }
           }
       }
       catch (IOException e){
           System.out.println(e);
       }
   }
   
   public List<Persona> leer(){
       try{
           File arch = new File(this.direccion);
           if (!arch.exists()){
               return new ArrayList<>();
           }
           else{
               Type lista = new TypeToken<List<Persona>>() {}.getType();
               List<Persona> resultado = gson.fromJson(new FileReader(this.direccion), lista);
               if (resultado == null) {
                   return new ArrayList<>();
               }
               return resultado;
           }
       }
       catch(Exception e){
           System.out.println(e);
           return new ArrayList<>();
       }
    }
   public void modificar(List<Persona> personas){
       try(FileWriter file = new FileWriter(this.direccion);){
          gson.toJson(personas, file);
       }
       catch(IOException e){
           System.out.println(e);
       }
   }
   public void agregarPersona(Persona p){
       List<Persona> personas = this.leer();
       personas.add(p);
       this.modificar(personas);
   }
}
