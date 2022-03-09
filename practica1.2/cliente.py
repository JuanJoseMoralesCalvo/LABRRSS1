import socket
import sys
import time
import select
import errno
import threading as th

#def introducir_mensaje():
 #   return input()

#timeout=4
#t=th.Timer(timeout,introducir_mensaje)

# Comprobamos numero de argumentos
n_arg = len(sys.argv)
if(n_arg!=3):
    sys.exit('Numero de argumentos erroneo\n')

print("Buen Dia, introduzca su nombre de usuario\n")

# Nombre de usuario recibido por teclado
HEADER_LENGTH = 10
nom_usuario = input()

print(f"Bienvenido {nom_usuario}, si desea enviar un archivo introduzca una f seguida del archivo con su formato\n")

usuario = nom_usuario.encode("utf-8")
usuario_header = f"{len(usuario):<{HEADER_LENGTH}}".encode("utf-8")
# Creamos el socket TCP
sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# IP del servidor y puerto
host = str(sys.argv[1])
ip = socket.gethostbyname(host)
puerto = int(sys.argv[2])
server_address = (ip, puerto)

# Realizamos el connect
sockfd.connect(server_address)
sockfd.setblocking(False)

sockfd.send(usuario_header + usuario)

# Empieza el chat
while True:
    ready_to_read, ready_to_write, in_error = select.select([sys.stdin,sockfd],[],[],1) #Dejamos un segundo para querer escribir
   
    for sock in ready_to_read:
        if sock is sockfd:
            usuario_header = sockfd.recv(HEADER_LENGTH)
            if not len(usuario_header):
                print("Cerramos conexion con el servidor")
                sys.exit()

            usuario_len = int(usuario_header.decode("utf-8").strip())
            usuario = sockfd.recv(usuario_len).decode("utf-8")
            
            msg_header = sockfd.recv(HEADER_LENGTH)
            msg_len = int(msg_header.decode("utf-8").strip())
            msg = sockfd.recv(msg_len).decode("utf-8")

            print(f"{usuario} > {msg}")
        else:
            msg = sys.stdin.readline()
            if msg: #Que no este vacio
                if msg[0] == "f":
                    fichero = input("Introduzca el nombre del fichero con su formato") 
                    f=open(fichero,'rb')
                    content = f.read(1024)
                    
                    msg_header = f"{len(msg):<{HEADER_LENGTH}}".encode("utf-8")
                    while content:
                        sockfd.send(msg_header + content)
                        content = f.read(1024)





                else:
                    msg = msg.encode("utf-8")
                    msg_header = f"{len(msg):<{HEADER_LENGTH}}".encode("utf-8")
                    sockfd.send(msg_header + msg)


       
