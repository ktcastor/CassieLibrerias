"""
Magiclist es una libreria con la cual puedes tratar listas con objetos jsón 
en forma de querys, por ejemplo como si se tratara de una sentencia sql.

La libreria tiene licencia GPLV3, espero y les guste
"""

#Importamos los módulos de la aplicacion
#Ningún módulo por el momento


#Clase de la libreria
class MagicList():

    #Constructor de la clase que resive como parametro la lista
    def __init__(self,data=[]):
        self.list = data


    #Función que extrae datos especificos de los diccionarios o objetos json
    def select(self,query="",where=""):

        #Creamos una lista donde vamos almacenar los resultados de las busquedas
        customList = []

        #convertimos el texto en lista y limpiamos espacios
        q = [x.strip() for x in query.split(",")]

        #Creamos la lista de acciones (filtros)
        self.actions = []

        #Parseamos el where si existe
        if where:
            # Soportamos "and" y "or" separando condiciones
            filters = where.replace(" and ", ",").replace(" or ", ",").split(",")
            for fi in filters:
                fi = fi.strip()
                # Detectamos el operador
                for op in ["<=", ">=", "<", ">", "=", "!="]:
                    if op in fi:
                        condition_key, condition_value = fi.split(op)
                        condition_key = condition_key.strip()
                        condition_value = condition_value.strip()
                        self.actions.append({"key":condition_key,"action":op,"value":condition_value})
                        break

        #Recorremos cada objeto de la lista
        for obj in self.list:
            try:
                #Validamos si cumple con los filtros
                cumple = True
                for act in self.actions:
                    valor = obj.get(act["key"])
                    if valor is None:
                        cumple = False
                        break

                    # Convertimos a número si aplica
                    try:
                        valor = float(valor)
                        act_val = float(act["value"])
                    except:
                        act_val = act["value"]

                    # Evaluamos según el operador
                    if act["action"] == "=" and str(valor) != str(act_val):
                        cumple = False
                    elif act["action"] == "!=" and str(valor) == str(act_val):
                        cumple = False
                    elif act["action"] == "<" and not (valor < act_val):
                        cumple = False
                    elif act["action"] == ">" and not (valor > act_val):
                        cumple = False
                    elif act["action"] == "<=" and not (valor <= act_val):
                        cumple = False
                    elif act["action"] == ">=" and not (valor >= act_val):
                        cumple = False

                    if not cumple:
                        break

                #Si no cumple, lo saltamos
                if not cumple:
                    continue

                #Si cumple, extraemos los campos solicitados en el query
                row = {}
                for item in q:
                    if item in obj:
                        row[item] = obj[item]

                #Si encontramos datos, los agregamos a la lista personalizada
                if row:
                    customList.append(row)

            except:
                return [{"Error":"Error al buscar datos con el query establecido."}]

        #retornamos la custom list
        return customList


if __name__ == "__main__":

    #Creamos una lista de prueba con diccionarios anidados
    peliculas = [
    {
        "titulo": "Inception",
        "año": 2010,
        "genero": "ciencia ficción",
        "director": {"nombre": "Christopher Nolan", "pais": "Reino Unido"},
        "rating": {"imdb": 8.8, "rotten": 87}
    },
    {
        "titulo": "Parasite",
        "año": 2019,
        "genero": "drama",
        "director": {"nombre": "Bong Joon-ho", "pais": "Corea del Sur"},
        "rating": {"imdb": 8.6, "rotten": 99}
    },
    {
        "titulo": "The Matrix",
        "año": 1999,
        "genero": "acción",
        "director": {"nombre": "Lana Wachowski", "pais": "Estados Unidos"},
        "rating": {"imdb": 8.7, "rotten": 88}
    },
    {
        "titulo": "Spirited Away",
        "año": 2001,
        "genero": "animación",
        "director": {"nombre": "Hayao Miyazaki", "pais": "Japón"},
        "rating": {"imdb": 8.6, "rotten": 97}
    },
    {
        "titulo": "Shrek",
        "año": 2001,
        "genero": "animación",
        "director": {"nombre": "Andrew Adamson", "pais": "Nueva Zelanda"},
        "rating": {"imdb": 7.9, "rotten": 88}
    },
    {
        "titulo": "Finding Nemo",
        "año": 2003,
        "genero": "animación",
        "director": {"nombre": "Andrew Stanton", "pais": "Estados Unidos"},
        "rating": {"imdb": 8.1, "rotten": 99}
    },
    {
        "titulo": "The Incredibles",
        "año": 2004,
        "genero": "animación",
        "director": {"nombre": "Brad Bird", "pais": "Estados Unidos"},
        "rating": {"imdb": 8.0, "rotten": 97}
    },
    {
        "titulo": "Ratatouille",
        "año": 2007,
        "genero": "animación",
        "director": {"nombre": "Brad Bird", "pais": "Estados Unidos"},
        "rating": {"imdb": 8.0, "rotten": 96}
    },
    {
        "titulo": "Wall-E",
        "año": 2008,
        "genero": "animación",
        "director": {"nombre": "Andrew Stanton", "pais": "Estados Unidos"},
        "rating": {"imdb": 8.4, "rotten": 95}
    },
    {
        "titulo": "Up",
        "año": 2009,
        "genero": "animación",
        "director": {"nombre": "Pete Docter", "pais": "Estados Unidos"},
        "rating": {"imdb": 8.2, "rotten": 98}
    }
]


    #Creamos una instancia de MagicList
    magiclist = MagicList(data = peliculas)

    #Ejemplo: seleccionar películas entre 2000 y 2010
    print(magiclist.select(query="titulo,año,genero", where="genero = animación, año>= 2000, año<=2010"))
