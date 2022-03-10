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

# Creamos el socket TCP
sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# IP del servidor y puerto
host = str(sys.argv[1])
ip = socket.gethostbyname(host)
puerto = int(sys.argv[2])
server_address = (ip, puerto)

# Realizamos el connect
sockfd.connect(server_address)
#sockfd.setblocking(False)

lista_socket= [sockfd]
lista_ip = []
lista_puerto = []

msg_ini = (f"{ip},{puerto}")


msg = sockfd.recv(1024).decode("utf-8") # Recibimos la ip y puerto del resto de clientes
_,ip, puerto = msg.split(" ") # Primero IP y despues PUERTO
lista_ip.append(ip)
lista_puerto.append(puerto)
i=0

for socket in lista_socket:
    socket.connect((lista_ip[i],lista_puerto[i]))
    i++
# Empieza el chat
while True:
    ready_to_read, ready_to_write, error = select.select([sys.stdin,lista_socket],[],[],1)
    
    for sock in ready_to_read:
        if sock is sockfd: # NOS HABLA EL SERVIDOR PARA AÑADIR O REMOVER CLIENTES
            

            msg_nuevo = sockfd.recv(1024).decode("utf-8") # Recibimos la ip y puerto del resto de clientes
            if msg_nuevo:
                if msg_nuevo[0] == "a":
                    _,ip, puerto = msg_nuevo.split(" ") # Primero IP y despues PUERTO
                    lista_ip.append(ip)
                    lista_puerto.append(puerto)
                    socket_cliente, dir_cliente = sock.accept()
                    lista_socket.append(socket_cliente)
                if msg_nuevo[0] == "r":
                    _,ip, puerto = socketnuevo.split(" ") # Primero IP y despues PUERTO
                    lista_ip.remove(ip)
                    lista_puerto.remove(puerto)
                    socket_cliente, dir_cliente = sock.close()
        
        else: # HABLAMOS CON CLIENTES




