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

i= 0
while True:
    ready_to_read, ready_to_write, in_error = select.select(lista_sockets, lista_clientes, lista_sockets,1)
    for sock in ready_to_read:
        if sock is sockfd:
            #Nuevo usuario
            socket_cliente, dir_cliente = sock.accept()
            nom_usuario = socket_cliente.recv(1024).decode("utf-8")
            lista_de_nombres.append(nom_usuario)
            cliente_string = json.dumps(lista_ip_y_puertos)
            socket_cliente.send(cliente_string.encode("utf-8"))
            lista_sockets.append(socket_cliente)
            lista_clientes.append(sock)
            print(lista_ip_y_puertos) 
            i = i+1 
        else:
            #Datos recibidos de un cliente
            datos = sock.recv(1024)
            if datos:
                #Nuevo cliente nos envia direccion y puerto
                exit = datos.decode("utf-8")
                if exit == "exit\n":
                    elim = lista_sockets.index((sock))
                    del lista_ip_y_puertos[lista_de_nombres[elim]]
                    lista_sockets.remove(sock)
                    lista_de_nombres.remove(lista_de_nombres[elim])
                    sock.close()
                    i = i -1
                else:
                    li = json.loads(datos)
                    lista_ip_y_puertos[lista_de_nombres[i]] = li 
                    for socket in lista_sockets:
                        if socket != sockfd and socket !=sock:
                            socket.send(datos)

        #    else:
         #       print(lista_ip_y_puertos) 

          #      elim = lista_sockets.index((sock))
           #     elim_usuario = elim - 1
            #    del lista_ip_y_puertos["cliente"+str(elim_usuario)]
             #   lista_sockets.remove(sock)
              #  i = len(lista_ip_y_puertos)
               # sock.close()




