import socket
import threading

def recibir_mensajes(sock):
    while True:
        try:
            mensaje = sock.recv(1024)
            if not mensaje:
                print("El servidor cerró la conexión.")
                break
            print(mensaje.decode('utf-8'))
        except:
            print("Error recibiendo mensaje. Desconectado.")
            break
    sock.close()
    print("Cerrando cliente...")
    os._exit(0)  # mata la ejecucion

def enviar_mensajes(sock):
    try:
        while True:
            mensaje = input()
            if mensaje.lower() == '/salir':
                print("Desconectando...")
                sock.close()
                break
            sock.send(mensaje.encode('utf-8'))
    except (KeyboardInterrupt, EOFError):
        print("Cliente cerrado por el usuario.")
        sock.close()

def main():
    host = '127.0.0.1'
    puerto = 8000

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente.connect((host, puerto))
        print("Conectado al servidor. Escribe tus mensajes:")
    except:
        print("No se pudo conectar al servidor.")
        return#pq devuelve nada

    # Hilos separados para enviar y recibir
    threading.Thread(target=recibir_mensajes, args=(cliente,), daemon=True).start()
    enviar_mensajes(cliente)

if __name__ == '__main__':
    import os #cierra el programa aunque existan hilos activos, cambiar