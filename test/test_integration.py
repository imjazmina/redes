import socket
import time
import pytest
import subprocess
import sys

HOST = "127.0.0.1"
PORT = 8000

#fixture = funcion que prepara entorno para test
@pytest.fixture(scope="module", autouse=True)# se ejecuta automaticamente 1 vez
def levantar_servidor():
    proceso = subprocess.Popen( #levanta el servidor
        [sys.executable, "server.py"],#ejecuta python server.py en segundo plano
        stdout=subprocess.DEVNULL,#no muestra salidas como print
        stderr=subprocess.DEVNULL# no muestra salidas de errores
    )

    time.sleep(1)  # tiempo para que levante el server

    yield  #marca que todo este listo para ejecuta los tests

    proceso.terminate()
    proceso.wait(timeout=2)#espera 2 seg para que el servidor cierre correctamente

def test_conexion_cliente_servidor():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((HOST, PORT))

    assert cliente.fileno() != -1 #verifica socket válido
    
    cliente.close()

def test_multiples_clientes_conectados():
    clientes = []

    for _ in range(3):
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.connect((HOST, PORT))
        clientes.append(c)

    time.sleep(0.1)

    clientes[0].send(b"Mensaje grupal")

    recibido = clientes[1].recv(1024)

    assert b"Mensaje grupal" in recibido

    for c in clientes:
        c.close()

def test_envio_recepcion_mensaje():
    cliente1= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    cliente1.connect((HOST, PORT))
    cliente2.connect((HOST, PORT))

    time.sleep(0.1)
    cliente1.send(b"Hola")
    recibido = cliente2.recv(1024)

    assert b"Hola" in recibido

    cliente1.close()
    cliente2.close()

def test_envio_multiples_mensajes():
    cliente1= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    cliente1.connect((HOST, PORT))
    cliente2.connect((HOST, PORT))

    time.sleep(0.1)

    mensajes = [b"uno", b"dos", b"tres"]

    for m in mensajes:
        cliente1.send(m)
        recibido = cliente2.recv(1024)
        assert m in recibido

    cliente1.close()
    cliente2.close()

def test_desconexion_cliente():
    c1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    c1.connect((HOST, PORT))
    c2.connect((HOST, PORT))

    c1.close()
    time.sleep(0.1)

    try:
        c2.send(b"Sigo conectado")
        assert True
    except Exception:
        pytest.fail("El servidor se cayó al desconectarse un cliente")

    c2.close()
