#nodo.py
#Clase que representa cada nodo del arbol de decision

class Nodo:

    #Crea un nodo del arbol
    #e: texto del nodo, True si es pregunta o False si es respuesta
    #s: objeto Nodo creado
    #r: ninguno
    def __init__(self, texto, es_pregunta):
        self.texto = texto
        self.es_pregunta = es_pregunta
        self.hijo_si = None
        self.hijo_no = None
