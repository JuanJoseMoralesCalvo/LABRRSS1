import socket
import sys 
import time

# Creamos el socket UDP

sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bindeamos con cualquier IP y puerto 5004

server_address = ('',5004)
sockfd.bind(server_address)
linea="PING RECIEVED"
while True:
    #Recibimos y enviamos, no necesita el accept

    try:
        print("Leyendo")

        while True:
            (linearec, address) = sockfd.recvfrom(64)
            if linearec:
                sockfd.sendto(linea.encode('utf-8'),address)
            else:
                break
    finally:
        #Se ejecuta siempre del bloque try
        sockfd.close()
