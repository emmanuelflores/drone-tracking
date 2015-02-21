// Basic server/client class for RPi
// Socket.cpp
// SmaCoCo
// v0.1 19-11-2014

#include "socket.h"

Socket::Socket(){
	mode = 0;
	int sockfd = -1;
	int newsockfd = -1;
	int port = -1;
	int clilen = -1;
	char* ip = new char[16];
	struct sockaddr_in serv_addr;
	struct sockaddr_in cli_addr;
	struct hostent* server = NULL;
}

//Socket::~Socket()
//{
//	delete mode;
//	delete sockfd;
//	delete newsockfd;
//	delete port;
//	delete clilen;
//	delete[] ip;
//	delete serv_addr;
//	delete cli_addr;
//	delete server;
//}

void Socket::setupServer(int port){
	if((mode == 0) || (mode == 1))
	{
		mode = 1;
	}
	else
	{
		cout << "ERROR: Socket is used as a client!" << endl;
	}
		
	cout << "Initiating new server at port " << port << endl;
	sockfd = socket(AF_INET, SOCK_STREAM, 0);
	if (sockfd < 0)
	{
        cout << "ERROR: Could not open socket" << endl;
	}
	else
	{
		cout << "Socket creation successful!" << endl;
	}
	
	bzero((char *) &serv_addr, sizeof(serv_addr));	
	
	serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = INADDR_ANY;
    serv_addr.sin_port = htons( port );
    if (bind(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0)
	{
		cout <<  "ERROR on binding" << endl;
	}
	else
	{
		cout << "Binding successful!" << endl;
	}
	
	listen(sockfd,MAX_NO_CLIENTS);
	clilen = sizeof(cli_addr);
}

bool Socket::acceptServer(){
	cout <<  "Waiting for new client..." << endl;
	newsockfd = accept( sockfd, (struct sockaddr *) &cli_addr, (socklen_t*) &clilen);
	if (newsockfd < 0)
	{
		cout << "ERROR: Could not accept connection" << endl;
		return false;
	}
	else
	{
		cout << "Connection to client successful!" << endl; 
		return true;
	}
}

void Socket::closeSocket(){
	//if(mode == 1)
		close( newsockfd );
	//else
		close( sockfd );
}

int Socket::getData(){
	char buffer[32];
	int n;
	int sock;
	if(mode == 1)
		sock = newsockfd; 
	else
		sock = sockfd;
	
	if ( (n = read(sock,buffer,31) ) < 0 )
	{
		cout << "ERROR reading from socket" << endl;
	}
	else
	{
		cout << "Data received!" << endl;
	}
	buffer[n] = '\0';
	return atoi( buffer );
}

char* Socket::getChars()
{
	char* buffer = new char[128];
	int n;
	int sock;
	if(mode == 1)
		sock = newsockfd; 
	else
		sock = sockfd;
	
	if ( (n = read(sock,buffer,128) ) < 0 )
	{
		cout << "ERROR reading from socket" << endl;
	}
	else
	{
		cout << "Data received!" << endl;
	}
	buffer[n] = '\0';
	return buffer;
}

string Socket::getStr(){
	char buffer[128];	
	int sock, n;
	
	if(mode == 1)
		sock = newsockfd; 
	else
		sock = sockfd;
	
	if( n = read(sock,buffer, 64) < -1)
	{
		cout << "ERROR reading from socket" << endl;
		return "ERROR";
	}
	else
	{
		#ifdef DEBUG
		cout << "Data received!" << endl;
		#endif
	}
	
	buffer[n] = '\0';
	string strbuf = buffer;	
	return strbuf;	
}

// sendData(int) is deprecated, use sendData(string) instead 
void Socket::sendData( int x ){
	int n;
	char buffer[32];
	int sock;
	if(mode == 1)
		sock = newsockfd;
	else
		sock = sockfd;
  
	sprintf( buffer, "%d\n", x );
	if ( (n = write( sock, buffer, strlen(buffer) ) ) < 0 )
		cout << "ERROR: Unable to write to socket" << endl;
	buffer[n] = '\0';
}

void Socket::sendData( string strToSend ){
	int n, sock;
	int len = strToSend.length();
	const char *buffer = strToSend.c_str();
	if(mode == 1)
		sock = newsockfd;
	else
		sock = sockfd;
  
	if( n = send(sock, buffer, len, MSG_EOR) < 0)
		cout << "ERROR: Unable to write to socket" << endl;
	//buffer[n] = '\0';
}

void Socket::setupClient(char* ipAddr, int portNo){
	if((mode == 0) || (mode == 2))
	{
		mode = 2;
	}
	else
	{
		cout << "ERROR: Socket is used as a client!" << endl;
	}
	
	ip = ipAddr;	
	port = portNo;
	
	printf( "Contacting server at %s on port %d\n", ip, port );
	
	if ( ( sockfd = socket(AF_INET, SOCK_STREAM, 0) ) < 0 )
	{
        cout << "ERROR: Could not open socket" << endl;
	}
	else
	{
		cout << "Socket creation successful!" << endl;
	}
	
    if ( ( server = gethostbyname( ip ) ) == NULL )
	{
        cout << "ERROR: Host does not exist, invalid IP address" << endl;
	}
	else
	{
		cout << "Host found!" << endl;
	}
	
	bzero( (char*) &serv_addr, sizeof(serv_addr));
	serv_addr.sin_family = AF_INET;
	bcopy( (char*)server->h_addr, (char *)&serv_addr.sin_addr.s_addr, server->h_length);
	serv_addr.sin_port = htons(portNo);	
	
	if ( connect(sockfd,(struct sockaddr *)&serv_addr,sizeof(serv_addr)) < 0)
	{
		cout << "ERROR: Unable to connect to host" << endl;
	}
}


