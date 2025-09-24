def expandir_pseudo(instr, operandos):
    """
    Devuelve (instruccion_real, operandos_reales).
    """
    if instr == "nop":
        return "addi", ["x0", "x0", "0"]

    if instr == "mv":
        # mv rd, rs -> addi rd, rs, 0
        return "addi", [operandos[0], operandos[1], "0"]

    if instr == "neg":
        # neg rd, rs -> sub rd, x0, rs
        return "sub", [operandos[0], "x0", operandos[1]]

    # Si no es pseudo, devolver igual
    return instr, operandos
