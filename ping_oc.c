//PROTOCOLO TCP ORIENTADO A CONEXION
//
//CLIENTE

#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <math.h>
#include <string.h>
#define MAXLINEA 500

int main(int argc, char *argv[])
{
	if(argc!=4)
	{
		printf("\nNo se introdujeron el número de argumentos correctamente\n");
		return -1;
	}
	struct timeval begin;
    	struct timeval end;
	float tiempo;
	int seq=1;
	int num_pet = atoi(argv[1]); //Numero de peticiones PING
	int num_pet2=0;
	char *ip = argv[2]; // URL/IP del servidor
	int puerto = atoi(argv[3]); //Puerto deseado para el socket
	int num_failed=0; //Numero de paquetes fallidos
	int num_rec; //Numero de paquetes recividos
	int perloss;
	char lineaenv[MAXLINEA]= "PING";
	char linearec[MAXLINEA];
	int n; //Variable de tamaño de la Linea
	char ipstr[16];
	int sockfd;//Variable para acceder al socket
	struct sockaddr_in servidor; //Variable para direccion de servidor
	struct hostent *host; //Resuelve la direccion por la URL
	float seconds,ms,min,max,avg,mdev;
	min=1000.0f;
	max=0.0f;
	avg=0.0;
	mdev=0.0;
	if((host=gethostbyname(ip))==NULL)
	{
		printf("No se pudo resolver la direccion de la URL recibida");
		return -1;
	}

	if((sockfd=socket(AF_INET, SOCK_STREAM, 0)) < 0) //SOCK_STREAM=TCP, devuelve -1 ante error
	{
		printf("Cliente: No se pudo abrir el socket");
		return -1;
	}
	n=strlen(lineaenv);//n=4 (PING)
	bzero((char*) &servidor, sizeof(servidor));

	servidor.sin_family = AF_INET;
	servidor.sin_port = htons(puerto);
	servidor.sin_addr = *((struct in_addr *)host->h_addr);
 	
	//A continuacion se conecta con el servidor
	printf("Conectando\n");
	if(connect(sockfd,(struct sockaddr *) &servidor, sizeof(struct sockaddr))==-1)
	{
		printf("Error al conectarse con el servidor\n");
		return -1;

	}
	else
	{
		inet_ntop(AF_INET, host->h_addr_list[0],ipstr,16);
		printf("PING %s (%s) %d bytes of data.\n", ip, ipstr,num_pet*64);//(char*) host->h_addr);
	}
	num_pet2=num_pet;
	while(num_pet2>0)
	{
		
		gettimeofday(&begin, 0);
		if(write(sockfd,lineaenv,n)!=n)
		{
			printf("ERROR AL ENVIAR LA LINEA CON WRITE\n");
			return -1;
		}
		if(read(sockfd,linearec,MAXLINEA)<0)
		{
			printf("ERROR AL RECIBIR LA LINEA CON READ\n");
			num_failed=num_failed+1;
		}
		gettimeofday(&end, 0);
		seconds=(end.tv_sec-begin.tv_sec)*1e6;
		ms=end.tv_usec-begin.tv_usec;
		tiempo=seconds+ms;
		if(min>tiempo)
			min=tiempo;
		if(max<tiempo)
			max=tiempo;
		avg=avg+tiempo;
		num_pet2--;
		printf("%s %s: icmp_seq=%d ttl=44 tiempo=%f us \n" ,linearec, ipstr,seq,tiempo);
		seq++;


	}
	
	close(sockfd); //LIBERAMOS CONEXION
	num_rec = num_pet - num_failed;
	perloss = num_failed/num_pet *100;
	mdev=sqrt((pow(avg,2)/num_pet)-pow(avg/num_pet,2));
	printf("\n---------- %s ping statistics -----------\n",ip);
	printf("%d packets transmitted, %d received, %d percent loss, tiempo %f us\n", num_pet, num_rec, perloss,avg);
	printf("rtt min/avg/max/mdev = %f/%f/%f/%f\n",min,avg/num_pet,max,mdev);
	return 0;

}


