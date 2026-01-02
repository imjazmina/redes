#pequenas validaciones comunes
def validar_mensaje(mensaje: str) -> bool:#devuelve un valor booleano
    if mensaje is None:
        return False
    mensaje = mensaje.strip()#elimina espacios en blanco al inicio y al final

    return mensaje != "" and len(mensaje) <= 256 #256 caracteres maximo porque es un chat simple

def formatear_mensaje(direccion: tuple, mensaje: str) -> str:
    return f"{direccion[0]}:{direccion[1]} dice: {mensaje}"