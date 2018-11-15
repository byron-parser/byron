%{
#define IP 666
%}
%%

(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9]\.){3}(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])  { return IP; } //Reconhece enderecos IP

%%

#include <stdio.h>

main(argc,argv)
int argc;
char *argv[];
{
  int val;

  while (val = yylex())
     printf("Token: %d\n",val);
}
