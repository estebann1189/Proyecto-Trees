#arbol.py
#Clase que maneja la logica del arbol de decision binario

from nodo import Nodo

class ArbolDecision:

    #Inicializa el arbol con un arbol por defecto
    #e: ninguno
    #s: arbol con raiz creada
    #r: ninguno
    def __init__(self):
        self.raiz = None
        self.crear_arbol_defecto()

    #Crea el arbol inicial minimo con una pregunta y dos respuestas
    #e: ninguno
    #s: self.raiz apunta al arbol por defecto
    #r: ninguno
    def crear_arbol_defecto(self):
        raiz = Nodo("¿Es un animal?", True)
        raiz.hijo_si = Nodo("perro", False)
        raiz.hijo_no = Nodo("computadora", False)
        self.raiz = raiz

    #Revisa si el nodo actual es una hoja (respuesta final)
    #e: nodo a revisar
    #s: True si es hoja, False si no
    #r: booleano
    def esta_en_hoja(self, nodo):
        if nodo.es_pregunta == False:
            return True
        return False

    #Avanza al siguiente nodo segun la respuesta del usuario
    #e: nodo actual, respuesta "si" o "no"
    #s: el hijo correspondiente del nodo
    #r: objeto Nodo
    def avanzar(self, nodo, respuesta):
        if respuesta == "si":
            return nodo.hijo_si
        else:
            return nodo.hijo_no

    #Aprende una nueva respuesta reemplazando la hoja incorrecta
    #e: nodo padre del incorrecto, nodo incorrecto, respuesta correcta nueva,
    #   nueva pregunta, si la nueva respuesta va en rama si o no,
    #   y si el padre llego por si o no
    #s: el arbol actualizado con el nuevo nodo
    #r: ninguno
    def aprender(self, padre, nodo_incorrecto, respuesta_correcta, nueva_pregunta, nueva_va_en_si, llego_por_si):
        #Crea la nueva pregunta y los dos nuevos nodos hoja
        nuevo_nodo_pregunta = Nodo(nueva_pregunta, True)
        nodo_correcto = Nodo(respuesta_correcta, False)

        #Coloca los hijos segun donde va la respuesta nueva
        if nueva_va_en_si:
            nuevo_nodo_pregunta.hijo_si = nodo_correcto
            nuevo_nodo_pregunta.hijo_no = nodo_incorrecto
        else:
            nuevo_nodo_pregunta.hijo_si = nodo_incorrecto
            nuevo_nodo_pregunta.hijo_no = nodo_correcto

        #Reemplaza el nodo incorrecto en el padre
        if padre is None:
            self.raiz = nuevo_nodo_pregunta
        elif llego_por_si:
            padre.hijo_si = nuevo_nodo_pregunta
        else:
            padre.hijo_no = nuevo_nodo_pregunta
