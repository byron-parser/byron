%{
#define OK 1
#define ERRO 0
%}
%%

([A-Z]{3}-[0-9]{4}) { return OK; }

%%

#include <stdio.h>

main(argc,argv)
int argc;
char *argv[];
{
  int val;

  while (val = yylex()){
  if(val == OK)
     printf("Token reconhecido");
  else if(val == ERRO)
    printf("Token nao reconhecido");
 else
    printf("Erro");
    }
}
