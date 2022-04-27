import socket 
import select
import requests
import re
import mysql.connector as mariadb
import datetime
host , port = '0.0.0.0' , 4443

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR , 1)
serversocket.bind((host , port))
serversocket.listen(1)
print('servidor en el puerto',port)
socket_list = [serversocket]

mariadb_connection = mariadb.connect(user='practica3',password='123',database= 'practica3', host='localhost',port='3306')

cursor=mariadb_connection.cursor()


while True:
    ready_to_read, ready_to_write, in_error = select.select(socket_list,[],[],10)
    for sock in ready_to_read:
        if sock is serversocket:
            connection , address = serversocket.accept()
            socket_list.append(connection)
        else:
            request = sock.recv(1024)
            if request:
                request = request.decode()
                print(request)
                string_list = request.split('\n')
                method = string_list[0]
                aux = method.split(" ")
                persistent = string_list[2]
                metodo = aux[0]
                requesting_file = aux[1]
                aux2 = persistent.split(" ")
                print('Client request \n')
                myfile=requesting_file[1:]
                if metodo == "POST":
                    aux_url = string_list[14]
                    aux_url = aux_url.split("=")
                    url_aux = aux_url[1]
                    idioma = aux_url[2]
                    url = url_aux.split("&")
                    url = url[0]
                    url = re.sub("%3A",":",url) # Se sustituye %3A por :
                    url = re.sub("%2F","/",url) # Se sustituye %2F por /
                    if idioma=="Espanol":
                        language = {"Accept-Language": "es-ES,es;q=0.5"}
                        param = dict(lang='es-ES,es;q=0.5')
                    elif idioma=="Ingles":
                        language = {"Accept-Language": "en-US,en;q=0.5"}
                        param = dict(lang='en-US,en;q=0.5')
                    print(language)
                    r = requests.get(url, headers=language, params=param)
                    r = r.text
                    header = 'HTTP/1.1 200 OK\n'
                    mimetype = 'text/html'
                    header += 'Content-Type: '+str(mimetype)+'\n\n'
                    responde = header+r
                    sock.send(responde.encode())
                    
                    #Parte de mysql
                    dia_aux = datetime.datetime.now()
                    dia = dia_aux.strftime("%y-%m-%d %H:%M:%S")
                    insertar = 'INSERT INTO historial(url, date) VALUES (%s, %s)'
                    elementos = (url, dia)
                    cursor.execute(insertar, elementos)
                    mariadb_connection.commit()

                else:
                    if(myfile == ''):
                        myfile = 'index.html'
                    elif myfile[0:3] == "htt":
                        r = requests.get(myfile)
                        r = r.text
                        header = 'HTTP/1.1 200 OK\n'
                        mimetype = 'text/html'
                        header += 'Content-Type: '+str(mimetype)+'\n\n'
                        responde = header+r
                        sock.send(responde.encode())
                    else:
                        try:
                            file = open(myfile , 'rb')
                            response = file.read()
                            file.close()

                            header = 'HTTP/1.1 200 OK\n'

                            if(myfile.endswith('.jpg')):
                                mimetype = 'image/jpg'
                            elif(myfile.endswith('.css')):
                                mimetype = 'text/css'
                            elif(myfile.endswith('.pdf')):
                                mimetype = 'application/pdf'
                            else:
                                mimetype = 'text/html'

                            header += 'Content-Type: '+str(mimetype)+'\n\n'

                        except Exception as e:
                            print("-")
                            header = 'HTTP/1.1 404 Not Found\n\n'
                            response = '<html><body>Error 404: File not found</body></html>'.encode('utf-8')

                        final_response = header.encode('utf-8')
                        final_response += response
                        sock.send(final_response)
                        print(aux2[1])
                        if aux2[1] == "keep-alive\r":
                            continue
                        else:
                            socket_list.remove(sock)
                            sock.close()
            
    if not (ready_to_read or ready_to_write or in_error):
        print("Servidor se encuentra inactivo\n")
