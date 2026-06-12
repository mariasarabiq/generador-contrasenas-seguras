Característica: Generador y Validador de Contraseñas Seguras
  Como usuario del portal de seguridad
  Quiero generar contraseñas seguras a partir de una palabra base y validar mis contraseñas actuales
  Para proteger mis cuentas y complicar la tarea a los atacantes

  Escenario: Generar opciones de contraseñas seguras omitiendo espacios en blanco
    Dado que el usuario se encuentra en la sección "Generador de Contraseñas Seguras"
    Cuando introduce la frase "la maria" en la caja de texto principal
    Y hace clic en el botón "Generar opciones"
    Entonces el sistema debe eliminar los espacios para procesar la palabra como "lamaria"
    Y el sistema debe generar 3 opciones de contraseña
    Y cada opción debe contener al menos 12 caracteres
    Y cada opción debe incluir una mezcla de letras mayúsculas, minúsculas, números y símbolos

  Escenario: Intento de generar contraseñas dejando el campo vacío
    Dado que el usuario se encuentra en la sección "Generador de Contraseñas Seguras"
    Cuando el usuario deja la caja de texto en blanco o solo contiene espacios
    Y hace clic en el botón "Generar opciones"
    Entonces el sistema debe mostrar una advertencia con el mensaje "Por favor, escribe una palabra válida."

  Escenario: Validar una contraseña que cumple con todos los requisitos
    Dado que el usuario se encuentra en la sección "Analizador y Validador de Contraseñas"
    Cuando introduce la contraseña "M@r1p0s4_9xZ"
    Y hace clic en el botón "Evaluar contraseña"
    Entonces el sistema debe mostrar un mensaje de éxito indicando que la contraseña es segura
    Y confirmar que cumple con todos los requisitos establecidos

  Escenario: Validar una contraseña débil o predecible
    Dado que el usuario se encuentra en la sección "Analizador y Validador de Contraseñas"
    Cuando introduce la contraseña "password12"
    Y hace clic en el botón "Evaluar contraseña"
    Entonces el sistema debe indicar que la contraseña no es completamente segura
    Y el sistema debe listar como faltantes: "Incluir al menos una letra mayúscula (A-Z)"
    Y "Incluir al menos un símbolo especial (!, @, #, $, %, etc.)"
    Y "Evitar el uso de palabras comunes u obvias como 'password'"
