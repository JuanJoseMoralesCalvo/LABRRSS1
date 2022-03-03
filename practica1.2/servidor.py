
import socket
import sys
import time
import select

# Comprobamos numero de argumentos
n_arg = len(sys.argv)
if(n_arg!=2):
    sys.exit('Numero de argumentos erroneo')


# Creamos socket y igualamos el puerto a usar
sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
puerto = int(sys.argv[1])
#bindeamos
server_address = ('', puerto) # '' Significa que es a cualquier direccion
sockfd.bind(server_address)

sockfd.listen(5)
lista_sockets = [sockfd]

while True:
    ready_to_read, ready_to_write, in_error = select.select(lista_sockets, lista_sockets, [], 5)
    if len(ready_to_read) != 0:
        for sock in ready_to_read:
            if sock is sockfd:
                conexion_Cliente, dir_Cliente = sock.accept()
                conexion_Cliente.setblocking(0)
                lista_sockets.append(conexion_Cliente)
                print ("Conectado cliente: {}".format(dir_Cliente))
            else:
                print("Datos recibidos\n")
                datos = sock.recv(1024)
                if not datos:
                    print("Cliente desconectado")
                    lista_sockets.remove(sock)
                else:
                    print("\nLos datos son: {}".format(datos.decode("utf-8")))

    if len(ready_to_write) != 0:
        for sock in ready_to_write:
            sock.send("Python select server from Ubuntu.\n".encode("utf-8"))
