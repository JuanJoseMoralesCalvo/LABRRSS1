import socket
import sys
import time
import select
import errno
import threading as th

n_arg = len(sys.argv)
if(n_arg!=3):
    sys.exit('Numero de argumentos erroneo\n')

print("Buen Dia, introduzca su nombre de usuario\n")

# Nombre de usuario recibido por teclado
nom_usuario = input()

print(f"Bienvenido {nom_usuario}, si desea enviar un archivo introduzca una f seguida del archivo con su formato\n")

# Creamos el socket TCP
sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# IP del servidor y puerto
host = str(sys.argv[1])
ip = socket.gethostbyname(host)
puerto = int(sys.argv[2])
server_address = (ip, puerto)

# Realizamos el connect
sockfd.connect(server_address)
#sockfd.setblocking(False)


# Empieza el chat
while True:
    ready_to_read, ready_to_write, in_error = select.select([sys.stdin,sockfd],[],[],1) #Dejamos un segundo para querer escribir
   
    for sock in ready_to_read:
        if sock is sockfd:

            
            msg = sockfd.recv(1024).decode("utf-8")
            if msg:
                if msg[0] == "f":
                    with open('rec.txt','w') as f:
                        while msg[0] != "r":
                            msg = sockfd.recv(1024)
                            msg = msg.decode("utf-8")
                            f.write(msg)
                            print(f"{msg}")

                else:
                    print(f"{msg}")
        else:
            msg = sys.stdin.readline()
            if msg: #Que no este vacio
                if msg[0] == "f":
                    aux = msg.split()
                    fichero = str(aux[1])
                    f=open(fichero,'rb')
                    content = f.read(1024)
                    sockfd.send("f".encode("utf-8"))
                    while content:
                        sockfd.send(content)
                        content = f.read(1024)
                    sockfd.send("r".encode("utf-8"))


                else:
                    msg_env = nom_usuario +": "+msg
                    sockfd.send(msg_env.encode("utf-8"))


       
