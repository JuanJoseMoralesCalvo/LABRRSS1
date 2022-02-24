import socket
import sys

# Creamos socket
sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#bindeamos
server_address = ('', 5004) # '' Significa que es a cualquier direccion
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

