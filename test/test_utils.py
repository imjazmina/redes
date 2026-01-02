#test de funciones utils
import pytest
from utils import validar_mensaje, formatear_mensaje

#happy path
@pytest.mark.parametrize("mensaje", [
    "Hola mundo",
    "   Espacios al inicio y final   ",
    "123",
    "Mensaje con caracteres especiales !@#$%^&*()",
    "a" * 256  #mensaje de 256 caracteres
])

def test_mensaje_valido(mensaje):
    assert validar_mensaje(mensaje) is True


#sad path
@pytest.mark.parametrize("mensaje", [
    "",
    "    ",  
    None,
    "a" * 257  #a partir de 257 caracteres ya es invalido
])
def test_mensaje_invalido(mensaje):
    assert validar_mensaje(mensaje) is False

def test_formatear_mensaje():
    direccion = ("127.0.0.1", 8000)
    mensaje = "Hola"
    esperado = "127.0.0.1:8000 dice: Hola"

    assert formatear_mensaje(direccion, mensaje) == esperado

 