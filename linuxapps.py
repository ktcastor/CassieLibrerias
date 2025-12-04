"""

Linux apps es una libreria desarollada por Cassie con la licencia GPLV3
que te permite listar las apps que tiendes instaladas en tu ordenadador,
podras obtener su nombre o nombres, su icono de la aplicación, y como se 
tiene que llamar para ejecutar la aplicación

Espero y les guste pequeños.

"""


#Importamos las librerias para el módulo
import os


#clase de la libreria
class LinuxApps():

	#Constructor de la clase
	def __init__(self):

		"""

		Guardamos los directorios principales donde se guardan los archivos .desktop de las aplicaciones instaladas.

		En GNU/Linux utilizan los archivos .desktop para agregar información de las aplicaciones instaladas individualmente
		asi como sus nombres, iconos y como ejecutar la app

		"""

		self.appsFolder = [
		    "/usr/share/applications/",
		    "/usr/local/share/applications/",
		    os.path.expanduser("~/.local/share/applications/"),
		    os.path.expanduser("~/.local/share/flatpak/exports/share/applications/"),
		    "/var/lib/flatpak/exports/share/applications/",
		    "/var/lib/snapd/desktop/applications/"
		]

	#función para optener las apps instaladas en el pc con Linux
	def currentApps(self):

		#Almacenamos las apps en una lista en forma de lista
		self.apps = []

		#Recorremos cada uno de los direcctorios que pueden contener apps instaladas en la distro
		for app in self.appsFolder:

			#Checamos que el directorio exista
			if os.path.exists(app):		

				#Extraemos las apps del directorio y las almacenamos
				desktop = os.listdir(app)

				for dsk in desktop:

					path = app + dsk
					self.apps.append({dsk:path})

		#Retornamos la información
		return self.apps

	#Función que obtiene información detallada de cada una de las apps, como sus nombres, iconos y como ejecutarla
	def getInfoApps(self):

		self.infoApps = []

		#Recorremos cada uno de los .desktop de cada una de las aplicaciones
		for dsk in self.apps:

			for name , path in dsk.items():

				#Abrimos el archivo de .desktop de cada app
				with open(path, "r", encoding="utf-8", errors="ignore") as f:

					app_names = {}
					app_icon = None
					app_exec = None

					#Recorremos cada una de las lineas que tiene el archivo . desktop y guardamos solo los nombres que sean en ingles y español
					for line in f:
						if line.startswith("Name"):

							key, value = line.split("=",1)

							if key.strip() in ["Name", "Name[es]", "Name[en]"]:
								app_names[key.strip()] = value.strip()


						if line.startswith("Exec="):
							app_exec = line.split("=",1)[1].strip()

						if line.startswith("Icon="):
							app_icon = line.split("=",1)[1].strip()

					#Guardamos la información de la aplicación en un diccionario
					self.infoApps.append({"names":app_names,"icon":app_icon,"execute":app_exec})

		#Retornamos la información
		return self.infoApps



if __name__ == "__main__":

	#Creamos una instancia de la clase LinuxApps
	linuxApps = LinuxApps()

	#Recorremos cada uno de los elementos de la lista para obtener su .desktop
	for app in linuxApps.currentApps():

		#Imprimimos la información
		print(app)


	#Espacio de separación
	print()


	#Recorremos cada uno de los elementos de la lista para obtener información detallada de las apps
	for app in linuxApps.getInfoApps():

		print(app)