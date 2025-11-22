# importa el módulo json para trabajar con datos JSON (serializar/deserializar)
import json
# importa el módulo os para comprobar la existencia de archivos y rutas
import os


# Clase que representa una persona con atributos privados
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

    # Método estático para crear una Persona desde una cadena JSON
    @staticmethod
    def from_json(s):
        # parsea la cadena JSON a una estructura de datos (dict)
        data = json.loads(s)
        # crea y retorna una nueva instancia de Persona usando los valores del dict
        return Persona(data.get('id'), data.get('nombre'), data.get('carnet'))


# Clase para manejar un archivo JSON que contiene una lista de personas
class ArchivoPersona:
    """Maneja un archivo JSON que contiene una lista de personas.

    Métodos principales:
    - agregar(persona): añade una instancia de Persona al archivo
    - agregar_por_datos(id, nombre, carnet): crea y añade una Persona
    - listar(): devuelve lista de objetos Persona
    - listar_dicts(): devuelve la lista cruda de diccionarios
    - buscar_por_id(id): devuelve una Persona o None
    - borrar_por_id(id): elimina una entrada por id y devuelve True si se eliminó
    - limpiar(): deja el archivo con una lista vacía
    """
    # Constructor que recibe la ruta del archivo JSON
    def __init__(self, filepath):
        # guarda la ruta proporcionada
        self.filepath = filepath
        # si el archivo no existe, crea uno nuevo con una lista vacía
        if not os.path.exists(self.filepath):
            # abre (crea) el archivo en modo escritura con codificación UTF-8
            with open(self.filepath, 'w', encoding='utf-8') as f:
                # escribe una lista vacía para inicializar el JSON
                json.dump([], f, ensure_ascii=False, indent=2)

    # Lee y retorna toda la lista de personas desde el archivo como lista de dicts
    def _read_all(self):
        # abre el archivo en modo lectura
        with open(self.filepath, 'r', encoding='utf-8') as f:
            try:
                # intenta parsear el JSON completo
                data = json.load(f)
            except (json.JSONDecodeError, ValueError):
                # si hay error de parseo, considera que no hay datos
                data = []
        # retorna la lista (posiblemente vacía)
        return data

    # Escribe la lista completa de diccionarios en el archivo (sobrescribe)
    def _write_all(self, list_dicts):
        # abre el archivo en modo escritura (sobrescribe) y serializa la lista
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(list_dicts, f, ensure_ascii=False, indent=2)

    # Añade una instancia de Persona al archivo
    def agregar(self, persona):
        # valida que el argumento sea una Persona
        if not isinstance(persona, Persona):
            # si no lo es, lanza un TypeError
            raise TypeError('Se espera una instancia de Persona')
        # lee todos los registros actuales
        data = self._read_all()
        # añade el diccionario de la persona nueva
        data.append(persona.to_dict())
        # escribe de nuevo la lista completa en el archivo
        self._write_all(data)

    # Crea y añade una Persona a partir de valores primitivos
    def agregar_por_datos(self, id, nombre, carnet):
        # crea la instancia de Persona
        p = Persona(id, nombre, carnet)
        # reutiliza el método agregar para persistirla
        self.agregar(p)

    # Devuelve una lista de instancias Persona cargadas desde el archivo
    def listar(self):
        # lee la representación cruda (lista de dicts)
        data = self._read_all()
        # convierte cada dict a una instancia Persona y retorna la lista
        return [Persona(d.get('id'), d.get('nombre'), d.get('carnet')) for d in data]

    # Devuelve la lista de diccionarios tal cual está en el archivo
    def listar_dicts(self):
        # retorna los datos crudos leídos del archivo
        return self._read_all()

    # Busca una Persona por su id y devuelve la instancia si la encuentra
    def buscar_por_id(self, id):
        # itera sobre cada diccionario en el archivo
        for d in self._read_all():
            # compara el campo 'id' con el valor buscado
            if d.get('id') == id:
                # si coincide, construye y retorna la Persona encontrada
                return Persona(d.get('id'), d.get('nombre'), d.get('carnet'))
        # si no encuentra nada, retorna None
        return None

    # Elimina una entrada identificada por id (si existe)
    def borrar_por_id(self, id):
        # lee la lista actual
        data = self._read_all()
        # construye una nueva lista excluyendo el id a borrar
        new = []
        for d in data:
            if d.get('id') != id:
                new.append(d)
        # escribe la lista filtrada en el archivo
        self._write_all(new)
        # devuelve True si se eliminó al menos un elemento (longitud cambió)
        return len(data) != len(new)

    # Vacía el archivo dejando una lista vacía
    def limpiar(self):
        # escribe una lista vacía en el archivo
        self._write_all([])


# Ejemplo de uso: crea un archivo JSON llamado 'hola.json' si no existe
archivo = ArchivoPersona("hola.json")

# Crea una instancia de Persona con id=2, nombre 'Luis' y carnet 1235
p1 = Persona(2, "Luis", 1235)
# Añade la persona creada al archivo
archivo.agregar(p1)
print(p1.to_dict())