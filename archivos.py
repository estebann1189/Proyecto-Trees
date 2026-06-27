#archivos.py
#Clase que se encarga de guardar y cargar el arbol desde un archivo JSON

import json
from nodo import Nodo

class ManejadorArchivos:

    #Convierte un nodo y todos sus hijos en un diccionario (recursivo)
    #e: nodo a convertir
    #s: diccionario con la informacion del nodo y sus hijos
    #r: diccionario
    def nodo_a_dict(self, nodo):
        if nodo is None:
            return None

        datos = {}
        datos["texto"] = nodo.texto
        datos["es_pregunta"] = nodo.es_pregunta
        datos["hijo_si"] = self.nodo_a_dict(nodo.hijo_si)
        datos["hijo_no"] = self.nodo_a_dict(nodo.hijo_no)
        return datos

    #Reconstruye un nodo desde un diccionario (recursivo)
    #e: diccionario con datos del nodo
    #s: objeto Nodo reconstruido
    #r: objeto Nodo o None
    def dict_a_nodo(self, datos):
        if datos is None:
            return None

        nodo = Nodo(datos["texto"], datos["es_pregunta"])
        nodo.hijo_si = self.dict_a_nodo(datos["hijo_si"])
        nodo.hijo_no = self.dict_a_nodo(datos["hijo_no"])
        return nodo

    #Guarda el arbol completo en un archivo JSON
    #e: nodo raiz del arbol, ruta del archivo donde guardar
    #s: archivo actualizado en disco, True si funciono o False si hubo error
    #r: booleano
    def guardar(self, raiz, ruta):
        try:
            datos = self.nodo_a_dict(raiz)
            archivo = open(ruta, "w", encoding="utf-8")
            json.dump(datos, archivo, ensure_ascii=False, indent=4)
            archivo.close()
            return True
        except:
            return False

    #Carga el arbol desde un archivo JSON
    #e: ruta del archivo a cargar
    #s: nodo raiz del arbol cargado, o None si hubo error
    #r: objeto Nodo o None
    def cargar(self, ruta):
        try:
            archivo = open(ruta, "r", encoding="utf-8")
            contenido = archivo.read()
            archivo.close()

            #Valida que el archivo no este vacio
            if contenido.strip() == "":
                return None

            datos = json.loads(contenido)

            #Valida que tenga la estructura minima esperada
            if "texto" not in datos or "es_pregunta" not in datos:
                return None

            raiz = self.dict_a_nodo(datos)
            return raiz

        except:
            return None
