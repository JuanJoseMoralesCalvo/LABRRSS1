
#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <math.h>
#include <string.h>

#define PORT_TCP_SERV 5001
#define MAXLINEA 500
#define SERVER_DIR "127.0.0.1"
int main()
{
	int sockfd, n, newsockfd, clilen, childpid;//socket y socket nuevo, longitudes y PID
	struct sockaddr_in cliente, servidor; //Direcciones de cliente y servidor
	char linea2[MAXLINEA]="64 bytes from ";//Linea a trasmitir
	char linea1[MAXLINEA];
	bzero((char*) &servidor,sizeof(servidor)); //Ponemos a 0 la variable

	servidor.sin_family = AF_INET; //TCP
	servidor.sin_port = htons(PORT_TCP_SERV); //Puerto
	servidor.sin_addr.s_addr = INADDR_ANY; //Cualquier cliente a la escucha
	
	if((sockfd = socket(AF_INET, SOCK_STREAM, 0))<0)
	{
		printf("ERROR AL ABRIR EL SOCKET\n");
		return -1;
	}

	if(bind(sockfd,(struct sockaddr*)&servidor,sizeof(servidor))<0)
	{
		printf("ERROR, NO SE PUEDE ASOCIAR EL SOCKET");
		return -1;
	}

	if(listen(sockfd,5) == -1)
	{
		printf("Error al escuchar\n");
		return -1;
	}
	for(;;)
	{
		printf("Estoy leyendo\n");
		clilen = sizeof(cliente);
		newsockfd= accept(sockfd,(struct sockaddr *)&cliente,&clilen);
		
		if(newsockfd<0)
		{
			printf("Problema en el accept");
			return -1;
		}

		while(read(newsockfd,linea1,sizeof(linea1))>0)
		{//leemos
			write(newsockfd,linea2,sizeof(linea2));//escribimos cuando recibimos el ping
		}
		close(newsockfd);
	}
	


	return 0;
}
