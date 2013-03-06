/* Copyright (c) 2011 by Intelligent Machines Corp. */
/* All rights reserved. */

/*
 * Usage: femtocom [serial_port [baud_rate]]
 *
 * This program will open /dev/tty and {serial_port} and cross connect
 * input and output.  This is very similar to minicom but with very
 * few creature comforts.  Three control-C's in a row will cause the
 * program to terminate.
 *
 * In addition, this program will open a connect to port 1234 on
 * the local host (if possible).  This is the port used by ttyshare
 * to disable the login/shell attached to a serial port.  If the
 * connection does not work, a short message ensues with no further
 * consequences.
 */

#include <fcntl.h>
#include <netdb.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <strings.h>
#include <termios.h>
#include <unistd.h>

static int terminal_open(char* name,
  int baud_rate, struct termios *original_termios);
static int transfer(int from_fd, int to_fd, int *control_c_count, int *shift);
static int ttyshare_socket_open(void);

int main(
  int arguments_count,
  char *arguments[],
  char *environment[])
{
    int done;
    int index;
    int ttyshare_socket;
    int maximum_fd;
    fd_set read_file_set;
    int serial_baud_rate;
    int serial_control_c_count;
    int serial_fd;
    char *serial_name;
    struct termios serial_termios;
    int shift;
    int terminal_baud_rate;
    int terminal_control_c_count;
    int terminal_fd;
    char *terminal_name;
    struct termios terminal_termios;

    /* Set default values: */
    serial_baud_rate = 115200;
    serial_name = "/dev/ttyS0";
    terminal_baud_rate = 115200;
    terminal_name = "/dev/tty";

    /* Parse command line arguments: */
    for (index = 1; index < arguments_count; index++) {
	char *argument;

	argument = arguments[index];
	if (index == 1) {
	    serial_name = argument;
	} else if (index == 2) {
	    serial_baud_rate = atoi(argument);
	} else if (index == 3) {
	    shift = atoi(argument);
	}
     }
    (void)printf("serial='%s' baud=%d shift=%d\n",
      serial_name, serial_baud_rate, shift);

    /* Open a connection to the ttyshare process: */
    ttyshare_socket = ttyshare_socket_open();

    /* Open {terminal_name} at {terminal_baud_rate): */
    terminal_fd =
      terminal_open(terminal_name, terminal_baud_rate, &terminal_termios);
    if (terminal_fd < 0) {
	(void)printf("Terminal open of '%s' at %d baud failed\n",
	  terminal_name, terminal_baud_rate);
	return 1;
    }

    /* Open {serial_name} at {serial_baud_rate): */
    serial_fd = terminal_open(serial_name, serial_baud_rate, &serial_termios);
    if (serial_fd < 0) {
	(void)printf("Serial open of '%s' at %d baud failed\n",
	  serial_name, serial_baud_rate);
	return 1;
    }

    /* Some miscellaneous set up: */
    maximum_fd = terminal_fd;
    if (serial_fd > maximum_fd) {
	maximum_fd = serial_fd;
    }
    serial_control_c_count = 0;
    terminal_control_c_count = 0;

    /* Now copy transfer keystrokes from one device to the other: */
    shift = 0;
    done = 0;
    while (!done) {
	int read_count;

	/* Wait for input from either {terminal_fd} or {serial_fd}: */
	FD_ZERO(&read_file_set);
	FD_SET(terminal_fd, &read_file_set);
	FD_SET(serial_fd, &read_file_set);
	read_count = select(maximum_fd + 1,
	  &read_file_set, (fd_set *)0, (fd_set *)0, (struct timeval *)0);
	if (read_count <= 0) {
	    (void)fprintf(stderr, "read_mask_count=%d\n", read_count);
	    return 1;
	}
	
	/* Copy any data from {terminal_fd} to {serial_fd}: */
	if (FD_ISSET(terminal_fd, &read_file_set)) {
	    done += transfer(terminal_fd,
	      serial_fd, &terminal_control_c_count, &shift);
	}

	/* Copy any data from {serial_fd} to {terminal_fd}: */
	if (FD_ISSET(serial_fd, &read_file_set)) {
	    done += transfer(serial_fd,
	      terminal_fd, &serial_control_c_count, &shift);
	}
    }

    /* Close and restore all of the connections: */
    if (ttyshare_socket >= 0) {
	(void)close(ttyshare_socket);
    }
    (void)tcsetattr(terminal_fd, TCSANOW, &terminal_termios);
    (void)tcsetattr(serial_fd, TCSANOW, &serial_termios);
    (void)close(terminal_fd);
    (void)close(serial_fd);
    return 0;
}

