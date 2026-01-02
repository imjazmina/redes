import socket
import threading
from utils import validar_mensaje, formatear_mensaje

clientes = set()
lock = threading.Lock() #bloqueo de hilos

def manejar_cliente(cliente, direccion):
    print(f"{direccion} se unio al chat")
    try:
        while True:
            mensaje = cliente.recv(1024)
            if not mensaje:#si el cliente se cierra recibe una cadena vacía: b'' y rompe el bucle
                break

            texto = mensaje.decode('utf-8')

            if not validar_mensaje(texto):
                continue  #mensaje invalido, no se procesa

            mensaje_final = formatear_mensaje(direccion, texto)
            print(mensaje_final)

            with lock:#si no se esta creando un nuevo hilo
                for c in list(clientes):#envia los mensajes
                    if c != cliente:
                        try:
                            c.send(mensaje_final.encode('utf-8'))
                        except:#si fallo el envio
                            clientes.remove(c)
                            c.close()#cierra el socket del cliente
    except Exception as e:
        print(f"Error con {direccion}: {e}")
    finally:#si hay deconexion de un cliente
        with lock:
            clientes.discard(cliente)
        cliente.close()
        print(f"Conexión cerrada de {direccion}")

def servidor():
    host = "127.0.0.1"
    puerto = 8000

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, puerto))
    servidor.listen()
    servidor.settimeout(1.0)  #bloqueante de accept

    print(f"Servidor escuchando en {host}:{puerto}")

    try:
        while True:
            try:
                cliente, direccion = servidor.accept()
                with lock:
                    clientes.add(cliente)
                hilo = threading.Thread(target=manejar_cliente, args=(cliente, direccion))
                hilo.start()
            except socket.timeout:
                continue  # Permite verificar si se presionó Ctrl+C
    except KeyboardInterrupt:
        print("Servidor detenido por el usuario.")
    finally: #siempre se ejecuta
        with lock:
            for c in clientes:
                c.close()
        servidor.close()
        print("Servidor cerrado.")

if __name__ == "__main__":
    servidor()
