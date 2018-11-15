%{
#define NUMBER  400
#define COMMENT 401
#define TEXT    402
#define COMMAND 403
%}
%%
[ \t]+                ;
[0-9]+  |
[0-9]+\.[0-9]+  |
\.[0-9]+              { return NUMBER;  }
#.*                   { return COMMENT; }
\"[^\"]*\"            { return TEXT;    }
[a-zA-Z][a-zA-Z0-9]+  { return COMMAND; }
\n                    { return '\n';    }
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

