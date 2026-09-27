import json
import os
import random
from datetime import datetime


from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle, Ellipse, Triangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen


# ============================================================
# COLORES
# ============================================================

NEGRO = (0, 0, 0, 1)
AMARILLO = (1, 0.816, 0, 1)
AMARILLO_CLARO = (1, 0.945, 0.46, 1)
BLANCO = (1, 1, 1, 1)

GRIS = (0.08, 0.08, 0.08, 1)
GRIS_HOVER = (0.145, 0.145, 0.145, 1)


# ============================================================
# FONDO ANIMADO
# ============================================================

class FondoAnimado(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.figuras = []

        self.crear_figuras()

        Clock.schedule_interval(
            self.animar,
            1 / 25
        )

    def crear_figuras(self):

        for _ in range(28):

            tipo = random.choice([
                "rect",
                "circle",
                "triangle"
            ])

            x = random.randint(0, 1200)
            y = random.randint(0, 800)

            tam = random.randint(8, 25)

            vx = random.choice([
                -1.0,
                -0.5,
                0.5,
                1.0
            ])

            vy = random.choice([
                -1.0,
                -0.5,
                0.5,
                1.0
            ])

            with self.canvas:

                Color(
                    0.23,
                    0.19,
                    0,
                    0.65
                )

                if tipo == "rect":

                    figura = Rectangle(
                        pos=(x, y),
                        size=(tam, tam)
                    )

                elif tipo == "circle":

                    figura = Ellipse(
                        pos=(x, y),
                        size=(tam, tam)
                    )

                else:

                    figura = Triangle(
                        points=(
                            x,
                            y,
                            x + tam / 2,
                            y + tam,
                            x + tam,
                            y
                        )
                    )

            self.figuras.append(
                [
                    figura,
                    vx,
                    vy
                ]
            )

    def animar(self, dt):

        for figura, vx, vy in self.figuras:

            x, y = figura.pos

            figura.pos = (
                x + vx,
                y + vy
            )

            if figura.pos[0] < -40:

                figura.pos = (
                    self.width + 40,
                    figura.pos[1]
                )

            elif figura.pos[0] > self.width + 40:

                figura.pos = (
                    -40,
                    figura.pos[1]
                )

            if figura.pos[1] < -40:

                figura.pos = (
                    figura.pos[0],
                    self.height + 40
                )

            elif figura.pos[1] > self.height + 40:

                figura.pos = (
                    figura.pos[0],
                    -40
                )


# ============================================================
# PANTALLA BASE
# ============================================================

class FondoScreen(Screen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.fondo = FondoAnimado()

        self.add_widget(
            self.fondo
        )

        self.contenido = BoxLayout(
            orientation="vertical",
            padding=dp(25),
            spacing=dp(12)
        )

        self.add_widget(
            self.contenido
        )

    def limpiar(self):

        self.contenido.clear_widgets()

    def agregar(self, widget):

        self.contenido.add_widget(
            widget
        )


# ============================================================
# FUNCIONES VISUALES
# ============================================================

def etiqueta(
    texto,
    size=18,
    color=BLANCO,
    height=dp(45)
):

    return Label(
        text=texto,
        font_size=dp(size),
        color=color,
        size_hint_y=None,
        height=height,
        halign="center",
        valign="middle"
    )


def boton(
    texto,
    callback,
    height=dp(52),
    amarillo=True
):

    b = Button(

        text=texto,

        font_size=dp(15),

        bold=True,

        size_hint_y=None,

        height=height,

        background_normal="",

        background_down="",

        background_color=(
            AMARILLO
            if amarillo
            else GRIS
        ),

        color=(
            NEGRO
            if amarillo
            else BLANCO
        )
    )

    b.bind(
        on_release=callback
    )

    return b


# ============================================================
# APP
# ============================================================

class ArgentumApp(App):

    def build(self):

        self.title = (
            "ARGENTUM - Competencias de Rap"
        )

        self.competencia = {

            "nombre": "",

            "fecha": "",

            "competidores": [],

            "rondas": [],

            "campeon": None
        }

        self.sm = ScreenManager()

        self.inicio = FondoScreen(
            name="inicio"
        )

        self.crear = FondoScreen(
            name="crear"
        )

        self.competidores = FondoScreen(
            name="competidores"
        )

        self.cuadro = FondoScreen(
            name="cuadro"
        )

        self.guardadas = FondoScreen(
            name="guardadas"
        )

        self.campeon_screen = FondoScreen(
            name="campeon"
        )

        for screen in [

            self.inicio,

            self.crear,

            self.competidores,

            self.cuadro,

            self.guardadas,

            self.campeon_screen

        ]:

            self.sm.add_widget(
                screen
            )

        self.pantalla_inicio()

        return self.sm

    # ========================================================
    # ARCHIVOS
    # ========================================================

    def ruta_archivo(self):

        return os.path.join(
            self.user_data_dir,
            "competencias.json"
        )

    def cargar_competencias(self):

        archivo = self.ruta_archivo()

        try:

            if os.path.exists(archivo):

                with open(
                    archivo,
                    "r",
                    encoding="utf-8"
                ) as f:

                    datos = json.load(f)

                    if isinstance(datos, list):

                        return datos

        except Exception:

            pass

        return []

    def guardar_competencia(self):

        lista = self.cargar_competencias()

        reemplazada = False

        for i, item in enumerate(lista):

            if (

                item.get("nombre")
                == self.competencia["nombre"]

                and

                item.get("fecha")
                == self.competencia["fecha"]

            ):

                lista[i] = self.competencia

                reemplazada = True

                break

        if not reemplazada:

            lista.append(
                self.competencia
            )

        os.makedirs(
            self.user_data_dir,
            exist_ok=True
        )

        with open(
            self.ruta_archivo(),
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                lista,
                f,
                ensure_ascii=False,
                indent=2
            )

    # ========================================================
    # INICIO
    # ========================================================

    def pantalla_inicio(self):

        s = self.inicio

        s.limpiar()

        s.agregar(
            Widget(
                size_hint_y=1
            )
        )

        s.agregar(
            etiqueta(
                "ARGENTUM",
                42,
                AMARILLO,
                dp(70)
            )
        )

        s.agregar(
            etiqueta(
                "COMPETENCIAS DE RAP",
                19,
                BLANCO,
                dp(50)
            )
        )

        s.agregar(
            boton(
                "CREAR COMPETENCIA",
                lambda *_:
                self.pantalla_crear(),
                dp(58),
                True
            )
        )

        s.agregar(
            boton(
                "COMPETENCIAS GUARDADAS",
                lambda *_:
                self.mostrar_competencias(),
                dp(58),
                False
            )
        )

        s.agregar(
            Widget(
                size_hint_y=1
            )
        )

        self.sm.current = "inicio"

    # ========================================================
    # CREAR COMPETENCIA
    # ========================================================

    def pantalla_crear(self):

        s = self.crear

        s.limpiar()

        s.agregar(
            Widget(
                size_hint_y=None,
                height=dp(40)
            )
        )

        s.agregar(
            etiqueta(
                "NUEVA COMPETENCIA",
                30,
                AMARILLO,
                dp(60)
            )
        )

        s.agregar(
            etiqueta(
                "Nombre de la competencia",
                15,
                BLANCO
            )
        )

        self.entrada_nombre = TextInput(

            multiline=False,

            font_size=dp(17),

            foreground_color=BLANCO,

            background_color=GRIS,

            cursor_color=AMARILLO,

            padding=[
                dp(12),
                dp(12)
            ],

            size_hint_y=None,

            height=dp(52)
        )

        s.agregar(
            self.entrada_nombre
        )

        s.agregar(
            etiqueta(
                "Fecha del evento (DD/MM/AAAA)",
                15,
                BLANCO
            )
        )

        self.entrada_fecha = TextInput(

            text=datetime.now().strftime(
                "%d/%m/%Y"
            ),

            multiline=False,

            font_size=dp(17),

            foreground_color=BLANCO,

            background_color=GRIS,

            cursor_color=AMARILLO,

            padding=[
                dp(12),
                dp(12)
            ],

            size_hint_y=None,

            height=dp(52)
        )

        s.agregar(
            self.entrada_fecha
        )

        s.agregar(
            Widget(
                size_hint_y=1
            )
        )

        s.agregar(
            boton(
                "CONTINUAR",
                self.continuar_creacion,
                dp(58),
                True
            )
        )

        s.agregar(
            boton(
                "VOLVER",
                lambda *_:
                self.pantalla_inicio(),
                dp(52),
                False
            )
        )

        self.sm.current = "crear"

    def continuar_creacion(self, *_):

        nombre = (
            self.entrada_nombre.text
            .strip()
        )

        fecha = (
            self.entrada_fecha.text
            .strip()
        )

        if not nombre or not fecha:

            return

        self.competencia = {

            "nombre": nombre,

            "fecha": fecha,

            "competidores": [],

            "rondas": [],

            "campeon": None
        }

        self.pantalla_competidores()

    # ========================================================
    # COMPETIDORES
    # ========================================================

    def pantalla_competidores(self):

        s = self.competidores

        s.limpiar()

        s.agregar(
            etiqueta(
                "COMPETIDORES",
                30,
                AMARILLO,
                dp(55)
            )
        )

        s.agregar(
            etiqueta(
                f"{self.competencia['nombre']}  •  "
                f"{self.competencia['fecha']}",
                14,
                BLANCO,
                dp(42)
            )
        )

        fila = BoxLayout(

            orientation="horizontal",

            size_hint_y=None,

            height=dp(52),

            spacing=dp(8)
        )

        self.entrada_competidor = TextInput(

            hint_text="Nombre del competidor",

            multiline=False,

            font_size=dp(16),

            foreground_color=BLANCO,

            hint_text_color=(
                0.55,
                0.55,
                0.55,
                1
            ),

            background_color=GRIS,

            cursor_color=AMARILLO,

            padding=[
                dp(10),
                dp(10)
            ]
        )

        self.entrada_competidor.bind(
            on_text_validate=
            self.agregar_competidor
        )

        fila.add_widget(
            self.entrada_competidor
        )

        fila.add_widget(
            boton(
                "+ AGREGAR",
                self.agregar_competidor,
                dp(52),
                True
            )
        )

        s.agregar(fila)

        scroll = ScrollView(
            size_hint_y=1
        )

        self.lista_layout = BoxLayout(

            orientation="vertical",

            spacing=dp(6),

            padding=[
                0,
                dp(5)
            ],

            size_hint_y=None
        )

        self.lista_layout.bind(
            minimum_height=
            self.lista_layout.setter(
                "height"
            )
        )

        scroll.add_widget(
            self.lista_layout
        )

        s.agregar(scroll)

        acciones = BoxLayout(

            orientation="horizontal",

            size_hint_y=None,

            height=dp(54),

            spacing=dp(8)
        )

        acciones.add_widget(

            boton(
                "− QUITAR SELECCIONADO",
                self.quitar_ultimo_competidor,
                dp(54),
                False
            )
        )

        acciones.add_widget(

            boton(
                "▶ EMPEZAR COMPE",
                self.empezar_competencia,
                dp(54),
                True
            )
        )

        s.agregar(
            acciones
        )

        s.agregar(
            boton(
                "VOLVER",
                lambda *_:
                self.pantalla_crear(),
                dp(48),
                False
            )
        )

        self.actualizar_lista_competidores()

        self.sm.current = "competidores"

    def agregar_competidor(self, *_):

        nombre = (
            self.entrada_competidor.text
            .strip()
        )

        if not nombre:

            return

        for existente in self.competencia[
            "competidores"
        ]:

            if existente.lower() == nombre.lower():

                self.entrada_competidor.text = ""

                return

        self.competencia[
            "competidores"
        ].append(nombre)

        self.entrada_competidor.text = ""

        self.actualizar_lista_competidores()

    def quitar_ultimo_competidor(self, *_):

        if self.competencia[
            "competidores"
        ]:

            self.competencia[
                "competidores"
            ].pop()

            self.actualizar_lista_competidores()

    def actualizar_lista_competidores(self):

        if not hasattr(
            self,
            "lista_layout"
        ):

            return

        self.lista_layout.clear_widgets()

        if not self.competencia[
            "competidores"
        ]:

            self.lista_layout.add_widget(

                etiqueta(
                    "Todavía no hay competidores.",
                    15,
                    (
                        0.55,
                        0.55,
                        0.55,
                        1
                    ),
                    dp(45)
                )
            )

            return

        for i, nombre in enumerate(

            self.competencia[
                "competidores"
            ],

            1

        ):

            fila = BoxLayout(

                orientation="horizontal",

                size_hint_y=None,

                height=dp(48),

                spacing=dp(8)
            )

            fila.add_widget(

                Label(

                    text=f"{i:02d}",

                    font_size=dp(15),

                    bold=True,

                    color=AMARILLO,

                    size_hint_x=None,

                    width=dp(45)
                )
            )

            fila.add_widget(

                Label(

                    text=nombre,

                    font_size=dp(16),

                    color=BLANCO,

                    halign="left",

                    valign="middle"
                )
            )

            self.lista_layout.add_widget(
                fila
            )

    # ========================================================
    # CUADRO
    # ========================================================

    def siguiente_potencia_de_dos(
        self,
        numero
    ):

        potencia = 1

        while potencia < numero:

            potencia *= 2

        return potencia

    def nombre_ronda(
        self,
        cantidad
    ):

        nombres = {

            2: "FINAL",

            4: "SEMIFINAL",

            8: "CUARTOS DE FINAL",

            16: "OCTAVOS DE FINAL",

            32: "DIECISEISAVOS DE FINAL",

            64: "TREINTAIDOSAVOS DE FINAL"
        }

        return nombres.get(
            cantidad,
            f"RONDA DE {cantidad}"
        )

    def empezar_competencia(self, *_):

        cantidad = len(
            self.competencia[
                "competidores"
            ]
        )

        if cantidad < 2:

            return

        self.competencia[
            "rondas"
        ] = []

        self.competencia[
            "campeon"
        ] = None

        self.generar_cuadro()

        self.pantalla_cuadro()

    def generar_cuadro(self):

        competidores = self.competencia[
            "competidores"
        ].copy()

        random.shuffle(
            competidores
        )

        cantidad = (
            self.siguiente_potencia_de_dos(
                len(competidores)
            )
        )

        while len(competidores) < cantidad:

            competidores.append(
                "BYE"
            )

        ronda = []

        for i in range(
            0,
            len(competidores),
            2
        ):

            ronda.append({

                "jugador1":
                competidores[i],

                "jugador2":
                competidores[i + 1],

                # IMPORTANTE:
                # NUNCA se asigna ganador
                # automáticamente.
                "ganador": None
            })

        self.competencia[
            "rondas"
        ] = [{

            "nombre":
            self.nombre_ronda(
                cantidad
            ),

            "combates":
            ronda
        }]

    # ========================================================
    # SELECCIONAR GANADOR
    # ========================================================

    def seleccionar_ganador(
        self,
        indice,
        jugador
    ):

        # ==========================================
        # BYE NO PUEDE SER GANADOR
        # ==========================================

        if jugador == "BYE":

            return

        ronda = self.competencia[
            "rondas"
        ][-1]

        combate = ronda[
            "combates"
        ][indice]

        # ==========================================
        # SI YA HAY GANADOR:
        # NO MOSTRAR VENTANA
        # NO CAMBIAR NADA
        # ==========================================

        if combate[
            "ganador"
        ] is not None:

            return

        # ==========================================
        # ÚNICO LUGAR DONDE SE ASIGNA GANADOR
        #
        # SOLO ocurre cuando el usuario toca
        # el botón del competidor.
        # ==========================================

        combate[
            "ganador"
        ] = jugador

        self.pantalla_cuadro()

    # ========================================================
    # ESTADO DE RONDA
    # ========================================================

    def ronda_terminada(self):

        if not self.competencia[
            "rondas"
        ]:

            return False

        ronda = self.competencia[
            "rondas"
        ][-1]

        for combate in ronda[
            "combates"
        ]:

            if combate[
                "ganador"
            ] is None:

                return False

        return True

    def obtener_ganadores(self):

        ganadores = []

        ronda = self.competencia[
            "rondas"
        ][-1]

        for combate in ronda[
            "combates"
        ]:

            ganador = combate[
                "ganador"
            ]

            if ganador:

                ganadores.append(
                    ganador
                )

        return ganadores

    # ========================================================
    # SIGUIENTE RONDA
    # ========================================================

    def siguiente_ronda(self, *_):

        # Nunca avanzar si falta elegir
        # manualmente algún ganador.

        if not self.ronda_terminada():

            return

        ganadores = (
            self.obtener_ganadores()
        )

        # ==========================================
        # CAMPEÓN
        # ==========================================

        if len(ganadores) == 1:

            self.competencia[
                "campeon"
            ] = ganadores[0]

            self.guardar_competencia()

            self.mostrar_campeon()

            return

        nuevos_combates = []

        for i in range(
            0,
            len(ganadores),
            2
        ):

            jugador1 = ganadores[i]

            if i + 1 < len(ganadores):

                jugador2 = ganadores[
                    i + 1
                ]

            else:

                jugador2 = "BYE"

            nuevos_combates.append({

                "jugador1":
                jugador1,

                "jugador2":
                jugador2,

                # MUY IMPORTANTE:
                # la nueva batalla comienza
                # SIN GANADOR.
                "ganador": None
            })

        self.competencia[
            "rondas"
        ].append({

            "nombre":
            self.nombre_ronda(
                len(ganadores)
            ),

            "combates":
            nuevos_combates
        })

        self.pantalla_cuadro()

    # ========================================================
    # BOTÓN DE COMPETIDOR
    # ========================================================

    def boton_jugador(
        self,
        tarjeta,
        indice,
        ganador,
        jugador
    ):

        # ==========================================
        # BYE:
        # SOLO TEXTO
        # NO ES BOTÓN
        # NO GENERA GANADOR
        # ==========================================

        if jugador == "BYE":

            b = Label(

                text="BYE",

                font_size=dp(14),

                bold=True,

                color=(
                    0.4,
                    0.4,
                    0.4,
                    1
                ),

                size_hint_y=None,

                height=dp(48)
            )

        else:

            # ======================================
            # COMPETIDOR REAL:
            # SIEMPRE ES SELECCIONABLE MANUALMENTE
            # ======================================

            b = Button(

                text=jugador,

                font_size=dp(15),

                bold=True,

                background_normal="",

                background_down="",

                background_color=(

                    AMARILLO

                    if ganador == jugador

                    else GRIS_HOVER
                ),

                color=(

                    NEGRO

                    if ganador == jugador

                    else BLANCO
                ),

                size_hint_y=None,

                height=dp(48)
            )

            b.bind(

                on_release=lambda *_:
                self.seleccionar_ganador(
                    indice,
                    jugador
                )
            )

        tarjeta.add_widget(
            b
        )

    # ========================================================
    # PANTALLA CUADRO
    # ========================================================

    def pantalla_cuadro(self):

        s = self.cuadro

        s.limpiar()

        ronda = self.competencia[
            "rondas"
        ][-1]

        s.agregar(

            etiqueta(
                "ARGENTUM",
                28,
                AMARILLO,
                dp(45)
            )
        )

        s.agregar(

            etiqueta(

                f"{ronda['nombre']}  •  "
                f"{self.competencia['nombre']}",

                18,

                BLANCO,

                dp(45)
            )
        )

        scroll = ScrollView(
            size_hint_y=1
        )

        lista = BoxLayout(

            orientation="vertical",

            spacing=dp(12),

            padding=[
                dp(8),
                dp(8)
            ],

            size_hint_y=None
        )

        lista.bind(

            minimum_height=
            lista.setter(
                "height"
            )
        )

        for i, combate in enumerate(

            ronda[
                "combates"
            ]
        ):

            tarjeta = BoxLayout(

                orientation="vertical",

                spacing=dp(5),

                padding=[
                    dp(12),
                    dp(10)
                ],

                size_hint_y=None,

                height=dp(185)
            )

            with tarjeta.canvas.before:

                Color(*GRIS)

                rect = Rectangle(

                    pos=tarjeta.pos,

                    size=tarjeta.size
                )

            tarjeta.bind(

                pos=lambda inst,
                val,
                r=rect:
                setattr(
                    r,
                    "pos",
                    val
                ),

                size=lambda inst,
                val,
                r=rect:
                setattr(
                    r,
                    "size",
                    val
                )
            )

            tarjeta.add_widget(

                etiqueta(

                    f"BATALLA {i + 1}",

                    13,

                    AMARILLO,

                    dp(30)
                )
            )

            # ======================================
            # JUGADOR 1
            # ======================================

            self.boton_jugador(

                tarjeta,

                i,

                combate[
                    "ganador"
                ],

                combate[
                    "jugador1"
                ]
            )

            tarjeta.add_widget(

                etiqueta(

                    "VS",

                    12,

                    (
                        0.5,
                        0.5,
                        0.5,
                        1
                    ),

                    dp(24)
                )
            )

            # ======================================
            # JUGADOR 2
            # ======================================

            self.boton_jugador(

                tarjeta,

                i,

                combate[
                    "ganador"
                ],

                combate[
                    "jugador2"
                ]
            )

            # ======================================
            # ESTADO
            # ======================================

            if combate[
                "ganador"
            ]:

                tarjeta.add_widget(

                    etiqueta(

                        "✓ GANADOR: "
                        + combate[
                            "ganador"
                        ],

                        12,

                        AMARILLO,

                        dp(25)
                    )
                )

            else:

                tarjeta.add_widget(

                    etiqueta(

                        "SELECCIONÁ EL GANADOR",

                        11,

                        (
                            0.5,
                            0.5,
                            0.5,
                            1
                        ),

                        dp(25)
                    )
                )

            lista.add_widget(
                tarjeta
            )

        scroll.add_widget(
            lista
        )

        s.agregar(
            scroll
        )

        # ==========================================
        # SIGUIENTE RONDA
        # ==========================================

        if self.ronda_terminada():

            s.agregar(

                boton(

                    "▶ SIGUIENTE RONDA",

                    self.siguiente_ronda,

                    dp(58),

                    True
                )
            )

        else:

            s.agregar(

                etiqueta(

                    "Elegí manualmente el ganador de cada batalla.",

                    13,

                    (
                        0.55,
                        0.55,
                        0.55,
                        1
                    ),

                    dp(38)
                )
            )

        acciones = BoxLayout(

            orientation="horizontal",

            size_hint_y=None,

            height=dp(52),

            spacing=dp(8)
        )

        acciones.add_widget(

            boton(

                "GUARDAR",

                lambda *_:
                self.guardar_competencia(),

                dp(52),

                False
            )
        )

        acciones.add_widget(

            boton(

                "INICIO",

                lambda *_:
                self.pantalla_inicio(),

                dp(52),

                False
            )
        )

        s.agregar(
            acciones
        )

        self.sm.current = "cuadro"

    # ========================================================
    # CAMPEÓN
    # ========================================================

    def mostrar_campeon(self):

        s = self.campeon_screen

        s.limpiar()

        s.agregar(
            Widget(
                size_hint_y=1
            )
        )

        s.agregar(
            etiqueta(
                "🏆",
                55,
                AMARILLO,
                dp(80)
            )
        )

        s.agregar(
            etiqueta(
                "CAMPEÓN",
                36,
                AMARILLO,
                dp(60)
            )
        )

        s.agregar(
            etiqueta(
                self.competencia[
                    "campeon"
                ] or "",

                30,

                BLANCO,

                dp(70)
            )
        )

        s.agregar(
            etiqueta(

                f"{self.competencia['nombre']}  •  "
                f"{self.competencia['fecha']}",

                14,

                (
                    0.65,
                    0.65,
                    0.65,
                    1
                ),

                dp(45)
            )
        )

        s.agregar(
            Widget(
                size_hint_y=1
            )
        )

        s.agregar(

            boton(

                "VOLVER AL INICIO",

                lambda *_:
                self.pantalla_inicio(),

                dp(58),

                True
            )
        )

        self.sm.current = "campeon"

    # ========================================================
    # COMPETENCIAS GUARDADAS
    # ========================================================

    def mostrar_competencias(self):

        s = self.guardadas

        s.limpiar()

        s.agregar(

            etiqueta(

                "COMPETENCIAS GUARDADAS",

                28,

                AMARILLO,

                dp(60)
            )
        )

        lista = (
            self.cargar_competencias()
        )

        scroll = ScrollView(
            size_hint_y=1
        )

        contenido = BoxLayout(

            orientation="vertical",

            spacing=dp(8),

            padding=[
                dp(8),
                dp(8)
            ],

            size_hint_y=None
        )

        contenido.bind(

            minimum_height=
            contenido.setter(
                "height"
            )
        )

        if not lista:

            contenido.add_widget(

                etiqueta(

                    "No hay competencias guardadas.",

                    15,

                    (
                        0.55,
                        0.55,
                        0.55,
                        1
                    ),

                    dp(50)
                )
            )

        else:

            for item in reversed(lista):

                campeon = (
                    item.get(
                        "campeon"
                    )
                    or
                    "En curso"
                )

                texto = (

                    f"{item.get('nombre', 'Sin nombre')}\n"

                    f"Fecha: "
                    f"{item.get('fecha', '-')}\n"

                    f"Competidores: "
                    f"{len(item.get('competidores', []))}\n"

                    f"Campeón: "
                    f"{campeon}"
                )

                contenido.add_widget(

                    Label(

                        text=texto,

                        font_size=dp(14),

                        color=BLANCO,

                        halign="left",

                        valign="middle",

                        size_hint_y=None,

                        height=dp(92)
                    )
                )

        scroll.add_widget(
            contenido
        )

        s.agregar(
            scroll
        )

        s.agregar(

            boton(

                "VOLVER",

                lambda *_:
                self.pantalla_inicio(),

                dp(55),

                False
            )
        )

        self.sm.current = "guardadas"


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":

    ArgentumApp().run()

