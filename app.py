"""La torre del último faro: aventura de texto para Streamlit."""

import random

import streamlit as st


st.set_page_config(page_title="La torre del último faro", page_icon="🗝️")

st.markdown(
    """
    <style>
    .stApp { background: #101713; color: #c9f5bf; }
    h1, h2, h3, p, button { font-family: monospace !important; }
    h1, h2, h3 { color: #a8f095 !important; }
    [data-testid="stSidebar"] { background: #17221a; }
    </style>
    """,
    unsafe_allow_html=True,
)


SCENES = {
    "plaza": {
        "title": "I. La última campanada",
        "text": (
            "Año 1986, en un reino que nunca conoció la electricidad. "
            "El faro de la torre se ha apagado. Si no lo enciendes antes del alba, "
            "las sombras llegarán al pueblo. Una anciana te ofrece una llave oxidada."
        ),
        "choices": [
            ("Aceptar la llave y entrar al bosque", "bosque", "llave", 0),
            ("Rechazarla y tomar el camino del río", "rio", None, 0),
        ],
    },
    "bosque": {
        "title": "II. El bosque que escucha",
        "text": (
            "Los árboles repiten tu nombre. Entre las raíces hay una espada vieja; "
            "a lo lejos brilla la ventana de una ermita."
        ),
        "choices": [
            ("Recoger la espada y seguir hacia la torre", "puerta", "espada", 0),
            ("Buscar ayuda en la ermita", "ermita", None, 0),
        ],
    },
    "rio": {
        "title": "II. El barquero",
        "text": (
            "Un barquero sin rostro pide un recuerdo como pago. También ves un "
            "puente roto que quizá puedas cruzar de un salto."
        ),
        "choices": [
            ("Entregar un recuerdo al barquero", "orilla", "moneda", 0),
            ("Saltar el puente roto (pierdes 1 vida)", "orilla", None, -1),
        ],
    },
    "ermita": {
        "title": "III. La ermita vacía",
        "text": (
            "Sobre el altar descansa una lámpara de aceite azul. Una inscripción dice: "
            "'La luz recuerda lo que el hierro olvida'."
        ),
        "choices": [
            ("Tomar la lámpara y subir a la torre", "puerta", "lampara", 0),
            ("Dejar el altar intacto y subir", "puerta", None, 0),
        ],
    },
    "orilla": {
        "title": "III. La otra orilla",
        "text": (
            "Has llegado al pie de la torre. Un mercader dormido dejó una lámpara "
            "encendida junto al sendero. El amanecer está cerca."
        ),
        "choices": [
            ("Llevar la lámpara a la torre", "puerta", "lampara", 0),
            ("No tocar sus cosas y subir", "puerta", None, 0),
        ],
    },
    "puerta": {
        "title": "IV. El guardián de piedra",
        "text": (
            "La puerta está sellada. Un guardián despierta y extiende la mano: "
            "'Muéstrame por qué mereces pasar'."
        ),
        "choices": [
            ("Abrir la cerradura con la llave", "biblioteca", "use_llave", 0),
            ("Mostrar la moneda del barquero", "biblioteca", "use_moneda", 0),
            ("Enfrentar al guardián con la espada", "combate", "use_espada", 0),
            ("Forzar la puerta (pierdes 1 vida)", "biblioteca", None, -1),
        ],
    },
    "combate": {
        "title": "V. La prueba del hierro",
        "text": (
            "La espada choca contra la piedra. El guardián se tambalea, pero un "
            "golpe más decidirá el combate. Lanza un dado de seis caras."
        ),
        "choices": [],
    },
    "biblioteca": {
        "title": "V. Los libros sin nombres",
        "text": (
            "Una página abierta revela el secreto: el faro necesita una llama y "
            "una promesa sincera. Un pasillo conduce a la cima; otro baja a una cripta."
        ),
        "choices": [
            ("Subir directamente al faro", "faro", None, 0),
            ("Explorar la cripta primero", "cripta", None, 0),
        ],
    },
    "cripta": {
        "title": "VI. La cripta",
        "text": (
            "En la oscuridad, una voz te ofrece poder a cambio de abandonar "
            "el pueblo. Cerca de la salida encuentras un frasco de luz curativa."
        ),
        "choices": [
            ("Rechazar la voz y beber el frasco (+1 vida)", "faro", None, 1),
            ("Aceptar el pacto de la sombra", "final_sombra", None, 0),
        ],
    },
    "faro": {
        "title": "VII. Antes del alba",
        "text": (
            "El cristal del faro está frío. Abajo, las primeras sombras rozan "
            "los tejados. La torre tiembla mientras decides qué hacer."
        ),
        "choices": [
            ("Encender el faro con la lámpara", "final_luz", "use_lampara", 0),
            ("Romper el cristal y dejar entrar el amanecer", "final_sacrificio", None, -1),
            ("Huir por las escaleras", "final_huida", None, 0),
        ],
    },
    "final_luz": {
        "title": "FINAL: El guardián del alba",
        "text": (
            "Prometes proteger a quienes quedaron atrás. La llama azul despierta "
            "el faro y las sombras retroceden. El pueblo te recordará durante años."
        ),
        "choices": [],
    },
    "final_sacrificio": {
        "title": "FINAL: La luz que costó caro",
        "text": (
            "El cristal estalla y el primer rayo de sol atraviesa la torre. "
            "Las sombras huyen. Has salvado al pueblo, aunque nadie sabrá "
            "cuánto te costó."
        ),
        "choices": [],
    },
    "final_sombra": {
        "title": "FINAL: Señor de la torre",
        "text": (
            "La sombra te concede su poder. El faro arde con fuego negro; "
            "el pueblo sobrevive, pero ahora te teme más que a la noche."
        ),
        "choices": [],
    },
    "final_huida": {
        "title": "FINAL: El camino de regreso",
        "text": (
            "Abandonas la torre. Al salir el sol, ves el pueblo cubierto de "
            "niebla. Sigues con vida, pero tendrás que vivir con tu decisión."
        ),
        "choices": [],
    },
    "final_derrota": {
        "title": "FINAL: La noche eterna",
        "text": (
            "Caes antes de alcanzar el faro. En la distancia suena la última "
            "campanada del pueblo. Tal vez otro aventurero lo consiga."
        ),
        "choices": [],
    },
}

