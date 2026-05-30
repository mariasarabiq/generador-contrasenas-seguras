import random
import re
import string
import streamlit as st

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
            # Elige una sustitución aleatoria
            resultado += random.choice(SUSTITUCIONES[letra_min])
        else:
            # Alterna mayúsculas y minúsculas aleatoriamente
            resultado += (
                letra.upper() if random.random() > 0.5 else letra.lower()
            )
    return resultado


def generar_contrasenas(palabra_base):
    """Genera 3 opciones de contraseñas seguras basadas en una palabra."""
    opciones = []

    # Caracteres para rellenar y asegurar la complejidad
    mayusculas = string.ascii_uppercase
    minusculas = string.ascii_lowercase
    numeros = string.digits
    simbolos = "!,@,#,$,%,&,*_?¿¡"

    for _ in range(3):
        # Primero transformamos la palabra del usuario
        base_segura = transformar_palabra(palabra_base)

        # Añadimos caracteres obligatorios para asegurar que cumpla los requisitos
        relleno = [
            random.choice(mayusculas),
            random.choice(minusculas),
            random.choice(numeros),
            random.choice(simbolos),
        ]

        # Si aún no llega a 12 caracteres, agregamos más caracteres aleatorios
        longitud_actual = len(base_segura) + len(relleno)
        if longitud_actual < 12:
            todos_los_caracteres = mayusculas + minusculas + numeros + simbolos
            relleno += random.choices(
                todos_los_caracteres, k=(12 - longitud_actual)
            )

        # Mezclamos el relleno para que no queden siempre al final
        random.shuffle(relleno)

        # Combinamos la palabra transformada con el relleno
        contrasena_final = base_segura + "".join(relleno)
        opciones.append(contrasena_final)

    return opciones


def evaluar_contrasena(contrasena):
    """Evalúa la contraseña y devuelve una lista de los requisitos faltantes."""
    faltantes = []

    # 1. Validación de longitud
    if len(contrasena) < 12:
        faltantes.append(
            "Tener al menos 12 caracteres (longitud actual: {}).".format(
                len(contrasena)
            )
        )

    # 2. Validación de mayúsculas
    if not re.search(r"[A-Z]", contrasena):
        faltantes.append("Incluir al menos una letra mayúscula (A-Z).")

    # 3. Validación de minúsculas
    if not re.search(r"[a-z]", contrasena):
        faltantes.append("Incluir al menos una letra minúscula (a-z).")

    # 4. Validación de números
    if not re.search(r"[0-9]", contrasena):
        faltantes.append("Incluir al menos un número (0-9).")

    # 5. Validación de símbolos
    if not re.search(r"[!,@,#,$,%,&,*_?¿¡]", contrasena):
        faltantes.append(
            "Incluir al menos un símbolo especial (!, @, #, $, %, etc.)."
        )

    # 6. Validación de palabras obvias o comunes
    palabras_prohibidas = ["password", "contraseña", "123456", "qwerty", "admin"]
    for palabra in palabras_prohibidas:
        if palabra in contrasena.lower():
            faltantes.append(
                f"Evitar el uso de palabras comunes u obvias como '{palabra}'."
            )
            break

    return faltantes


# --- Interfaz Web con Streamlit ---
st.title("Programa de contraseña segura")
st.write(
    "Este programa te ayuda a generar contraseñas seguras y a verificar el nivel de seguridad de tus contraseñas actuales."
)

st.markdown("---")

# Sección 1: Generador de contraseñas
st.header("Generador de contraseñas seguras")
palabra_usuario = st.text_input(
    "Introduce una palabra base (puede ser una palabra común, un nombre o un concepto):",
    placeholder="Ejemplo: caballo",
    key="entrada_palabra_base",
)

if palabra_usuario:
    palabra_limpia = palabra_usuario.strip()
    if len(palabra_limpia) == 0:
        st.warning("Por favor, escribe una palabra válida.")
    else:
        st.subheader("Tus 3 opciones sugeridas:")
        opciones_generadas = generar_contrasenas(palabra_limpia)

        # Usamos bloques de código estáticos para mostrar las contraseñas sin romper la reactividad
        for i, opcion in enumerate(opciones_generadas, 1):
            st.write(f"**Opción {i}:**")
            st.code(opcion, language="text")

st.markdown("---")

# Sección 2: Validador de contraseñas
st.header("Validador de contraseñas")
contrasena_a_probar = st.text_input(
    "Introduce la contraseña que deseas evaluar:",
    type="password",
    placeholder="Escribe tu contraseña aquí...",
    key="entrada_contrasena_evaluar",
)

if contrasena_a_probar:
    errores = evaluar_contrasena(contrasena_a_probar)

    if not errores:
        st.success(
            "¡Felicidades! La contraseña es segura y cumple con todos los requisitos establecidos."
        )
    else:
        st.error("La contraseña no es completamente segura.")
        st.write("Para cumplir con los requisitos, te hace falta lo siguiente:")
        for error in errores:
            st.write(f"❌ {error}")