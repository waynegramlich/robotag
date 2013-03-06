/* Copyright (c) 2011 by Intelligent Machines Corporation. */
/* All rights reserved. */

/*
 * Usage: ttyshare program arguments ....
 *
 * This program will execute "program arguments ...".  Upon
 * receiving a socket connection to port 1234, it will terminate
 * the program.  Upon losing the socket connection, it will reexecute
 * "program arguments ...".  Thus, whenever a program wants
 * exclusive access to the serial port, it connects to port 1234.
 * shared access is returned by dropping the connection to port 1234.
 *
 * The intent of this program is to be an alternate way of attaching
 * a shell to a serial port the init process via /etc/inittab.  This
 * allows the serial uart to be used as a console.  However, whenever
 * the serial uart needs to be used stand-alone, the connection to port
 * 1234 causes the login/shell processes to go away so that the serial
 * uart is exclusively available for the stand-alone program.
 *
 * Thus, in /etc/inittab we normally see something like:
 *
 *   T0:23:respawn:/sbin/getty -L ttyS0 115200 vt100
 *
 * gets replaced by:
 *
 *   T0:23:respawn:/etc/ttyshare /bin/sh
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <strings.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/select.h>
#include <netinet/in.h>
#include <unistd.h>

static int child_fork(char *arguments[], char *environment[]);
static void child_kill(int child_pid);

int main(
  int arguments_count,
  char *arguments[],
  char *environment[])
{
    int child_pid;
    int client_socket;
    int file_number_maximum;
    struct hostent *host_entry;
    int listen_socket;
    int option_value;
    struct sockaddr_in server_address;
    int result;
    int index;

    (void)printf("Hello, World!\n");

    /* Allocate a socket: */
    listen_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (listen_socket < 0) {
	(void)printf("Socket open failed\n");
	return 1;
    }
    
    /* Mark the socket so that the address can be reused: */
    option_value = 1;
    if (setsockopt(listen_socket, SOL_SOCKET, SO_REUSEADDR,
      (void *)&option_value, sizeof option_value) < 0) {
	(void)printf("setsockopt reuse address failed\n");
        return 1;
    }

    /* Mark the socket as keep alive so we know when it goes away: */
    option_value = 1;
    if (setsockopt(listen_socket, SOL_SOCKET, SO_KEEPALIVE,
      (void *)&option_value, sizeof option_value) < 0) {
	(void)printf("setsockopt keep alive failed\n");
        return 1;
    }

    /* Bind port 1234 to {listen_socket}: */
    bzero((char *)&server_address, sizeof(server_address));
    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = INADDR_ANY;
    server_address.sin_port = htons(1234);
    
    /* Sometimes bind(2) can not get connected; so we try a number of times */
    for (index = 0; index < 20; index++) {
	struct timeval timeout;

        result = bind(listen_socket,
	  (struct sockaddr *)&server_address, sizeof(server_address));
	if (result >= 0) {
	    break;
	}
	(void)fprintf(stderr, "#");

	/* Sleep for 1 second: */
	timeout.tv_sec = 1;
	timeout.tv_usec = 0;
	select(1, 0, 0, 0, &timeout);
    }
    if (result < 0) {
	(void)printf("ttyshare: bind failed\n");
	return 1;
    }

    /* Now start listening for connections: */
    if (listen(listen_socket, 1) < 0) {
	(void)printf("ttyshare: listen failed\n");
	return 1;
    }

    /* Loop until done: */
    child_pid = child_fork(arguments + 1, environment);
    client_socket = -1;
    while (1) {
	struct sockaddr_in client_address;
	socklen_t client_length;
	int count;

	/* Block on either a read or accept: */
	if (client_socket >= 0) {
	    /* Block on a read from {client_socket}: */
	    int amount_read;
	    char buffer[20];

	    amount_read = read(client_socket, (void *)buffer, sizeof(buffer));
	    if (amount_read == 0) {
		/* We have an end of file: */
		(void)printf("ttyshare lost connection\n");
		(void)close(client_socket);
		/* Set client_socket to -1 to force an accept() next time: */
		client_socket = -1;
	        child_pid = child_fork(arguments + 1, environment);
	    } /* else ignore whatever comes in: */
	} else {
	    /* Block on an accept from {server_socket}: */
	    client_length = sizeof(client_address);
	    client_socket = accept(listen_socket,
	      (struct sockaddr *)&client_address, &client_length);
	    if (client_socket < 0) {
		(void)printf("ttyshare accept failed\n");
	    } else {
		(void)printf("ttyshare accepted a connection\n");
		child_kill(child_pid);
	    }
	}
    }

    return 0;
}

static int child_fork(
  char *arguments[],
  char *environment[])
{
    /*  */
    int child_pid;

    child_pid = fork();
    if (child_pid == 0) {
	/* We are in the child fork: */
	int result;

	(void)printf("forking_child\n");
	(void)fflush(stdout);
	result = execve(arguments[0], arguments, environment);
	(void)printf("Child exec failed\n");
	exit(1);
    }
    return child_pid;
}

static void child_kill(
  int child_pid)
{
    int result;

    if (child_pid != 0) {
	result = kill(child_pid, SIGHUP);
	if (result < 0) {
	    (void)printf("kill failed\n");
	}
    }
}

