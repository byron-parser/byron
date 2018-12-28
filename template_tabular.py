# -*- coding: utf-8 -*-

# Copyright (C) 2018 Gabriel Felipe Huwe.
# This file is part of Byron.

# Byron is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.

# Byron is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Byron.  If not, see <https://www.gnu.org/licenses/>.

from collections import OrderedDict
import shlex
import re

gramatica = {}
tabela = {}
prod_inicial = None

nts = []
firsts = {}
follows = {}
done = []

cnt_term = []

atual = None

caracteres = list("abcdefghijklmnopqrstuvwxyz")
caracteres_maiusculos = list("ABCDFGHIJKLMNOPRSTUVWXY")
mapa_str_char_lst = []
mapa_str_char = OrderedDict()

def char_to_str(c):
    return mapa_str_char[c]

def str_to_char(s):
    for k, v in mapa_str_char.items():
        if s == v:
            return k
    return None

def txts_to_txtc(txt_original):
    global caracteres, caracteres_maiusculos, mapa_str_char
    txt = list(OrderedDict.fromkeys(txt_original.replace("->", " ").replace("|", " ").replace("\n", " ").split()))

    for t in txt:
        #print(t)
        if t == "E":
            mapa_str_char_lst.append(("E", "E"))
        else:
            tup = False
            for tupla in tokens:
                if t == tupla[1]:
                    tup = True
            if tup:
                c = caracteres.pop(0)
            else:
                c = caracteres_maiusculos.pop(0)
            mapa_str_char_lst.append((c, t))
    
    mapa_str_char = OrderedDict(mapa_str_char_lst)

    mapa_invertido = {v: k for k, v in mapa_str_char.items()}
    
    txt_novo = ""
    for linha in txt_original.splitlines():
        linha_nova = ""
        for palavra in linha.split():
            if palavra in mapa_invertido.keys():
                nova_palavra = mapa_invertido[palavra]
            else:
                nova_palavra = palavra
            linha_nova += nova_palavra
        txt_novo += linha_nova + "\n"

    return txt_novo


def isterminal(inp):
    return inp.islower() or inp.isdigit()

ordem_producoes = []
tokens = {("for", "FOR"), ("int", "INT"), ("while", "WHILE"), ("float", "FLOAT"), ("string", "STRING")}

def ler_input(txt):
    global prod_inicial, cnt_term
    primeiro = True

    #print("Entre com uma gramática (enter para terminar):")
    txt = txts_to_txtc(txt)
    texto = txt.splitlines()

    for linha in texto:
            linha = linha.replace(" ", "")

            for d in linha:
                if isterminal(d):
                    cnt_term.append(d)

            lados = linha.split("->")
            lado_esq, lado_dir = lados[0], lados[1]
            nts.append(lado_esq)
            
            producoes = lado_dir.split("|")

            if primeiro:
                prod_inicial = lado_esq
                primeiro = False

            gramatica[lado_esq] = producoes

    cnt_term = list(set(cnt_term))
    cnt_term.append("$")

def first(nt, i=0):
    if nt in nts:
        firsts[nt] = []
        for p in gramatica[nt]:
            if isterminal(p[0]) or p == "E":
                firsts[nt].append(p[0])
            else:
                if "E" in gramatica[p[i]] and len(p)>1:
                    first(p[i+1])
                    firsts[nt].extend(firsts[p[i+1]])
                first(p[i])
                firsts[nt].extend(firsts[p[i]])
        firsts[nt] = set(firsts[nt])

def follow(nt):
    global prod_inicial, atual
    #_follows = []
    indices = []
    if nt == prod_inicial:
        #_follows.append("$")
        follows[nt].append("$")
    for k, prods in gramatica.items():
        for prod in prods:
            if nt in prod:
                indices.append((k, prod, prod.index(nt)))

    for idx in indices:
        esq, prod, i = idx
        
        if i == len(prod)-1:
            if prod[i] != esq:
                if not follows[esq]:
                    follow(esq)
                follows[nt].extend(follows[esq])
                
        
        elif prod[i+1] in nts:
            follows[nt].extend(firsts[prod[i+1]])
            
            try:
                follows[nt].remove("E")
            except:
                pass
            

            if "E" in firsts[prod[i+1]]:
                if not follows[esq]:
                    follow(esq)
                follows[nt].extend(follows[esq])
        
        else:
            follows[nt].append(prod[i+1])
    follows[nt] = list(set(follows[nt]))
 
def cria_tabela():
    for k, prods in gramatica.items():
        tabela[k] = {}
        for prod in prods:
            if prod[0] in nts:
                for f in firsts[prod[0]]:
                    if f != "E":
                        tabela[k][f] = (k, prod)
            elif "E" == prod[0]:
                for b in follows[k]:
                    tabela[k][b] = (k, prod)
            else:
                tabela[k][prod[0]] = (k, prod)

