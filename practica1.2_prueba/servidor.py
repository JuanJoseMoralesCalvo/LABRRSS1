
import socket
import sys
import time
import select

HEADER_LENGTH = 10
# Funcion en la que recibimos el mensaje
def recieve_message(socket_cli):
    try:
        msg_header = socket_cli.recv(HEADER_LENGTH)

        msg_len = int(msg_header.decode("utf-8").strip())
        return {"header": msg_header, "data": socket_cli.recv(msg_len)}
    except:
        return False
# Comprobamos numero de argumentos
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
lista_clientes = [] #Creamos la lista de clientes

while True:
    ready_to_read, ready_to_write, in_error = select.select(lista_sockets, lista_clientes, lista_sockets,1)
    for sock in ready_to_read:
        if sock is sockfd: #Alguien nuevo se ha conectado al servidor
            print("Hola\n")
            socket_cliente, dir_Cliente = sock.accept()
            lista_sockets.append(socket_cliente)
            lista_clientes.append(sock)
        else:
            print("Datos recibidos del cliente:\n")
                
         #   datos = recieve_message(sock)
            datos = sock.recv(1024)
            if datos:

                for socket in lista_sockets:
                    if socket != sock:
                        try:
                            socket.send(datos)
                        except:
                        
                            continue
            else:
                
                print("Cliente desconectado")
                lista_sockets.remove(sock)
                if sock in lista_clientes:
                    lista_clientes.remove(sock)
                continue




    
