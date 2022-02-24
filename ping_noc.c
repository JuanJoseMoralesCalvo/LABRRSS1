//PROTOCOLO UDP NO ORIENTADO A CONEXION
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
#define PORT_TCP_SERV 5000
#define MAXLINEA 500
#define SERVER_DIR "127.0.0.1"

int main(int argc, char *argv[])
{
	if(argc!=3)
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
	int long_servidor;
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

	if((sockfd=socket(AF_INET, SOCK_DGRAM, 0)) < 0) //SOCK_STREAM=UDP, devuelve -1 ante error
	{
		printf("Cliente: No se pudo abrir el socket");
		return -1;
	}
	
	servidor.sin_family = AF_INET;
	servidor.sin_port = htons(PORT_TCP_SERV);
	//memcpy(&servidor.sin_addr, host->h_addr_list[0], host->h_length);
	servidor.sin_addr = *((struct in_addr *)host->h_addr);
	//servidor.sin_addr.s_addr = INADDR_ANY;
	inet_ntop(AF_INET, host->h_addr_list[0],ipstr,16);
	
	printf("PING %s (%s) X bytes of data.\n", ip, ipstr);
	
	n=strlen(lineaenv);
	num_pet2=num_pet;
	long_servidor=sizeof(servidor);
	while(num_pet2>0)
	{
		gettimeofday(&begin, 0);
		if(sendto(sockfd,lineaenv,n,0,(struct sockaddr *)&servidor,sizeof(servidor))!=n)
		{
			printf("ERROR AL ENVIAR LA LINEA CON WRITE\n");
			return -1;
		}
		
		if(recvfrom(sockfd,linearec,MAXLINEA,0,(struct sockaddr *)0,(int*)0)<0)
		{
			printf("ERROR AL RECIBIR LA LINEA CON READ\n");
			num_failed=num_failed+1;
		}
		
		gettimeofday(&end, 0);
		seconds=(end.tv_sec-begin.tv_sec)*1e-6;
		ms=end.tv_usec-begin.tv_usec;
		tiempo=seconds+ms;
		if(min>tiempo)
			min=tiempo;
		if(max<tiempo)
			max=tiempo;
		avg=avg+tiempo;
		num_pet2 = num_pet2 - 1;
		printf("%s %s: icmp_seq=%d ttl=44 time=%f \n" ,linearec, ipstr,seq,tiempo);
		seq = seq +1;


	}
	
	close(sockfd); //LIBERAMOS CONEXION
	
	num_rec = num_pet - num_failed;
	perloss = num_failed/num_pet *100;
	mdev=sqrt((pow(avg,2)/num_pet)-pow(avg/num_pet,2));
	printf("\n---------- %s ping statistics -----------\n",ip);
	printf("%d packets transmitted, %d received, %d percent loss, time %f ms\n", num_pet, num_rec, perloss,avg);
	printf("rtt min/avg/max/mdev = %f/%f/%f/%f\n",min,avg/num_pet,max,mdev);
	return 0;
}
