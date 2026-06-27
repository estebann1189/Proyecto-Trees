#ventana.py
#Clase que maneja toda la interfaz grafica del juego

import tkinter as tk
from tkinter import messagebox, filedialog
from arbol import ArbolDecision
from archivos import ManejadorArchivos

#Colores del tema
FONDO        = "#1a1a1a"
FONDO_PANEL  = "#222222"
COLOR_TEXTO  = "#aaaaaa"
COLOR_GRIS   = "#555555"
COLOR_SI     = "#4a7a5a"
COLOR_NO     = "#7a4a4a"
COLOR_ACENTO = "#555577"
COLOR_BORDE  = "#333333"

#Fuentes
FUENTE_TITULO = ("Courier", 15, "bold")
FUENTE_NORMAL = ("Courier", 11)
FUENTE_CHICA  = ("Courier", 9)
FUENTE_BOTON  = ("Courier", 10)
FUENTE_GRANDE = ("Courier", 13, "bold")

class Ventana:

    #Inicializa la ventana principal y los objetos del juego
    #e: ninguno
    #s: ventana creada y lista para usarse
    #r: ninguno
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Adivina en que estoy pensando")
        self.ventana.geometry("480x440")
        self.ventana.resizable(True, True)
        self.ventana.configure(bg=FONDO)

        self.arbol = ArbolDecision()
        self.manejador = ManejadorArchivos()
        self.ruta_archivo = "arbol_guardado.json"

        #Variables del juego
        self.nodo_actual = None
        self.nodo_padre = None
        self.llego_por_si = False

        self.mostrar_pantalla_inicio()
        self.ventana.mainloop()

    #Elimina todos los widgets actuales de la ventana
    #e: ninguno
    #s: ventana limpia
    #r: ninguno
    def limpiar_pantalla(self):
        for widget in self.ventana.winfo_children():
            widget.destroy()

    #Crea un boton con el estilo del tema
    #e: contenedor padre, texto, color de fondo, funcion, ancho
    #s: objeto Button listo para usar
    #r: objeto Button
    def hacer_boton(self, padre, texto, color, accion, ancho=22):
        boton = tk.Button(
            padre,
            text=texto,
            font=FUENTE_BOTON,
            bg=color,
            fg=COLOR_TEXTO,
            activebackground=FONDO_PANEL,
            activeforeground=COLOR_TEXTO,
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=COLOR_BORDE,
            width=ancho,
            pady=6,
            cursor="hand2",
            command=accion
        )
        return boton

    #Muestra la pantalla de inicio con titulo, instrucciones y botones
    #e: ninguno
    #s: pantalla de inicio visible
    #r: ninguno
    def mostrar_pantalla_inicio(self):
        self.limpiar_pantalla()

        tk.Label(self.ventana,
                 text="adivina en que estoy pensando",
                 font=FUENTE_TITULO,
                 bg=FONDO, fg=COLOR_TEXTO).pack(pady=(32, 2))

        tk.Label(self.ventana,
                 text="responde si o no y el programa intentara adivinar",
                 font=FUENTE_CHICA,
                 bg=FONDO, fg=COLOR_GRIS).pack(pady=(0, 24))

        separador = tk.Frame(self.ventana, bg=COLOR_BORDE, height=1)
        separador.pack(fill="x", padx=40, pady=(0, 24))

        boton_jugar = self.hacer_boton(self.ventana, "iniciar partida", COLOR_SI, self.iniciar_partida)
        boton_jugar.pack(pady=5)

        boton_cargar = self.hacer_boton(self.ventana, "cargar archivo", COLOR_ACENTO, self.cargar_desde_archivo)
        boton_cargar.pack(pady=5)

        boton_guardar = self.hacer_boton(self.ventana, "guardar arbol", COLOR_BORDE, self.guardar_manual)
        boton_guardar.pack(pady=5)

        boton_salir = self.hacer_boton(self.ventana, "salir", COLOR_NO, self.ventana.destroy)
        boton_salir.pack(pady=5)

        self.etiqueta_archivo = tk.Label(self.ventana,
                                          text="arbol por defecto",
                                          font=FUENTE_CHICA,
                                          bg=FONDO, fg=COLOR_GRIS)
        self.etiqueta_archivo.pack(side="bottom", pady=12)

    #Inicia una nueva partida desde la raiz del arbol
    #e: ninguno
    #s: partida comenzada, muestra primera pregunta
    #r: ninguno
    def iniciar_partida(self):
        self.nodo_actual = self.arbol.raiz
        self.nodo_padre = None
        self.llego_por_si = False
        self.mostrar_pregunta()

    #Muestra la pregunta actual o intenta adivinar si llego a una hoja
    #e: ninguno
    #s: pantalla actualizada con pregunta o intento de adivinanza
    #r: ninguno
    def mostrar_pregunta(self):
        self.limpiar_pantalla()

        #Si llego a una hoja intenta adivinar
        if self.arbol.esta_en_hoja(self.nodo_actual):
            self.manejar_hoja()
            return

        tk.Label(self.ventana,
                 text="pregunta",
                 font=FUENTE_CHICA,
                 bg=FONDO, fg=COLOR_GRIS).pack(pady=(30, 6))

        #Caja con la pregunta
        caja = tk.Frame(self.ventana, bg=FONDO_PANEL,
                        highlightthickness=1, highlightbackground=COLOR_BORDE)
        caja.pack(padx=44, fill="x")

        tk.Label(caja,
                 text=self.nodo_actual.texto,
                 font=("Courier", 13, "bold"),
                 bg=FONDO_PANEL, fg=COLOR_TEXTO,
                 wraplength=360, justify="center",
                 padx=20, pady=26).pack()

        tk.Label(self.ventana,
                 text="tu respuesta",
                 font=FUENTE_CHICA,
                 bg=FONDO, fg=COLOR_GRIS).pack(pady=(18, 8))

        marco = tk.Frame(self.ventana, bg=FONDO)
        marco.pack()

        btn_si = self.hacer_boton(marco, "si", COLOR_SI, self.responder_si, ancho=10)
        btn_si.grid(row=0, column=0, padx=10)

        btn_no = self.hacer_boton(marco, "no", COLOR_NO, self.responder_no, ancho=10)
        btn_no.grid(row=0, column=1, padx=10)

        btn_volver = tk.Button(self.ventana, text="volver al menu",
                                font=FUENTE_CHICA,
                                bg=FONDO, fg=COLOR_GRIS,
                                relief="flat", bd=0,
                                activebackground=FONDO,
                                activeforeground=COLOR_TEXTO,
                                cursor="hand2",
                                command=self.mostrar_pantalla_inicio)
        btn_volver.pack(side="bottom", pady=12)

    #Procesa la respuesta Si del usuario y avanza en el arbol
    #e: ninguno
    #s: nodo_actual avanza por rama Si
    #r: ninguno
    def responder_si(self):
        self.nodo_padre = self.nodo_actual
        self.llego_por_si = True
        self.nodo_actual = self.arbol.avanzar(self.nodo_actual, "si")
        self.mostrar_pregunta()

    #Procesa la respuesta No del usuario y avanza en el arbol
    #e: ninguno
    #s: nodo_actual avanza por rama No
    #r: ninguno
    def responder_no(self):
        self.nodo_padre = self.nodo_actual
        self.llego_por_si = False
        self.nodo_actual = self.arbol.avanzar(self.nodo_actual, "no")
        self.mostrar_pregunta()

    #Muestra la pantalla cuando el sistema intenta adivinar
    #e: ninguno
    #s: pantalla con intento de adivinanza y botones para confirmar
    #r: ninguno
    def manejar_hoja(self):
        self.limpiar_pantalla()

        tk.Label(self.ventana,
                 text="creo que se lo que es",
                 font=FUENTE_CHICA,
                 bg=FONDO, fg=COLOR_GRIS).pack(pady=(30, 8))

        caja = tk.Frame(self.ventana, bg=FONDO_PANEL,
                        highlightthickness=1, highlightbackground=COLOR_BORDE)
        caja.pack(padx=44, fill="x")

        tk.Label(caja,
                 text=self.nodo_actual.texto,
                 font=("Courier", 20, "bold"),
                 bg=FONDO_PANEL, fg=COLOR_TEXTO,
                 pady=24).pack()

        tk.Label(self.ventana,
                 text="estabas pensando en eso?",
                 font=FUENTE_NORMAL,
                 bg=FONDO, fg=COLOR_TEXTO).pack(pady=(16, 10))

        marco = tk.Frame(self.ventana, bg=FONDO)
        marco.pack()

        btn_si = self.hacer_boton(marco, "si, adivinaste", COLOR_SI, self.adivino_bien, ancho=14)
        btn_si.grid(row=0, column=0, padx=10)

        btn_no = self.hacer_boton(marco, "no, fallaste", COLOR_NO, self.adivino_mal, ancho=14)
        btn_no.grid(row=0, column=1, padx=10)

    #Muestra el mensaje de victoria cuando el sistema adivino correctamente
    #e: ninguno
    #s: pantalla de exito con opciones de nueva partida o salir
    #r: ninguno
    def adivino_bien(self):
        self.limpiar_pantalla()

        tk.Label(self.ventana,
                 text="lo logre",
                 font=("Courier", 26, "bold"),
                 bg=FONDO, fg=COLOR_SI).pack(pady=(50, 6))

        tk.Label(self.ventana,
                 text="era " + self.nodo_actual.texto,
                 font=FUENTE_NORMAL,
                 bg=FONDO, fg=COLOR_GRIS).pack(pady=(0, 30))

        btn_nuevo = self.hacer_boton(self.ventana, "jugar de nuevo", COLOR_SI, self.iniciar_partida)
        btn_nuevo.pack(pady=5)

        btn_menu = self.hacer_boton(self.ventana, "menu principal", COLOR_ACENTO, self.mostrar_pantalla_inicio)
        btn_menu.pack(pady=5)

        btn_salir = self.hacer_boton(self.ventana, "salir", COLOR_NO, self.ventana.destroy)
        btn_salir.pack(pady=5)

    #Muestra el formulario de aprendizaje cuando el sistema falla al adivinar
    #e: ninguno
    #s: formulario visible para que el usuario ingrese la respuesta correcta
    #r: ninguno
    def adivino_mal(self):
        self.limpiar_pantalla()

        tk.Label(self.ventana,
                 text="falle, ensenname",
                 font=FUENTE_GRANDE,
                 bg=FONDO, fg=COLOR_NO).pack(pady=(18, 2))

        tk.Label(self.ventana,
                 text="completa los campos y aprendere para la proxima",
                 font=FUENTE_CHICA,
                 bg=FONDO, fg=COLOR_GRIS).pack(pady=(0, 10))

        panel = tk.Frame(self.ventana, bg=FONDO_PANEL,
                         highlightthickness=1, highlightbackground=COLOR_BORDE)
        panel.pack(padx=30, fill="x")

        #Campo respuesta correcta
        tk.Label(panel, text="en que estabas pensando?",
                 font=FUENTE_CHICA,
                 bg=FONDO_PANEL, fg=COLOR_TEXTO,
                 anchor="w").grid(row=0, column=0, sticky="w", padx=14, pady=(12, 2))

        self.campo_respuesta = tk.Entry(panel,
                                         font=FUENTE_NORMAL,
                                         bg=FONDO, fg=COLOR_TEXTO,
                                         insertbackground=COLOR_TEXTO,
                                         relief="flat", bd=4, width=32)
        self.campo_respuesta.grid(row=1, column=0, sticky="w", padx=14, pady=(0, 10))

        #Campo nueva pregunta
        texto_label = "que pregunta diferencia tu respuesta de \"" + self.nodo_actual.texto + "\"?"
        tk.Label(panel, text=texto_label,
                 font=FUENTE_CHICA,
                 bg=FONDO_PANEL, fg=COLOR_TEXTO,
                 anchor="w", wraplength=400, justify="left").grid(
                 row=2, column=0, sticky="w", padx=14, pady=(4, 2))

        self.campo_pregunta = tk.Entry(panel,
                                        font=FUENTE_NORMAL,
                                        bg=FONDO, fg=COLOR_TEXTO,
                                        insertbackground=COLOR_TEXTO,
                                        relief="flat", bd=4, width=32)
        self.campo_pregunta.grid(row=3, column=0, sticky="w", padx=14, pady=(0, 10))

        #Seleccion si/no
        tk.Label(panel, text="para tu respuesta, la pregunta seria:",
                 font=FUENTE_CHICA,
                 bg=FONDO_PANEL, fg=COLOR_TEXTO,
                 anchor="w").grid(row=4, column=0, sticky="w", padx=14, pady=(4, 4))

        self.opcion_seleccionada = tk.StringVar()
        self.opcion_seleccionada.set("")

        marco_radio = tk.Frame(panel, bg=FONDO_PANEL)
        marco_radio.grid(row=5, column=0, sticky="w", padx=14, pady=(0, 14))

        tk.Radiobutton(marco_radio, text="si",
                        variable=self.opcion_seleccionada,
                        value="si",
                        font=FUENTE_NORMAL,
                        bg=FONDO_PANEL, fg=COLOR_SI,
                        selectcolor=FONDO,
                        activebackground=FONDO_PANEL).pack(side="left", padx=(0, 30))

        tk.Radiobutton(marco_radio, text="no",
                        variable=self.opcion_seleccionada,
                        value="no",
                        font=FUENTE_NORMAL,
                        bg=FONDO_PANEL, fg=COLOR_NO,
                        selectcolor=FONDO,
                        activebackground=FONDO_PANEL).pack(side="left")

        marco_botones = tk.Frame(self.ventana, bg=FONDO)
        marco_botones.pack(pady=10)

        btn_guardar = self.hacer_boton(marco_botones, "guardar y aprender", COLOR_SI, self.guardar_aprendizaje, ancho=18)
        btn_guardar.grid(row=0, column=0, padx=6)

        btn_cancelar = self.hacer_boton(marco_botones, "cancelar", COLOR_BORDE, self.mostrar_pantalla_inicio, ancho=10)
        btn_cancelar.grid(row=0, column=1, padx=6)

    #Valida los campos y guarda el nuevo aprendizaje en el arbol
    #e: ninguno
    #s: arbol actualizado, archivo guardado automaticamente
    #r: ninguno
    def guardar_aprendizaje(self):
        respuesta_correcta = self.campo_respuesta.get().strip()
        nueva_pregunta = self.campo_pregunta.get().strip()
        opcion = self.opcion_seleccionada.get()

        #Valida campos vacios
        if respuesta_correcta == "":
            messagebox.showwarning("Campo vacio", "Por favor escribe en que estabas pensando.")
            return

        if nueva_pregunta == "":
            messagebox.showwarning("Campo vacio", "Por favor escribe una pregunta para diferenciar la respuesta.")
            return

        if opcion == "":
            messagebox.showwarning("Sin seleccion", "Por favor indica si la respuesta a la pregunta seria si o no.")
            return

        #Aprende la nueva respuesta en el arbol
        nueva_va_en_si = (opcion == "si")
        self.arbol.aprender(self.nodo_padre, self.nodo_actual,
                            respuesta_correcta, nueva_pregunta,
                            nueva_va_en_si, self.llego_por_si)

        #Guarda automaticamente el arbol actualizado
        resultado = self.manejador.guardar(self.arbol.raiz, self.ruta_archivo)

        if resultado:
            messagebox.showinfo("Aprendido", "Aprendi algo nuevo.\nEl arbol fue guardado automaticamente.")
        else:
            messagebox.showwarning("Error al guardar", "No se pudo guardar el arbol, pero el aprendizaje quedo en memoria.")

        self.nueva_partida()

    #Carga un arbol desde un archivo seleccionado por el usuario
    #e: ninguno
    #s: arbol actualizado con el contenido del archivo
    #r: ninguno
    def cargar_desde_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Selecciona el archivo del arbol",
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")]
        )

        if ruta == "" or ruta is None:
            return

        #Carga el arbol desde el archivo
        raiz_cargada = self.manejador.cargar(ruta)

        if raiz_cargada is None:
            messagebox.showerror("Error al cargar",
                                 "No se pudo cargar el archivo.\n"
                                 "Puede estar vacio, danado o con formato incorrecto.\n"
                                 "Se usara el arbol por defecto.")
            self.arbol.crear_arbol_defecto()
            self.etiqueta_archivo.config(text="arbol por defecto")
        else:
            self.arbol.raiz = raiz_cargada
            self.ruta_archivo = ruta
            nombre_archivo = ruta.split("/")[-1]
            messagebox.showinfo("Archivo cargado", "Arbol cargado:\n" + nombre_archivo)
            self.etiqueta_archivo.config(text=nombre_archivo)

    #Guarda el arbol actual manualmente en un archivo
    #e: ninguno
    #s: archivo guardado con el arbol actual
    #r: ninguno
    def guardar_manual(self):
        ruta = filedialog.asksaveasfilename(
            title="Guardar arbol como",
            defaultextension=".json",
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")]
        )

        if ruta == "" or ruta is None:
            return

        resultado = self.manejador.guardar(self.arbol.raiz, ruta)

        if resultado:
            messagebox.showinfo("Guardado", "Arbol guardado en:\n" + ruta)
            self.ruta_archivo = ruta
        else:
            messagebox.showerror("Error", "No se pudo guardar el archivo.")

    #Reinicia la partida volviendo a la pantalla de inicio
    #e: ninguno
    #s: pantalla de inicio mostrada
    #r: ninguno
    def nueva_partida(self):
        self.mostrar_pantalla_inicio()