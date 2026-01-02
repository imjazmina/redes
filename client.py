import socket
import threading
from utils import validar_mensaje

def recibir_mensajes(sock, stop_event):
    while not stop_event.is_set():
        try:
            mensaje = sock.recv(1024)
            if not mensaje:
                print("Servidor desconectado.")
                stop_event.set()
                break
            print(mensaje.decode('utf-8'))
        except:
            print("Error al recibir mensaje.")
            stop_event.set()
            break
    sock.close()
    print("Hilo de recepción terminado.")

def enviar_mensajes(sock, stop_event):
    try:
        while not stop_event.is_set():
            mensaje = input()
            
            if mensaje.lower() == "/salir":
                print("Desconectando...")
                stop_event.set()
                sock.close()
                break

            if not validar_mensaje(mensaje):
                print("Mensaje inválido. Intente nuevamente.")
                continue

            sock.send(mensaje.encode('utf-8'))

    except (KeyboardInterrupt, EOFError):
        print("Cliente cerrado por el usuario.")
        stop_event.set()
        sock.close()

def main():
    host = '127.0.0.1'
    puerto = 8000

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente.connect((host, puerto))
        print("Conectado al servidor.")
    except:
        print("No se pudo conectar al servidor.")
        return

    stop_event = threading.Event()

    hilo_receptor = threading.Thread(target=recibir_mensajes, args=(cliente, stop_event))
    hilo_receptor.start()

    enviar_mensajes(cliente, stop_event)

    # Esperar que el hilo receptor termine antes de salir
    hilo_receptor.join()
    print("Cliente cerrado correctamente.")

if __name__ == "__main__":
    main()