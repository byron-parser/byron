#!/usr/bin/python3

import shlex
import re
import readline

tokens = []

#print("Input de tokens (regex seguido por símbolo, separado por ':', 'fim' encerra):")

#entrada = input()
def ler_input(entrada):
    global tokens
    tokens_txt = ""
    linhas = entrada.splitlines()
    for linha in linhas:
        token = linha.split(":")
        tokens.append((token[0], token[1]))
        tokens_txt += f"{token[0]}: {token[1]}\n"
    return tokens_txt

#texto_entrada = input() 
#tokens = [("for", "FOR"), ("if", "IF"), ("([a-z]|[A-Z]|[0-9]|_])+", "ID")]
#texto_entrada = "for abc_123 if true"
def reconhece(texto):
    texto_separado = shlex.split(texto, posix=False)
    texto_tokenizado = ""

    for unidade in texto_separado:
        literal = False
        for token in tokens:
            if f"^{unidade}$" == f"^{token[0]}$":
                texto_tokenizado += f"{token[1]} "
                literal = True
                break
        if not literal:
            for token in tokens:
                if re.match(f"^{token[0]}$", unidade):
                    texto_tokenizado += f"{token[1]}({unidade}) "
                    break

    return texto_tokenizado