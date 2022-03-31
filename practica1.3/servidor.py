import socket

sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR , 1)
sockfd.bind(('192.168.188.227', 8888))
sockfd.listen(1)

while True:
    sockcli, sockcli_address = sockfd.accept()
    request = sockcli.recv(1024)
    print(request.decode("utf-8")+"\n")

