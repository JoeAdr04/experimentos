
package com.mycompany.guardados;
import java.io.*;
import java.nio.*;
import com.google.gson.Gson;
import java.util.Scanner;
public class Guardados {

    public static void main(String[] args) {
        Scanner te= new Scanner(System.in);
        ArchPersona arch = new ArchPersona("hola.json");
        String nom = "";
        String dir = "";
        
        int opt =100;
        do{
            System.out.println("-----Menu de manejo de archivos");
            System.out.println("1. LeerArchivo");
            System.out.println("2. Agregar una persona");
            System.out.println("0. Salir");
            System.out.print("Ingrese una opcion: ");
            opt = te.nextInt();
            if(opt == 1){
                System.out.println(arch.leer());
            }
            else if(opt == 2){
                System.out.print("Ingrese Nombre: ");
                nom = te.next();
                System.out.println("Ingrese direccion");
                dir = te.next();
                Persona p = new Persona(nom, dir);
                arch.agregarPersona(p);
            }
        }while(opt!=0);
        
    }
    //Crud: Create, Read, Update, Delete
}
