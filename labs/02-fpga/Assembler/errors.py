class EnsambladorError(Exception):
    """Error general del ensamblador"""
    pass

class SintaxisError(EnsambladorError):
    """Error de sintaxis"""
    pass

class InstruccionInvalida(EnsambladorError):
    """Error por instrucción desconocida"""
    pass

class OperandoInvalido(EnsambladorError):
    """Error por operandos incorrectos"""
    pass

class EtiquetaNoDefinida(EnsambladorError):
    """Error por etiqueta no definida"""
    pass

class InmediatoFueraDeRango(EnsambladorError):
    """Error por inmediatos inválidos"""
    pass
