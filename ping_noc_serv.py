import socket
import sys 
import time

#Comprobamos que se haya introducido el puerto 

n_arg = len(sys.argv)
if(n_arg!=2):
    sys.exit('Numero de argumentos erroneo')

# Creamos el socket UDP

sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bindeamos con cualquier IP y puerto recibido por comando

puerto = int(sys.argv[1])
server_address = ('',puerto)
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
