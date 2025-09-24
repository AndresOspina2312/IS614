import sys

from parser import parsear_linea
from pseudo import expandir_pseudo
from encoder import codificar
from errors import EnsambladorError

# Primera pasada: construir tabla de símbolos
def primera_pasada(lineas):
    """
    Recorre las lineas y construye la tabla de símbolos (etiqueta -> direccion).
    Cada instrucción base ocupara 4 bytes.
    NOTA: si una seudoinstrucción se expande a múltiples instrucciones
    (si expandir_pseudo devuelve una lista), también contamos todas ellas.
    """
    tabla_simbolos = {}
    pc = 0  # contador de lugar (dirección simulada)

    for lineno, linea in enumerate(lineas, start=1):
        nodo = parsear_linea(linea)
        if nodo is None:
            continue

        # Si hay etiqueta, la asociamos a la dirección actual
        if nodo.get("etiqueta"):
            etiqueta = nodo["etiqueta"]
            if etiqueta in tabla_simbolos:
                raise EnsambladorError(f"L{lineno}: etiqueta duplicada '{etiqueta}'")
            tabla_simbolos[etiqueta] = pc

        # Si la línea contiene instrucción, contamos cuántas instrucciones
        instr = nodo.get("instruccion")
        if not instr:
            continue

        # Preguntar a pseudo si la instrucción se expande
        expand = expandir_pseudo(instr, nodo.get("operandos", []))
        # expandir_pseudo puede devolver:
        #  - (instr_real, operandos_real)  -> contamos 1 instrucción
        #  - [ (instr1, ops1), (instr2, ops2), ... ] -> contamos len(lista)
        if isinstance(expand, list):
            cuenta = len(expand)
        else:
            cuenta = 1

        pc += 4 * cuenta

    return tabla_simbolos

# Segunda pasada: codificar
def segunda_pasada(lineas, tabla_simbolos):
    """
    Recorre las líneas, expande seudoinstrucciones, codifica cada instrucción
    usando encoder.codificar(...) y devuelve listas de binarios y hexadecimales.
    """
    binarios = []
    hexadecimales = []
    pc = 0  # contador (dirección) usado para calcular offsets relativos

    for lineno, linea in enumerate(lineas, start=1):
        nodo = parsear_linea(linea)
        if nodo is None:
            continue

        # Si solo hay etiqueta y nada más, continuar
        if nodo.get("instruccion") is None:
            continue

        instr = nodo["instruccion"]
        operandos = nodo.get("operandos", [])

        # Expandir seudoinstrucción (puede devolver un tuple o una lista de tuples)
        expand = expandir_pseudo(instr, operandos)

        expansiones = []
        if isinstance(expand, list):
            # lista de (instr_real, operandos_real)
            expansiones = expand
        else:
            # single (instr_real, operandos_real)
            instr_real, operandos_real = expand
            expansiones = [(instr_real, operandos_real)]

        # Codificar cada instrucción resultante de la expansión
        for instr_real, operandos_real in expansiones:
            try:
                binario, hexa = codificar(instr_real, operandos_real, tabla_simbolos, pc)
            except EnsambladorError as e:
                # Añadir contexto de línea para el usuario
                raise EnsambladorError(f"L{lineno}: {str(e)}") from e

            # Validar longitud de binario
            if len(binario) != 32:
                raise EnsambladorError(f"L{lineno}: codificación inválida (no son 32 bits): {binario}")

            binarios.append(binario)
            hexadecimales.append(hexa)
            pc += 4

    return binarios, hexadecimales


# Escritura de archivos de salida
def escribir_salidas(nombre_hex, nombre_bin, lista_hex, lista_bin):
    with open(nombre_hex, "w") as fh:
        for linea in lista_hex:
            fh.write(linea + "\n")

    with open(nombre_bin, "w") as fb:
        for linea in lista_bin:
            fb.write(linea + "\n")


# Programa principal
def main():
    if len(sys.argv) != 4:
        print("Uso: python assembler.py entrada.asm salida.hex salida.bin")
        sys.exit(1)

    archivo_entrada = sys.argv[1]
    archivo_hex = sys.argv[2]
    archivo_bin = sys.argv[3]

    try:
        with open(archivo_entrada, "r", encoding="utf-8") as f:
            lineas = f.readlines()
    except FileNotFoundError:
        print(f"Error: no se encontró el archivo de entrada '{archivo_entrada}'")
        sys.exit(1)

    try:
        # Primera pasada: construir tabla de símbolos
        tabla_simbolos = primera_pasada(lineas)

        # Segunda pasada: generar código máquina
        lista_binarios, lista_hexadecimales = segunda_pasada(lineas, tabla_simbolos)

        # Escribir archivos
        escribir_salidas(archivo_hex, archivo_bin, lista_hexadecimales, lista_binarios)

        print("✅ Ensamblado completado con éxito.")
        print(f"  Instrucciones ensambladas: {len(lista_binarios)}")
        print(f"  Salida hex: {archivo_hex}")
        print(f"  Salida bin: {archivo_bin}")

    except EnsambladorError as e:
        print("❌ Error en ensamblado:", e)
        sys.exit(1)
    except Exception as e:
        # Errores inesperados
        print("❌ Error inesperado:", repr(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