passos = 0

def testa_sentenca(s):
    global passos
    pilha = ["$", prod_inicial]
    entrada = list(s)
    entrada.append("$")
    acao = ""
    string_final = ""
    erro = False
    try:
        while pilha != ["$"] or entrada != ["$"]:
            if passos > 1000:
                erro = True
                break
            passos += 1
            p = pilha[len(pilha) - 1]
            e = entrada[0]

            pilha_print = []
            entrada_print = []

            for pi in pilha:
                if pi != "$" and pi != "E":
                    pilha_print.append(char_to_str(pi))
                elif pi == "E":
                    pilha_print.append("ε")
                else:
                    pilha_print.append(pi)

            for en in entrada:
                if en != "$":
                    entrada_print.append(char_to_str(en))
                else:
                    entrada_print.append(en)

            if p == "E":
                pilha.pop()
                acao = "Sentença vazia.\n"
            elif isterminal(p):
                if p == e:
                    pilha.pop()
                    entrada.pop(0)
                    acao = "Reconhece terminal.\n"
                else:
                    #print("Erro.\n")
                    erro = True
            else:
                pilha.pop()
                prod = list(tabela[p][e][1])[::-1]
                pilha.extend(prod)
                pe_print = ""
                for b in tabela[p][e][1]:
                    if b == "E":
                        pe_print += "ε "
                    else:
                        pe_print += f"{char_to_str(b)} "
                pe_print = pe_print[:-1]
                acao = char_to_str(tabela[p][e][0]) + " -> " + pe_print + "\n"
            string_final += "Pilha: " + str(pilha_print) + "\nEntrada: " + str(entrada_print) + "\nAção: " + acao + "\n"
    except:
        erro = True
        #string_final += "Erro ao reconhecer sentença.\n"
    if not erro:
        pilha_print = []
        entrada_print = []

        for pi in pilha:
            if pi != "$" and pi != "E":
                pilha_print.append(char_to_str(pi))
            elif pi == "E":
                pilha_print.append("ε")
            else:
                pilha_print.append(pi)

        for en in entrada:
            if en != "$":
                entrada_print.append(char_to_str(en))
            else:
                entrada_print.append(en)
        string_final += "Pilha: " + str(pilha_print) + "\nEntrada: " + str(entrada_print) + "\nAção: Aceita."
    else:
        string_final += "Erro ao reconhecer sentença."

    return not erro

def reconhece_tokens(texto):
    texto_separado = shlex.split(texto, posix=False)
    texto_tokenizado = ""

    for unidade in texto_separado:
        literal = False
        for token in tokens:
            if f"^{unidade}$" == f"^{token[0]}$":
                texto_tokenizado += f"{str_to_char(token[1])}"
                literal = True
                break
        if not literal:
            for token in tokens:
                if re.match(f"^{token[0]}$", unidade):
                    texto_tokenizado += f"{str_to_char(token[1])}"
                    break

    return texto_tokenizado

def reconhece_sentenca(sentenca):
    #sentenca = "int string for string while string float while string for string"
    sentenca_chars = reconhece_tokens(sentenca)

    #print(sentenca_chars)

    return testa_sentenca(sentenca_chars)

def prepara_dados():
    global nts, atual, estados
    for nt in nts:
        first(nt)    
    for nt in nts:
        follows[nt] = []
    for nt in nts:
        atual = nt
        follow(nt)
    cria_tabela()


if __name__ == '__main__':
    txt = "X -> T Y\n" \
    "Y -> FOR T Y | E\n" \
    "T -> F M\n" \
    "M -> WHILE F M | E\n" \
    "F -> INT X FLOAT | STRING"
    ler_input(txt)

    print("Inicial: " + prod_inicial)

    for nt in nts:
        first(nt)
    
    print("Firsts: ")
    for k, v in firsts.items():
            print(k + ": " + str(v))

    #input("")

    for nt in nts:
        follows[nt] = []

    for nt in nts:
        atual = nt
        follow(nt)
        #follows[nt] = follow(nt)
    
    print("Follows: ")
    for k, v in follows.items():
            print(k + ": " + str(v))

    #input("")
    
    cria_tabela()
    
    print("Tabela preditiva: ")
    for k, v in tabela.items():
        print (k + ": ")
        for k1, v1 in v.items():
            print(k1 + " = " + str(v1))
        print("")

    print(tabela)

    sentenca = "int string for string while string float while string for string"
    sentenca_chars = reconhece_tokens(sentenca)

    print(sentenca_chars)

    print(testa_sentenca(sentenca_chars))
