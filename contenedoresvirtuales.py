"""
Librería para crear contenedores virtuales, como si fueran una usb
que son unicamente accesibles desde este script con python

la librería tiene licencia GPLV3 por lo que lo puedes portear a tus proyectos
"""

# Importamos las librerias necesarias para el funcionamiento del módulo

# Libreria para trabajar con el sistema operativo
import os

# Libreria para codificar y descodificar archivos en base64
import base64

# Importamos la libreria de json
import json


# crear la clase que crea los contenedores
class PortableContainer():

    # Definimos su constructor donde pedimos el nombre del contenedor y su tamaño en bytes en este caso 1GB
    def __init__(self, name="portable_container", size="1024", unit="MB", path=""):

        self.name = name
        self.size = size
        self.path = path

        # Convertimos el tamaño a bytes según la unidad
        if unit.upper() == "GB":
            self.size = int(size) * 1024 * 1024 * 1024
        elif unit.upper() == "MB":
            self.size = int(size) * 1024 * 1024
        else:
            self.size = int(size)  # ya está en bytes

        # Si el contenedor no existe lo creamos
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump({"max_size": self.size, "files": []}, f)

    # Función para agregar elemenotos al contenedor
    def addItem(self, name="", type="", path=""):

        # Revisamos que exista el archivo
        if os.path.exists(path):

            # Abrimos el archivo que queremos almacenar en el contenedor.
            with open(path, "rb") as f:
                content = f.read()

                # Convertimos el contenido a Base64 para guardarlo en JSON
                content_b64 = base64.b64encode(content).decode("utf-8")

                container = self.read()
                current_size = self.getContainerSize()

                # Validamos contra el tamaño máximo guardado en el JSON
                if current_size + len(content_b64.encode("utf-8")) > container["max_size"]:
                    print(f"⚠️ No se puede agregar '{name}', excede el tamaño máximo del contenedor ({container['max_size']} bytes).")
                    return


                # Almacenamos el contenido del archivo en el contenedor
                self.write(name=name, type=type, data=content_b64)

    # Función para escribir datos en el archivo
    def write(self, name="", type="" , data=None):

        # Checamos que el contenedor exista
        if os.path.exists(self.path):

            # obtenemos el json del contenedor
            container = self.read()

            # Agregamos un nuevo archivo al contenedor
            container["files"].append({"name": name, "type": type ,"data": data})

            # Guardamos el archivo en el contenedor
            self.save(data=container)

    # Función para leer contenedores
    def read(self):
        with open(self.path, "r") as f:
            return json.load(f)

    # Función para guardar archivos en el contenedor
    def save(self, data):
        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)


    #Función para listar que archivos se encuentran en el contenedor
    def getFiles(self):

        #Obtenemos el contenedor para leer su contenido
        container = self.read()


        files = []

        #Recorremos cada uno de los archivos del contenedor
        for item in container["files"]:

            files.append([item["name"],item["type"]])


        #retornamos los archivos del contenedor

        return files

    #Función para retornar un archivo del contenedor
    def getFile(self,name):

        #Obtenemos el contenedor para leer su contenido
        container = self.read()


        try:

            for item in container["files"]:

                if item["name"] == name:


                    #Devolvemos los datos del archivo
                    return item["data"]
        
        except:

            #Si ocurre un error mandamos un arreglo vacio
            return []

    #Función que creca el tamaño del contenedor
    def getContainerSize(self):
        container = self.read()
        total = 0
        for item in container["files"]:
            total += len(item["data"].encode("utf-8"))
        return total


if __name__ == "__main__":

    # Creamos una instancia del contenedor portable
    portableContainer = PortableContainer(
        name="Cassie_Container",
        size="1024",
        path="/home/cassie/Documentos/Cassie_Container.cp"
    )

    # Añadimos elementos al contenedor
    portableContainer.addItem(name="chikorita", type="png" ,path="/home/cassie/Descargas/152.png")
    portableContainer.addItem(name="con otra.mp3", type="mp3" , path="/home/cassie/Descargas/Con Otra.mp3")

    #Imprimimos que archivos tiene el contenedor
    files = portableContainer.getFiles()

    #Imprimimos el contenido de un archivo en especifico
    file = portableContainer.getFile(name="con otra.mp3")
    print(file)

    print(files)
