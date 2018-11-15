%{
#define OK  1
#define ERRO 0
%}
%%
[(][0-9][0-9][)][0-9][0-9][0-9][0-9][-][0-9][0-9][0-9][0-9] { return OK; }
[0-9][0-9][0-9][0-9][0-9][0-9][-][0-9][0-9][0-9][0-9] { return OK; }
[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9] { return OK; }
%%

#include <stdio.h>

main(argc,argv)
int argc;
char *argv[];
{
  int val;

  while (val = yylex()) {
	if (val = 1) {
		printf("Numero valido");
	}
	else if (val = 0) {
		printf("Numero invalido");
	}
	else {
		printf("Erro");
	}
  }
  
}

