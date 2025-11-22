import json
import os

class Charango:
    cont = 0
    def __init__(self, mat="madera"):
        self.__material = mat
        self.__cuerdas = []
        self.__nroCuerdas = 0
        
    def getmaterial(self):
        return self.__material
    def getNroCuerdas(self):
        return self.__nroCuerdas
    def setCuerdas(self, cuerdas):
        self.__cuerdas = cuerdas
    def setNroCuerdas(self):
        self.__nroCuerdas = len(self.__cuerdas)
    def toDict(self):
        return {
            "material":self.__material,
            "nroCuerdas" :self.__nroCuerdas,
            "cuerdas": self.__cuerdas
        }
    
    def dicObj(self, dict):
        c = Charango(dict.get("Material", ""))
        c.setCuerdas(dict.get("cuerdas"))
        return c
            
class ArchivoCharango:
    def __init__(self, ruta:str):
        self.__ruta = ruta
        if not os.path.exists(self.__ruta):
            with open(self.__ruta, 'w') as arch:
                json.dump([], arch, ensure_ascii= False, indent=2)
                
    def leerTodo(self):
        with open(self.__ruta, "r", encoding="utf-8") as file:
            try:
                datos = json.load(file)
            except Exception as e:
                print(e)
                datos = []
            return datos
        
    def modificarArch(self, dict):
        try:
            with open(self.__ruta, "w", encoding="utf-8") as file:
                json.dump(dict, file,ensure_ascii=False, indent=2)
        except Exception as e:
            print("no s epudoi modificar", e)
        
    def agregarCharango(self, c:Charango):
        datos = self.leerTodo()
        datos.append(c.toDict())
        self.modificarArch(datos)
class Main:
    x = 0
    arch = None
    while(x !=4):
        print('''
    Menu:
    1. CrearArchivo
    2. Agregar un Charango
    3. listar Todos los charangos
    4. salir
          ''')
        x = int(input("Seleccione una opcion: "))
        if (x == 1):
            arch = ArchivoCharango("charangos.json")
        elif(x == 2):
            y = input("material del charango: ")
            c = Charango(y)
            arch.agregarCharango(c)
        elif(x == 3):
            print(arch.leerTodo())
        