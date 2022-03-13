import socket 
import sys
import time
import select
import pickle
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
lista_ip_puertos =


while True:
    ready_to_read, ready_to_write, in_error = select.select(lista_sockets, lista_clientes, lista_sockets,1)
    for sock in ready_to_read:
        if sock is sockfd:
            #Nuevo usuario
            socket_cliente, dir_cliente = sock.accept()
            cliente_string = pickle.dumps(lista_ip_y_puertos)
            socket_cliente.send(cliente_string)
            lista_sockets.append(socket_cliente)
            lista_clientes.append(sock)
            
        else:
            #Datos recibidos de un cliente
            datos = sock.recv(1024)
            if datos:
                #Nuevo cliente nos envia direccion y puerto
                lista_ip_y_puertos = pickle.loads(datos)
                for socket in lista_sockets:
                    if socket != sockfd and socket !=sock:
                        socket.send(lista_ip_y_puertos)




