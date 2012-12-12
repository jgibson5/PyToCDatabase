#include	"unp.h"



void
str_echo(int sockfd)
{
	char		arg[16];
	ssize_t		n;
	char		line[MAXLINE];

	printf("here\n");
	for ( ; ; ) {
		if ( (n = Readline(sockfd, line, MAXLINE)) == 0)
			return;		/* connection closed by other end */

		if (sscanf(line, "GET /%s http/1.1\n", arg) == 1) {
			printf("1 %s\n%s\n", line, arg);
			n = strlen(line);
			Writen(sockfd, line, n);
			Close(sockfd);
		} else
			printf("%s\n", line);
			//snprintf(line, sizeof(line), "not valid\n");

		
	}
}

int store_class(int sockfd) {
	return 0;
}
