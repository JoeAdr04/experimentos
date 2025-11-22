import json
import os

class Persona:
    # Constructor que inicializa id, nombre y carnet
    def __init__(self, id, nombre, carnet):
        # almacena el identificador en un atributo privado
        self.__id = id
        # almacena el nombre en un atributo privado
        self.__nombre = nombre
        # almacena el número/valor del carnet en un atributo privado
        self.__carnet = carnet
        
    # Método para obtener el id (getter)
    def getId(self):
        # devuelve el valor privado __id
        return self.__id
    
    # Método para obtener el nombre (getter)
    def getNombre(self):
        # devuelve el valor privado __nombre
        return self.__nombre
    
    # Método para obtener el carnet (getter)
    def getCarnet(self):
        # devuelve el valor privado __carnet
        return self.__carnet

    # Convierte la instancia a un diccionario simple
    def to_dict(self):
        # retorna un dict con las claves esperadas para serializar
        return {"id": self.__id, "nombre": self.__nombre, "carnet": self.__carnet}

    # Convierte la instancia a una cadena JSON
    def to_json(self):
        # serializa el diccionario a JSON y lo devuelve como string
        return json.dumps(self.to_dict())


class Casa:
    def __init__(self,dir = "", num= 0):
        self.__direccion = dir
        self.__numero = num
        self.__personas = []
        
    def addPersona(self, per:Persona):
        self.__personas.append(per)
    # Retorna la dirección de la casa
    def getDireccion(self):
        return self.__direccion

    # Retorna el número de la casa
    def getNumero(self):
        return self.__numero

    # Retorna la lista de objetos Persona
    def getPersonas(self):
        return list(self.__personas)

    # Convierte la instancia a un diccionario (serializable a JSON)
    def to_dict(self):
        return {
            "direccion": self.__direccion,
            "numero": self.__numero,
            "personas": [p.to_dict() for p in self.__personas]
        }

    # Crea una Casa desde un diccionario (proveniente de JSON)
    @staticmethod
    def from_dict(d):
        c = Casa(d.get('direccion', ''), d.get('numero', 0))
        # si hay personas, convertir cada dict a Persona
        for pd in d.get('personas', []):
            # crear Persona desde dict (espera keys id, nombre, carnet)
            p = Persona(pd.get('id'), pd.get('nombre'), pd.get('carnet'))
            c.addPersona(p)
        return c


class ArchivoCasa:
    """Maneja un archivo JSON que contiene una lista de casas.

    Cada casa se serializa como un diccionario con claves: 'direccion', 'numero', 'personas'.
    """
    def __init__(self, filepath):
        self.filepath = filepath
        if not os.path.exists(self.filepath):
            print("archivo creado")
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def _read_all(self):
        with open(self.filepath, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except (json.JSONDecodeError, ValueError):
                data = []
        return data

    def _write_all(self, list_dicts):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(list_dicts, f, ensure_ascii=False, indent=2)

    def agregar(self, casa: Casa):
        if not isinstance(casa, Casa):
            raise TypeError('Se espera una instancia de Casa')
        data = self._read_all()
        data.append(casa.to_dict())
        self._write_all(data)

    def agregar_por_datos(self, direccion, numero, personas=None):
        c = Casa(direccion, numero)
        # aceptar lista de Persona o lista de dicts
        if personas:
            for item in personas:
                if isinstance(item, Persona):
                    c.addPersona(item)
                elif isinstance(item, dict):
                    p = Persona(item.get('id'), item.get('nombre'), item.get('carnet'))
                    c.addPersona(p)
                else:
                    raise TypeError('personas debe ser lista de Persona o lista de dicts')
        self.agregar(c)

    def listar(self):
        data = self._read_all()
        print("aqui se listo")
        return [Casa.from_dict(d) for d in data]

    def listar_dicts(self):
        return self._read_all()

    def buscar_por_numero(self, numero):
        for d in self._read_all():
            if d.get('numero') == numero:
                return Casa.from_dict(d)
        return None

    def borrar_por_numero(self, numero):
        data = self._read_all()
        new = [d for d in data if d.get('numero') != numero]
        self._write_all(new)
        return len(data) != len(new)

    def limpiar(self):
        self._write_all([])

    

arch = ArchivoCasa("casa.json")
#per = Persona(1,"asdf", 123)
#per2 = Persona(2,"asdfg", 1234)
#casa= Casa("calle falsa", 123)
#casa.addPersona(per)
#casa.addPersona(per2)
#arch.agregar(casa)
x =0
while(x != 4):
    print('''
          Menu de manejo
          1. agregar casa
          2. eliminar casa por numero
          3. listar casas
          4. salir
          ''')
    x = int(input("Ingrese un numero: "))
    if(x == 1):
        x = input("Ingrese direccion: ")
        y = int(input("ingrese numero de la casa, solo numeros: "))
        cas = Casa(x, y)
        arch.agregar(cas)
    elif(x == 2):
        print(arch.listar())
        print("que numoer de casa desea eliminar?")
        x = int(input())
        arch.borrar_por_numero(x)
    elif(x == 3):
        print(arch.listar_dicts())
        