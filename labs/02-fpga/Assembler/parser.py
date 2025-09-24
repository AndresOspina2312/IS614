from lexer import lexer

def parsear_linea(linea):
    """
    Recibe una línea de código y devuelve un diccionario con:
      - etiqueta (opcional)
      - instruccion
      - operandos
    """
    tokens = lexer(linea)
    if not tokens:
        return None

    nodo = {"etiqueta": None, "instruccion": None, "operandos": []}

    # ¿Etiqueta al inicio?
    if tokens[0][0] == "ETIQUETA":
        nodo["etiqueta"] = tokens[0][1]
        tokens = tokens[1:]

    if not tokens:
        return nodo

    # Primera palabra = instrucción
    if tokens[0][0] == "INSTRUCCION":
        nodo["instruccion"] = tokens[0][1]
        tokens = tokens[1:]

    # El resto = operandos (omitimos separadores)
    for tipo, valor in tokens:
        if tipo not in ("SEPARADOR",):
            nodo["operandos"].append(valor)

    return nodo
