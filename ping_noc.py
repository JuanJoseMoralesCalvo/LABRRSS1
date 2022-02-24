import socket
import sys
import time
import math as m
#Comprobamos numero de argumentos
n_arg = len(sys.argv)
if(n_arg!=3):
    sys.exit('Numero de argumentos erroneo')

# Creamos el socket UDP
sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# IP del servidor y puerto

host = str(sys.argv[2])
ip = socket.gethostbyname(host)
server_address = (ip, 5004) #hacemos uso del puerto 5004

#Numero de peticiones, auxiliar para bucle, numero de secuencia
num_pet = int(sys.argv[1])
num_pet2 = num_pet
nseq = 1
ttl = 44
times = 100

linea = "PING"
minimo = 100
maximo = 0
avg=0
print("PING {} ({}) X bytes of data. ".format(host,ip))

#iteramos
while num_pet2>0:
    start = time.time()
    sockfd.sendto(linea.encode('utf-8'), server_address) #Realizamos el sendto al servidor
    sockfd.recvfrom(64) #Esperamos a recibir info del servidor
    end = time.time()
    times = (end - start)*1000 #milisegundos
    print("64 bytes from {} ({}): icmp_seq={} ttl={} time={}".format(host,ip,nseq,ttl,times))
    
    if(minimo>times):
        minimo=times
    if(maximo<times):
        maximo=times
    avg = avg + times
    num_pet2 = num_pet2 - 1
    nseq = nseq + 1
mdev = m.sqrt(avg**2/num_pet - (avg/num_pet)**2)
print("-------------------------- {} ping statistics------------------------".format(host))
print("{} packets transmited, {} received, 0% packet loss, time {}ms".format(num_pet, num_pet,avg))
print("rtt min/avg/max/mdev = {}/{}/{}/{}".format(minimo,avg/num_pet,maximo,mdev))
sockfd.close()


