import socket
import sys
import time
import select
import errno
import pickle


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

#Primero recibimos la lista de clientes una vez nos conectamos

lista_de_clientes = pickle.loads(sockfd.recv(1024)) # Recibimos el numero de clientes
tam_lista = len(lista_de_clientes)

#Enviamos nuestra direccion y puerto al servidor
sockcli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockcli.bind(('',0)) #Random port and every ip
sockcli.listen(5)

ip_cliente, puerto_cliente = sockcli.getsockname() 
cliente = ([ip_cliente],[puerto_cliente])
cliente_string = pickle.dumps(cliente)
sockfd.send(cliente_string)


lista_socket= [sys.stdin,sockfd,sockcli]

    


if tam_lista == 0:
    print("Es usted el primer usuario en el chat, espere a que alguien se conecte\n")
    
#La primera vez que nos conectamos al chat realizamos la conexion con los peers
else:
    print(lista_de_clientes)
    for i in range(tam_lista):
        socket_clientes = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_clientes.connect((lista_de_clientes[i][0],lista_de_clientes[i][1]))
        print(f"Conectado a {lista_de_clientes[i][0]}:{lista_de_clientes[i][1]}")
        lista_socket.append(socket_clientes)
# Empieza el chat
while True:
    ready_to_read, ready_to_write, error = select.select(lista_socket,[],[],1)
    
    for sock in ready_to_read:
        if sock is sockcli:
            socket_cliente, dir_cliente = sock.accept()
            lista_socket.append(socket_cliente)

        else: # HABLAMOS CON CLIENTES
            if sock is sys.stdin:
                msg = sys.stdin.readline()
                if msg:
                    msg_env = nom_usuario +": "+msg
                    for socket in lista_socket:
                        if socket != sockfd and socket != sockcli:
                            socket.send(msg_env.encode("utf-8"))
            else:
                msg = sock.recv(1024).decode("utf-8")
                print(f"{msg}")

                    




