#include	"unp.h"


int read_all(int sockfd, char* buf, ssize_t max) {
	ssize_t		n;
	char		line[MAXLINE];
	printf("CALLED\n");
    Py_Initialize();
    printf("1\n");
	while (Readline(sockfd, line, MAXLINE) > 0) {
		printf("2\n");
		n = strlen(buf);
		if (strlen(buf) + strlen(line) < max) {
			printf("3\n");
			strcat(buf, "print 'please print ");
			strcat(buf, line);
			strcat(buf, "'");
			printf("4\n");
			printf("%s\n", buf);
			PyRun_SimpleString(buf);
		} else {
			printf("no\n");
		}
	}
    Py_Finalize();
	return max;
}

void
str_echo(int sockfd)
{
	// char*		arg[16];
	ssize_t		n;
	char		line[MAXLINE];
	ssize_t		max = 128;
	char		buf[max];

	read_all(sockfd, buf, max);
	for ( ; ; ) {
		if ( (n = Readline(sockfd, line, MAXLINE)) == 0) {
			return;		/* connection closed by other end */
		}

		// printf("%s\n", line);
		// if (sscanf(line, "%s", arg) == 1) {
		// 	printf("1 %s\n", arg);
		// 	n = strlen(line);
		// 	printf("%zd\n", n);
		// 	// Writen(sockfd, line, n);
		// } else {
		// 	printf("%s\n", line);
		// 	//snprintf(line, sizeof(line), "not valid\n");
		// }
	}
}

// int store_class(int sockfd) {
// 	return 0;
// }