static int transfer(
  int from_fd,
  int to_fd,
  int *control_c_count,
  int *shift)
{
    int amount_read;
    char buffer[1024];
    char character;
    int done;
    int index;
    int read_count;

    done = 0;
    amount_read = read(from_fd, buffer, sizeof(buffer));
    if (amount_read > 0) {
	/* We read {amount_read} bytes of data into {buffer} from {from_fd}: */

	/* Check {buffer} for Control-C's to see if program is over: */
	for (index = 0; index < amount_read; index++) {
	    character = buffer[index];

	    if (character == '\3') {
	      if (++(*control_c_count) >= 3) {
		    done = 1;
		}
	    } else {
		*control_c_count = 0;
		if (character == '\24') {
		    /* Control-T: */
		    *shift = 1;
		} else if (character == '\7') {
		    /* Control-G: */
		    *shift = 0;
		}
	    }
	}

	/* Shift characters: */
	if (*shift) {
	    for (index = 0; index < amount_read; index++) {
		character = buffer[index];
		/* Let all control characters through that are not a
		 * carraige-return, line-feed, or tab.  All other */
		if ((character & 128) == 0) {
		    /* Eight bit is clear: */
		if ((character == '\n') || (character == '\r') ||
		    (character == '\t') || (character >= ' ') )
		    /* All printing characters, carriage-return, line-feed,
		     * and tab are shifted up.  Everything else remains
		     * unshifted. */
		    character |= 0x80;
		} else if ((character & 128) != 0) {
		    /* Eight bit is set; shift {character} down: */
		    character &= 0x7f;
		}
		buffer[index] = character;
	    }
	}

	/* Copy {amount_read} bytes in {buffer} over to {to_fd}: */
	if (write(to_fd, buffer, amount_read) != amount_read) {
	    (void)fprintf(stderr, "Write to {serial_fd} failed\n");
	    return 1;
	}
    }
    return done;
}

static int terminal_open(
  char *name,
  int baud_rate,
  struct termios *original_termios)
{
    int baud_flag;
    int control_flags;
    int terminal_fd;
    struct termios raw_termios;

    /* Compute {baud_flag} from {baud_rate}:*/
    switch (baud_rate) {
      case 0:
	baud_flag = B0;
	break;
      case 50:
	baud_flag = B50;
	break;
      case 75:
	baud_flag = B75;
	break;
      case 110:
	baud_flag = B110;
	break;
      case 150:
	baud_flag = B150;
	break;
      case 200:
	baud_flag = B200;
	break;
      case 300:
	baud_flag = B300;
	break;
      case 600:
	baud_flag = B600;
	break;
      case 1200:
	baud_flag = B1200;
	break;
      case 1800:
	baud_flag = B1800;
	break;
      case 2400:
	baud_flag = B2400;
	break;
      case 4800:
	baud_flag = B4800;
	break;
      case 9600:
	baud_flag = B9600;
	break;
      case 19200:
	baud_flag = B19200;
	break;
      case 38400:
	baud_flag = B38400;
	break;
      case 57600:
	baud_flag = B57600;
	break;
      case 115200:
	baud_flag = B115200;
	break;
      case 230400:
	baud_flag = B230400;
	break;
      default:
	return -1;
	break;
    }

    /* Open {name} in read/write non-blocking mode: */
    terminal_fd = open(name, O_RDWR | O_NONBLOCK);
    if (terminal_fd < 0) {
	(void)fprintf(stderr, "Unable to open '%s'\n", name);
	return -2;
    }

    /* Grab original termios: */
    if (tcgetattr(terminal_fd, original_termios) != 0) {
	(void)fprintf(stderr,
	  "Unable to get original termios for '%s'\n", name);
	return -3;
    }

    /* Initalize {terimios} structure: */
    cfmakeraw(&raw_termios);
    control_flags = raw_termios.c_cflag;
    control_flags &= ~CRTSCTS;
    control_flags |= CREAD | CLOCAL | HUPCL;
    raw_termios.c_cflag = control_flags;
    raw_termios.c_cc[VMIN] = 1;
    raw_termios.c_cc[VTIME] =  0;

    /* Set the input and output speed of {termios}: */
    if ((cfsetispeed(&raw_termios, baud_flag) != 0)  ||
      (cfsetospeed(&raw_termios, baud_flag) != 0)) {
	return -4;
    }

    /* Bind the {termios} values to {terminal_fd}: */
    if (tcsetattr(terminal_fd, TCSANOW, &raw_termios) < 0) {
	return -5;
    }

    return terminal_fd;
}

int ttyshare_socket_open(void)
{
    int socket_fd;
    int n;
    struct sockaddr_in server_address;
    struct hostent *server;
    char buffer[256];

    /* Lookup internet address for "localhost": */
    server = gethostbyname("localhost");
    if (server == NULL) {
	(void)fprintf(stderr, "ERROR, can not find localhost\n");
        exit(1);
    }

    /* Allocate a TCP socket: */
    socket_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (socket_fd < 0) {
	(void)fprintf(stderr, "ERROR opening socket\n");
	exit(1);
    }

    /* Copy the require information in to open the connection: */	
    bzero((void *)&server_address, sizeof(server_address));
    server_address.sin_family = AF_INET;
    bcopy((void *)server->h_addr,
      (void *)&server_address.sin_addr.s_addr, server->h_length);
    server_address.sin_port = htons(1234);

    /* Attempt to open the connection: */
    if (connect(socket_fd,
      (struct sockaddr *)&server_address, sizeof(server_address)) < 0) {
	(void)fprintf(stderr, "Could not connect to ttyshare port 1234\n");
	(void)close(socket_fd);
	socket_fd = -1;
    }
    return socket_fd;
}
