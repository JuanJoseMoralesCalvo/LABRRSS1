import socket
import sys
import time
import select
import errno
import json

n_arg = len(sys.argv)
if(n_arg!=3):
    sys.exit('Numero de argumentos erroneo\n')

print("Buen Dia, introduzca su nombre de usuario\n")

# Nombre de usuario recibido por teclado
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
sockfd.send(nom_usuario.encode("utf-8"))
#Primero recibimos la lista de clientes una vez nos conectamos

lista_de_clientes = json.loads(sockfd.recv(1024)) # Recibimos el numero de clientes
tam_lista = len(lista_de_clientes)

#Enviamos nuestra direccion y puerto al servidor
sockcli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockcli.bind(('',0)) #Random port and every ip
sockcli.listen(5)

ip_cliente, puerto_cliente = sockcli.getsockname() 
cliente = {"ip":ip_cliente, "puerto":puerto_cliente}
cliente_string = json.dumps(cliente)
sockfd.send(cliente_string.encode("utf-8"))


lista_socket= [sys.stdin,sockfd,sockcli]

desconexion_cliente = "D"
    
print(lista_de_clientes)
i=0

if tam_lista == 0:
    print("Es usted el primer usuario en el chat, espere a que alguien se conecte\n")
    
#La primera vez que nos conectamos al chat realizamos la conexion con los peers
else:
    for i in lista_de_clientes.values():
        socket_clientes = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_clientes.connect((i["ip"],i["puerto"]))
       # print(f"Conectado a {lista_de_clientes["cliente"+str(i)]["ip"]}:{lista_de_clientes["cliente"+str(i)]["puerto"]}")
        lista_socket.append(socket_clientes)
# Empieza el chat

while True:
    ready_to_read, ready_to_write, error = select.select(lista_socket,[],[],1)
    
    for sock in ready_to_read:
        if sock is sockcli:
            socket_cliente, dir_cliente = sock.accept()
            lista_socket.append(socket_cliente)
            print("Un nuevo cliente se conecto a esta sala, Salude!")

        else: # HABLAMOS CON CLIENTES
            if sock is sys.stdin:
                msg = sys.stdin.readline()
                if msg:
                    if msg == "exit\n":
                        sockfd.send(msg.encode("utf-8"))
                        sys.exit()
                    elif msg[0] == "f":
                        print("Mandando fichero\n")
                        aux = msg.split()
                        fichero = str(aux[1])
                        f = open(fichero,'rb')
                        content = f.read(1024)
                        content_utf = content.decode("utf-8")
                        for socket in lista_socket:
                            if socket != sockfd and socket != sockcli and socket != sys.stdin:
                                socket.send("f".encode("utf-8"))

                        time.sleep(1)
                        while content:
                            print("Proceso de mandado\n")
                            for socket in lista_socket:
                                if socket != sockfd and socket != sockcli and socket != sys.stdin:
                                    socket.send(content)
                            content = f.read(1024)
                        print("FINALIZADO PROCESO DE MANDADO\n")
                        time.sleep(1)
                        for socket in lista_socket:
                            if socket != sockfd and socket != sockcli and socket != sys.stdin:
                                socket.send("r".encode("utf-8"))
                    
                    else:
                        msg_env = nom_usuario +": "+msg
                        for socket in lista_socket:
                            if socket != sockfd and socket != sockcli and socket != sys.stdin:
                                socket.send(msg_env.encode("utf-8"))
            else:
                try:
                    msg = sock.recv(1024).decode("utf-8")
                    if msg:
                        if msg[0] == "f":
                            print("Iniciamos proceso de escritura\n")
                            with open('rec2.txt','w') as f:
                                while msg[0] != "r":
                                    msg = sock.recv(1024)
                                    msg = msg.decode("utf-8")
                                    f.write(msg)
                                    print("Fichero recibido\n")

                        else:
                            print(f"{msg}")
                    else:
                        lista_socket.remove(sock)
                        print("Un cliente se desconecto de la sala de chat")
                        

                except:
                    continue

                    




