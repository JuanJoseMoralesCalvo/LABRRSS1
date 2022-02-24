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
	int long_cliente;
	int sockfd, n=1, clilen, childpid;//socket y socket nuevo, longitudes y PID
	struct sockaddr_in cliente, servidor; //Direcciones de cliente y servidor
	char linea2[MAXLINEA]="64 bytes from";//Linea a trasmitir
	char linea1[MAXLINEA];
	int i,j;
	char ip;
	bzero((char*) &servidor,sizeof(servidor)); //Ponemos a 0 la variable
	bzero((char*) &cliente,sizeof(cliente));
	servidor.sin_family = AF_INET; //TCP
	servidor.sin_port = htons(PORT_TCP_SERV); //Puerto
	servidor.sin_addr.s_addr = INADDR_ANY; //Cualquier cliente a la escucha
	if((sockfd = socket(AF_INET, SOCK_DGRAM, 0))<0)
	{
		printf("ERROR AL ABRIR EL SOCKET\n");
		return -1;
	}

	if(bind(sockfd,(struct sockaddr*)&servidor,sizeof(struct sockaddr ))<0)
	{
		printf("ERROR, NO SE PUEDE ASOCIAR EL SOCKET");
		return -1;
	}
	i=0;
	j=0;
	long_cliente=sizeof(cliente);
	while(n>0)
	{//leemos
	
			j++;			
			printf("Hola %d : %d \n",i,j);	
			n=recvfrom(sockfd,linea1,sizeof(linea1),0,(struct sockaddr *)&cliente,&long_cliente);
			i=sendto(sockfd,linea2,MAXLINEA,0,(struct sockaddr *)&cliente,long_cliente);//escribimos cuando recibimos el pingi
			if(i<0)
				printf("Error");
			printf("Mando\n");
			
		}

	close(sockfd);

		


	return 0;
}
