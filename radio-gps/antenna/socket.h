// Basic server/client class for RPi
// Socket.h
// SmaCoCo
// v0.1 19-11-2014

#ifndef SOCKET_H
#define SOCKET_H

#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>

#include <iostream>
using namespace std;

const int MAX_NO_CLIENTS = 5;

class Socket
{
	public:
		Socket();
		//~Socket();
		void setupServer(int port);
		bool acceptServer();
		void closeSocket();
		void setupClient(char* ipAddr, int portNo);
		void sendData(int x);
		void sendData(string strToSend);
		int getData();
		string getStr();
		char* getChars();
	protected:
	private:
		unsigned char mode; 
		int sockfd;
		int newsockfd;
		int port;
		int clilen;
		char* ip;
		struct sockaddr_in serv_addr;
		struct sockaddr_in cli_addr;
		struct hostent* server;
};

#endif
