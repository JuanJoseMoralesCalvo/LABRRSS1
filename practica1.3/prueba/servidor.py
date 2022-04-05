import socket 
import select

host , port = '0.0.0.0' , 8888

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR , 1)
serversocket.bind((host , port))
serversocket.listen(1)
print('servidor en el puerto',port)
socket_list = [serversocket]
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
                requesting_file = aux[1]
                aux2 = persistent.split(" ")
                print('Client request \n')
                myfile=requesting_file[1:]
                

                if(myfile == ''):
                    myfile = 'index.html'

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
            

    
