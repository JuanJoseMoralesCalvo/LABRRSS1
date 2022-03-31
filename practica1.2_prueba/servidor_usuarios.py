import socket 
import sys
import time
import select
import json
n_arg = len(sys.argv)
if(n_arg!=2):
        sys.exit('Numero de argumentos erroneo\n')

# Creamos socket y igualamos el puerto a usar
sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1) # Nos permite reconectarnos
puerto = int(sys.argv[1])

# Permitimos la conexion
server_address = ('', puerto) # '' Significa que es a cualquier direccion
sockfd.bind(server_address)
sockfd.listen(5)

lista_sockets = [sockfd] #Creamos una lista de sockets para usuarios que se van uniendo
lista_clientes = []
lista_ip_y_puertos = {}
lista_de_nombres = ["servidor"]
lista_de_salas = ["servidor"]
lista_de_salas_nuevas = {}
i= 0
c=0
while True:
    ready_to_read, ready_to_write, in_error = select.select(lista_sockets, lista_clientes, lista_sockets,1)
    for sock in ready_to_read:
        if sock is sockfd:
            #Nuevo usuario
            socket_cliente, dir_cliente = sock.accept()
            aux = socket_cliente.recv(1024).decode("utf-8")
            aux_sep = aux.split(" ")
            nom_usuario = str(aux_sep[0])
            nom_sala = str(aux_sep[1])
            password = str(aux_sep[2])
            nueva_o_existente = str(aux_sep[3])
            if nueva_o_existente == "u": # ya existe la sala
                for i in lista_de_salas:
                    if i[0] == nom_sala and i[1] == password:
                        c=1
                    
                        
                if c==1:
                    lista_de_nombres.append((nom_usuario, nom_sala))
                    cliente_string = json.dumps(lista_ip_y_puertos[nom_sala])
                    socket_cliente.send(cliente_string.encode("utf-8"))
                    lista_sockets.append(socket_cliente)
                    lista_clientes.append(sock)
                    print(lista_ip_y_puertos)
                    print(lista_de_salas)
                    c=0
                else:
                    socket_cliente.send("y".encode("utf-8"))
            else:
                lista_de_nombres.append((nom_usuario, nom_sala))
                lista_de_salas.append((nom_sala,password))
                lista_sockets.append(socket_cliente)
                lista_ip_y_puertos[nom_sala]={}
                lista_clientes.append(sock)
                cliente_string = json.dumps(lista_de_salas_nuevas)
                socket_cliente.send(cliente_string.encode("utf-8"))
                 

        else:
            #Datos recibidos de un cliente
            datos = sock.recv(1024)
            if datos:
                #Nuevo cliente nos envia direccion y puerto
                exit = datos.decode("utf-8")
                if exit == "exit\n":
                    elim = lista_sockets.index((sock))
                    del lista_ip_y_puertos[lista_de_nombres[elim][1]][lista_de_nombres[elim][0]]
                    lista_sockets.remove(sock)
                    lista_de_nombres.remove(lista_de_nombres[elim])
                    sock.close()
                else:
                    li = json.loads(datos)
                    lista_ip_y_puertos[nom_sala][nom_usuario]=li
                    for socket in lista_sockets:
                        if socket != sockfd and socket !=sock:
                            socket.send(datos)






