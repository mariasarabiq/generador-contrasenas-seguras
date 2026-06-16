import random
import re
import string
import streamlit as st
from st_keyup import st_keyup

# Diccionario de sustituciones comunes para transformar palabras (Leet speak)
SUSTITUCIONES = {
    "a": ["4", "@"],
    "e": ["3", "3"],
    "i": ["1", "!"],
    "o": ["0", "*"],
    "u": ["μ", "v"],
    "s": ["5", "$"],
    "t": ["7", "+"],
}


def transformar_palabra(palabra):
    """Mezcla y reemplaza letras de una palabra con símbolos y números."""
    resultado = ""
    for letra in palabra:
        letra_min = letra.lower()
        if letra_min in SUSTITUCIONES and random.random() > 0.3:
            resultado += random.choice(SUSTITUCIONES[letra_min])
        else:
            resultado += (
                letra.upper() if random.random() > 0.5 else letra.lower()
            )
    return resultado


def generar_contrasenas(palabra_base):
    """Genera 3 opciones de contraseñas seguras basadas en una palabra."""
    opciones = []
    mayusculas = string.ascii_uppercase
    minusculas = string.ascii_lowercase
    numeros = string.digits
    simbolos = "!,@,#,$,%,&,*_?¿¡"

    for _ in range(3):
        base_segura = transformar_palabra(palabra_base)
        relleno = [
            random.choice(mayusculas),
            random.choice(minusculas),
            random.choice(numeros),
            random.choice(simbolos),
        ]

        longitud_actual = len(base_segura) + len(relleno)
        if longitud_actual < 12:
            todos_los_caracteres = mayusculas + minusculas + numeros + simbolos
            relleno += random.choices(
                todos_los_caracteres, k=(12 - longitud_actual)
            )

        random.shuffle(relleno)
        contrasena_final = base_segura + "".join(relleno)
        opciones.append(contrasena_final)

    return opciones


# --- Interfaz Web con Streamlit ---
st.title("🛡️ Portal de Seguridad: Contraseñas Seguras")
st.write(
    "Esta plataforma te ayuda a generar contraseñas robustas y a verificar el nivel de seguridad de tus claves actuales en tiempo real."
)

st.markdown("---")

# Sección 1: Generador de contraseñas
st.header("1. Generador de Contraseñas Seguras")
palabra_usuario = st.text_input(
    "Introduce una palabra base (puede ser una palabra común o nombre):",
    placeholder="Ejemplo: la maria",
    key="entrada_palabra_base",
)

boton_generar = st.button("Generar opciones")

if boton_generar:
    palabra_limpia = palabra_usuario.strip().replace(" ", "")
    
    if len(palabra_limpia) == 0:
        st.warning("Por favor, escribe una palabra válida.")
    else:
        st.subheader("Tus 3 opciones sugeridas:")
        opciones_generadas = generar_contrasenas(palabra_limpia)

        for i, opcion in enumerate(opciones_generadas, 1):
            st.write(f"**Opción {i}:**")
            st.code(opcion, language="text")

st.markdown("---")

# Sección 2: Validador de contraseñas reactivo
st.header("2. Analizador y Validador Reactivo en Vivo")

# IMPORTANTE: Usamos st_keyup para que reaccione instantáneamente con cada tecla
contrasena_a_probar = st_keyup(
    "Introduce la contraseña que deseas evaluar:",
    type="password",
    placeholder="Escribe tu contraseña aquí...",
    key="entrada_contrasena_evaluar",
)

# st_keyup devuelve 'None' si la caja está vacía. Lo forzamos a texto para evitar errores de lectura.
if contrasena_a_probar is None:
    contrasena_a_probar = ""

# Variables de estado para la reactividad
longitud_ok = len(contrasena_a_probar) >= 12
mayuscula_ok = bool(re.search(r"[A-Z]", contrasena_a_probar))
minuscula_ok = bool(re.search(r"[a-z]", contrasena_a_probar))
numero_ok = bool(re.search(r"[0-9]", contrasena_a_probar))
simbolo_ok = bool(re.search(r"[!,@,#,$,%,&,*_?¿¡]", contrasena_a_probar))

palabras_prohibidas = ["password", "contraseña", "123456", "qwerty", "admin"]
# Es válido si tiene texto y no contiene palabras prohibidas
palabras_ok = False
if contrasena_a_probar:
    palabras_ok = not any(p in contrasena_a_probar.lower() for p in palabras_prohibidas)

# Mostrar checklist en tiempo real
st.write("### Requisitos de seguridad:")
st.markdown(f"{'✅' if longitud_ok else '❌'} Tener al menos 12 caracteres.")
st.markdown(f"{'✅' if mayuscula_ok else '❌'} Incluir al menos una letra mayúscula (A-Z).")
st.markdown(f"{'✅' if minuscula_ok else '❌'} Incluir al menos una letra minúscula (a-z).")
st.markdown(f"{'✅' if numero_ok else '❌'} Incluir al menos un número (0-9).")
st.markdown(f"{'✅' if simbolo_ok else '❌'} Incluir al menos un símbolo especial (!, @, #, etc.).")
st.markdown(f"{'✅' if (contrasena_a_probar and palabras_ok) else '❌'} Evitar el uso de palabras comunes u obvias.")

# Condición global para habilitar el botón
es_valida = longitud_ok and mayuscula_ok and minuscula_ok and numero_ok and simbolo_ok and palabras_ok

# El botón usa 'disabled' para activarse solo cuando es_valida es True
boton_evaluar = st.button(
    "Confirmar y guardar contraseña", 
    disabled=not es_valida, 
    type="primary"
)

if boton_evaluar:
    st.success("¡Felicidades! Tu contraseña es completamente segura y ha sido validada.")
st.markdown("---")
st.write(
    "María Guadalupe Sarabia Velarde"
)

