import random
import re
import string
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

SUSTITUCIONES = {
    "a": ["4", "@"], "e": ["3", "3"], "i": ["1", "!"],
    "o": ["0", "*"], "u": ["μ", "v"], "s": ["5", "$"], "t": ["7", "+"],
}

def transformar_palabra(palabra):
    resultado = ""
    for letra in palabra:
        letra_min = letra.lower()
        if letra_min in SUSTITUCIONES and random.random() > 0.3:
            resultado += random.choice(SUSTITUCIONES[letra_min])
        else:
            resultado += letra.upper() if random.random() > 0.5 else letra.lower()
    return resultado

@app.route('/')
def index():
    # Sirve la página web HTML
    return render_template('index.html')

@app.route('/generar', methods=['POST'])
def generar():
    datos = request.json
    palabra_usuario = datos.get('palabra', '')
    
    lista_palabras = palabra_usuario.strip().split()
    cantidad_palabras = len(lista_palabras)
    
    if cantidad_palabras == 0:
        return jsonify({"error": "Por favor, escribe una palabra válida."}), 400
    if cantidad_palabras > 50:
        return jsonify({"error": f"Has ingresado {cantidad_palabras} palabras. El límite es de 50."}), 400

    palabra_limpia = palabra_usuario.strip().replace(" ", "")
    opciones = []
    mayusculas = string.ascii_uppercase
    minusculas = string.ascii_lowercase
    numeros = string.digits
    simbolos = "!,@,#,$,%,&,*_?¿¡"

    for _ in range(3):
        base_segura = transformar_palabra(palabra_limpia)
        if len(base_segura) > 8:
            base_segura = base_segura[:8]

        relleno = [
            random.choice(mayusculas), random.choice(minusculas),
            random.choice(numeros), random.choice(simbolos),
        ]

        caracteres_faltantes = 12 - (len(base_segura) + len(relleno))
        if caracteres_faltantes > 0:
            todos_los_caracteres = mayusculas + minusculas + numeros + simbolos
            relleno += random.choices(todos_los_caracteres, k=caracteres_faltantes)

        random.shuffle(relleno)
        contrasena_final = base_segura + "".join(relleno)
        opciones.append(contrasena_final)

    return jsonify({"opciones": opciones})

@app.route('/validar', methods=['POST'])
def validar():
    datos = request.json
    contrasena = datos.get('contrasena', '')
    
    palabras_prohibidas = ["password", "contraseña", "123456", "qwerty", "admin"]
    palabras_ok = False
    if contrasena:
        palabras_ok = not any(p in contrasena.lower() for p in palabras_prohibidas)

    resultados = {
        "longitud": len(contrasena) >= 12,
        "mayuscula": bool(re.search(r"[A-Z]", contrasena)),
        "minuscula": bool(re.search(r"[a-z]", contrasena)),
        "numero": bool(re.search(r"[0-9]", contrasena)),
        "simbolo": bool(re.search(r"[!,@,#,$,%,&,*_?¿¡]", contrasena)),
        "palabras": palabras_ok if contrasena else False
    }
    
    es_valida = all(resultados.values())
    resultados["es_valida"] = es_valida
    
    return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True)
