import socket
import sys
import time
import select

# Comprobamos numero de argumentos
n_arg = len(sys.argv)
if(n_arg!=3):
    sys.exit('Numero de argumentos erroneo')

print("Buen Dia, introduzca su nombre de usuario\n")

# Nombre de usuario recibido por teclado
nom_usuario = input()

# Creamos el socket TCP
sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# IP del servidor y puerto
host = str(sys.argv[1])
ip = socket.gethostbyname(host)
puerto = int(sys.argv[2])
server_address = (ip, puerto)

# Realizamos el connect
sockfd.connect(server_address)

# Empieza el chat
while True:
    
    ready_to_read, ready_to_write, in_error = select.select([sockfd],[sockfd],[],5)
   
    if len(ready_to_read) != 0:
        buf = sockfd.recv(64)  #Recibimos bloques de 64 bytes
        if len(buf) != 0:
            print("{}\n".format(buf.decode("utf-8")))

    if len(ready_to_write) != 0:
        mensaje = input()
        sockfd.send(mensaje.encode("utf-8"))


