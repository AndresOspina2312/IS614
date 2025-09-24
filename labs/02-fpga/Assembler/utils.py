# Diccionario de registros
registros = {
    f"x{i}": i for i in range(32)
}
# Alias comunes
registros.update({
    "zero": 0, "ra": 1, "sp": 2, "gp": 3, "tp": 4,
    "t0": 5, "t1": 6, "t2": 7,
    "s0": 8, "fp": 8, "s1": 9,
    "a0": 10, "a1": 11, "a2": 12, "a3": 13,
    "a4": 14, "a5": 15, "a6": 16, "a7": 17,
    "s2": 18, "s3": 19, "s4": 20, "s5": 21,
    "s6": 22, "s7": 23, "s8": 24, "s9": 25,
    "s10": 26, "s11": 27,
    "t3": 28, "t4": 29, "t5": 30, "t6": 31
})

# Tabla de instrucciones base
instrucciones_base = {
    # INSTRUCCIONES R
    "add":  {"tipo": "R", "funct3": 0x0, "funct7": 0x00, "opcode": 0x33},
    "sub":  {"tipo": "R", "funct3": 0x0, "funct7": 0x20, "opcode": 0x33},
    "sll":  {"tipo": "R", "funct3": 0x1, "funct7": 0x00, "opcode": 0x33},
    "slt":  {"tipo": "R", "funct3": 0x2, "funct7": 0x00, "opcode": 0x33},
    "sltu": {"tipo": "R", "funct3": 0x3, "funct7": 0x00, "opcode": 0x33},
    "xor":  {"tipo": "R", "funct3": 0x4, "funct7": 0x00, "opcode": 0x33},
    "srl":  {"tipo": "R", "funct3": 0x5, "funct7": 0x00, "opcode": 0x33},
    "sra":  {"tipo": "R", "funct3": 0x5, "funct7": 0x20, "opcode": 0x33},
    "or":   {"tipo": "R", "funct3": 0x6, "funct7": 0x00, "opcode": 0x33},
    "and":  {"tipo": "R", "funct3": 0x7, "funct7": 0x00, "opcode": 0x33},

    # INSTRUCCIONES I 
    "addi": {"tipo": "I", "funct3": 0x0, "opcode": 0x13},
    "slti": {"tipo": "I", "funct3": 0x2, "opcode": 0x13},
    "sltiu":{"tipo": "I", "funct3": 0x3, "opcode": 0x13},
    "xori": {"tipo": "I", "funct3": 0x4, "opcode": 0x13},
    "ori":  {"tipo": "I", "funct3": 0x6, "opcode": 0x13},
    "andi": {"tipo": "I", "funct3": 0x7, "opcode": 0x13},

    # Cargas
    "lb":   {"tipo": "I", "funct3": 0x0, "opcode": 0x03},
    "lh":   {"tipo": "I", "funct3": 0x1, "opcode": 0x03},
    "lw":   {"tipo": "I", "funct3": 0x2, "opcode": 0x03},
    "lbu":  {"tipo": "I", "funct3": 0x4, "opcode": 0x03},
    "lhu":  {"tipo": "I", "funct3": 0x5, "opcode": 0x03},

    # saltos relativos
    "jalr": {"tipo": "I", "funct3": 0x0, "opcode": 0x67},

    # INSTRUCCIONES S
    "sb":   {"tipo": "S", "funct3": 0x0, "opcode": 0x23},
    "sh":   {"tipo": "S", "funct3": 0x1, "opcode": 0x23},
    "sw":   {"tipo": "S", "funct3": 0x2, "opcode": 0x23},

    # INSTRUCCIONES B
    "beq":  {"tipo": "B", "funct3": 0x0, "opcode": 0x63},
    "bne":  {"tipo": "B", "funct3": 0x1, "opcode": 0x63},
    "blt":  {"tipo": "B", "funct3": 0x4, "opcode": 0x63},
    "bge":  {"tipo": "B", "funct3": 0x5, "opcode": 0x63},
    "bltu": {"tipo": "B", "funct3": 0x6, "opcode": 0x63},
    "bgeu": {"tipo": "B", "funct3": 0x7, "opcode": 0x63},

    # INSTRUCCIONES U
    "lui":  {"tipo": "U", "opcode": 0x37},
    "auipc":{"tipo": "U", "opcode": 0x17},

    # INSTRUCCIONES J
    "jal":  {"tipo": "J", "opcode": 0x6F},

    # ----- Pseudoinstrucciones -----
    "nop":  {"tipo": "PSEUDO"},
}

# Funciones auxiliares
def a_binario(valor, bits):
    """Convierte un entero a binario con signo y longitud fija."""
    if valor < 0:
        valor = (1 << bits) + valor
    return format(valor & ((1 << bits) - 1), f"0{bits}b")

def a_hexadecimal(bin_str):
    """Convierte binario a hexadecimal de 8 dígitos (32 bits)."""
    return format(int(bin_str, 2), "08x")