REQUIRED_ITEMS = {
    "use_llave": "llave",
    "use_moneda": "moneda",
    "use_espada": "espada",
    "use_lampara": "lampara",
}

ITEM_NAMES = {
    "llave": "llave oxidada",
    "moneda": "moneda del barquero",
    "espada": "espada vieja",
    "lampara": "lámpara azul",
}


def restart():
    st.session_state.scene = "plaza"
    st.session_state.health = 3
    st.session_state.inventory = set()
    st.session_state.history = []
    st.session_state.notice = ""


def choose(label, destination, effect, health_change):
    """Aplica una decisión cuando el jugador pulsa un botón."""
    st.session_state.history.append(label)

    if effect in ITEM_NAMES:
        st.session_state.inventory.add(effect)
        st.session_state.notice = f"Has obtenido: {ITEM_NAMES[effect]}."
    else:
        st.session_state.notice = ""

    st.session_state.health = min(3, st.session_state.health + health_change)

    if st.session_state.health <= 0:
        st.session_state.scene = "final_derrota"
    else:
        st.session_state.scene = destination


def roll_die():
    result = random.randint(1, 6)
    st.session_state.history.append(f"Lanzar dado: {result}")

    if result >= 3:
        st.session_state.scene = "biblioteca"
        st.session_state.notice = f"Sacaste {result}. ¡Venciste al guardián!"
    else:
        st.session_state.health -= 1

        if st.session_state.health <= 0:
            st.session_state.scene = "final_derrota"
        else:
            st.session_state.scene = "biblioteca"

        st.session_state.notice = (
            f"Sacaste {result}. Pasaste, pero perdiste 1 vida."
        )


if "scene" not in st.session_state:
    restart()


st.title("🗝️ LA TORRE DEL ÚLTIMO FARO")
st.caption("Una aventura de texto al estilo de los juegos de rol de los 80")

with st.sidebar:
    st.header("HOJA DE PERSONAJE")
    st.write(f"❤️ Vida: {st.session_state.health}/3")

    items = [
        ITEM_NAMES[item]
        for item in sorted(st.session_state.inventory)
    ]
    st.write("🎒 Inventario: " + (", ".join(items) if items else "vacío"))
    st.write(f"📜 Decisiones: {len(st.session_state.history)}")

    if st.session_state.history:
        with st.expander("Ver decisiones anteriores"):
            for number, decision in enumerate(st.session_state.history, 1):
                st.write(f"{number}. {decision}")

    st.button("Empezar de nuevo", on_click=restart)


scene = SCENES[st.session_state.scene]

st.header(scene["title"])
st.write(scene["text"])

if st.session_state.notice:
    st.info(st.session_state.notice)

if st.session_state.scene == "combate":
    st.button(
        "🎲 Lanzar dado",
        on_click=roll_die,
        type="primary",
    )

elif st.session_state.scene.startswith("final_"):
    st.success(
        "Fin de la aventura. Puedes jugar otra vez para descubrir otro final."
    )
    st.button(
        "↻ Jugar otra vez",
        on_click=restart,
        type="primary",
    )

else:
    st.subheader("¿Qué haces?")

    for number, (label, destination, effect, health_change) in enumerate(
        scene["choices"]
    ):
        required = REQUIRED_ITEMS.get(effect)

        if required is None or required in st.session_state.inventory:
            st.button(
                label,
                key=f"{st.session_state.scene}_{number}",
                on_click=choose,
                args=(label, destination, effect, health_change),
                use_container_width=True,
            )
