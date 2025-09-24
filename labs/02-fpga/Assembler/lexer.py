import re

patrones = [
    ("COMENTARIO",   r"#.*"),
    ("DIRECTIVA",    r"\.(text|data)"),
    ("ETIQUETA",     r"[A-Za-z_]\w*:"),
    # Poner REGISTRO antes que INSTRUCCION
    ("REGISTRO",     r"(?:x(?:[0-9]|[12][0-9]|3[01])|zero|ra|sp|gp|tp|t[0-6]|s(?:[0-9]|1[01])|a[0-7]|fp)"),
    ("INSTRUCCION",  r"[A-Za-z.]+"),
    ("NUMERO",       r"-?(0x[0-9A-Fa-f]+|\d+)"),
    ("SEPARADOR",    r"[,\(\)]"),
    ("ESPACIO",      r"\s+"),
]

regex_master = re.compile("|".join(f"(?P<{nombre}>{patron})" for nombre, patron in patrones))

def lexer(linea):
    tokens = []
    for match in regex_master.finditer(linea):
        tipo = match.lastgroup
        valor = match.group()
        if tipo in ("ESPACIO", "COMENTARIO"):
            continue
        if tipo == "ETIQUETA":
            valor = valor[:-1]
        tokens.append((tipo, valor))
    return tokens

# Prueba rápida
if __name__ == "__main__":
    ejemplo = "addi x1, x2, 10"
    print(lexer(ejemplo))
