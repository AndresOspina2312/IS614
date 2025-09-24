from utils import a_binario, a_hexadecimal, registros, instrucciones_base
from errors import EnsambladorError

def codificar(instr, operandos, tabla_simbolos, pc):
    """
    Recibe:
      - instr: nombre de la instrucción
      - operandos: lista de registros/inmediatos/etiquetas
      - tabla_simbolos: diccionario de etiquetas -> direcciones
      - pc: contador actual
    Devuelve (binario, hexadecimal)
    """
    if instr not in instrucciones_base:
        raise EnsambladorError(f"Instrucción desconocida: {instr}")

    info = instrucciones_base[instr]

    #INSTRUCCIONES R
    if info["tipo"] == "R":
        rd = registros[operandos[0]]
        rs1 = registros[operandos[1]]
        rs2 = registros[operandos[2]]
        funct7 = a_binario(info["funct7"], 7)
        rs2_b = a_binario(rs2, 5)
        rs1_b = a_binario(rs1, 5)
        funct3 = a_binario(info["funct3"], 3)
        rd_b = a_binario(rd, 5)
        opcode = a_binario(info["opcode"], 7)
        binario = funct7 + rs2_b + rs1_b + funct3 + rd_b + opcode

    #INSTRUCCIONES I
    elif info["tipo"] == "I":
        rd = registros[operandos[0]]
        rs1 = registros[operandos[1]]
        inmediato = int(operandos[2], 0)

        if not -2048 <= inmediato <= 2047:
            raise EnsambladorError(f"Immediate out of range (-2048 to 2047): {inmediato}")

        imm_b = a_binario(inmediato, 12)
        rs1_b = a_binario(rs1, 5)
        funct3 = a_binario(info["funct3"], 3)
        rd_b = a_binario(rd, 5)
        opcode = a_binario(info["opcode"], 7)
        binario = imm_b + rs1_b + funct3 + rd_b + opcode

    #INSTRUCCIONES S
    elif info["tipo"] == "S":
        rs2 = registros[operandos[0]]
        inmediato = int(operandos[1], 0)
        rs1 = registros[operandos[2]]
        imm_b = a_binario(inmediato, 12)
        imm_hi = imm_b[:7]
        imm_lo = imm_b[7:]
        rs2_b = a_binario(rs2, 5)
        rs1_b = a_binario(rs1, 5)
        funct3 = a_binario(info["funct3"], 3)
        opcode = a_binario(info["opcode"], 7)
        binario = imm_hi + rs2_b + rs1_b + funct3 + imm_lo + opcode

    #INSTRUCCIONES B
    elif info["tipo"] == "B":
        rs1 = registros[operandos[0]]
        rs2 = registros[operandos[1]]
        etiqueta = operandos[2]
        if etiqueta not in tabla_simbolos:
            raise EnsambladorError(f"Etiqueta no definida: {etiqueta}")
        direccion = tabla_simbolos[etiqueta]
        offset = direccion - pc
        imm_b = a_binario(offset, 13)
        imm12 = imm_b[0]
        imm10_5 = imm_b[2:8]
        imm4_1 = imm_b[8:12]
        imm11 = imm_b[1]
        rs1_b = a_binario(rs1, 5)
        rs2_b = a_binario(rs2, 5)
        funct3 = a_binario(info["funct3"], 3)
        opcode = a_binario(info["opcode"], 7)
        binario = imm12 + imm10_5 + rs2_b + rs1_b + funct3 + imm4_1 + imm11 + opcode

    #INSTRUCCIONES U
    elif info["tipo"] == "U":
        rd = registros[operandos[0]]
        inmediato = int(operandos[1], 0)
        imm_b = a_binario(inmediato, 20)
        rd_b = a_binario(rd, 5)
        opcode = a_binario(info["opcode"], 7)
        binario = imm_b + rd_b + opcode

    #INSTRUCCIONES J
    elif info["tipo"] == "J":
        rd = registros[operandos[0]]
        etiqueta = operandos[1]
        if etiqueta not in tabla_simbolos:
            raise EnsambladorError(f"Etiqueta no definida: {etiqueta}")
        direccion = tabla_simbolos[etiqueta]
        offset = direccion - pc
        imm_b = a_binario(offset, 21)
        imm20 = imm_b[0]
        imm10_1 = imm_b[10:20]
        imm11 = imm_b[9]
        imm19_12 = imm_b[1:9]
        rd_b = a_binario(rd, 5)
        opcode = a_binario(info["opcode"], 7)
        binario = imm20 + imm19_12 + imm11 + imm10_1 + rd_b + opcode

    else:
        raise EnsambladorError(f"Formato no soportado: {info['tipo']}")

    return binario, a_hexadecimal(binario)
