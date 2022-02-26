import socket
import sys

# Comprobamos que se ha introducido el puerto		    
n_arg = len(sys.argv)
if(n_arg!=2):
    sys.exit('Numero de argumentos erroneo')
# Creamos socket y igualamos el puerto a usar
sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
puerto = int(sys.argv[1])
#bindeamos
server_address = ('', puerto) # '' Significa que es a cualquier direccion
sockfd.bind(server_address)

sockfd.listen(1)

while True:

    (clientsocket, client_address) = sockfd.accept()
    try:
        print("Leyendo")
        while True:
            
            linearec = clientsocket.recv(64)
            if linearec:
                clientsocket.sendall(linearec)
            else:
                break
    finally: 
        # Se ejecuta siempre despues de un bloque try
        clientsocket.close()

