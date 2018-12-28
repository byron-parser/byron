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

atual = None

cnt_term = []

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
            #print("E encontrado.")
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

    #print(mapa_str_char)

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
    #print(txt_novo)

    return txt_novo


#print(str_to_char("AYYLMAO"))
#print(char_to_str(list(mapa_str_char.keys())[list(mapa_str_char.values()).index("AYYLMAO")]))

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
        
        for p in producoes:
            ordem_producoes.append((lado_esq, p))

    cnt_term = list(set(cnt_term))
    cnt_term.append("$")

def first(nt, i=0):
    if nt in nts:
        firsts[nt] = []
        for p in gramatica[nt]:
            if isterminal(p[0]) or p == "E":
                firsts[nt].append(p[0])
            elif nt != p[i]:
                #print(gramatica)
                if "E" in gramatica[p[i]] and len(p)>1:
                    first(p[i+1])
                    firsts[nt].extend(firsts[p[i+1]])
                first(p[i])
                firsts[nt].extend(firsts[p[i]])
        firsts[nt] = set(firsts[nt])

def follow(nt):
    global prod_inicial, atual
    indices = []
    if nt == prod_inicial:
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

estados = []
ests_percorridos = []
inicial_anterior = prod_inicial

gotos = []

def aumenta_gramatica():
    global prod_inicial, inicial_anterior
    estado = []
    
    #nts.insert(0, "Z")
    gramatica["Z"] = [prod_inicial]
    inicial_anterior = prod_inicial
    prod_inicial = "Z"
    
    estado.append(("Z", inicial_anterior, 0))
    expande(estado, ("Z", inicial_anterior, 0))
    estados.append(estado)
    
    ests_str = estado
    ests_str = ""
    for est in estado:
        est_str = []
        for letra in est[1]:
            if letra != "Z":
                est_str.append(char_to_str(letra))
            else:
                est_str.append("Z")
        est_str.insert(est[2], "●")
        est_str = "".join([f"{e} " for e in est_str])
        ests_str += f"{est_str.strip()}, "
    ests_str = ests_str[:-2]
        
    #estado_str = "Z => ●" + inicial_anterior

    #print("i0: " + str(ests_str))
    gotos.append("i0: " + str(ests_str))

sts = []
prontos = []

def expande(c, s):
    esq, prod, pos = s
    if pos < len(prod):
        if prod[pos] in nts and s not in prontos:
            for prd in gramatica[prod[pos]]:
                if (prod[pos], prd, 0) not in c:
                    c.append((prod[pos], prd, 0))
                    prontos.append(s)
                    expande(c, (esq, prd, 0))

novo_estado = []
aux = []

def calcula_estado(est, s):
    global novo_estado, aux, prontos
    for estado in est:
        esq, prod, pos = estado
        if prod[pos] == s:
            if pos < len(prod):
                novo_estado.append((esq, prod, pos+1))
                expande(aux, (esq, prod, pos+1))
                prontos = []
                novo_estado.extend(aux)
        aux = []
    return novo_estado


def pega_simbolos(est):
    simbolos = []
    for e in est:
        esq, prod, pos = e
        if pos < len(prod):
            if prod[pos] not in simbolos:
                simbolos.append(prod[pos])
    return simbolos

def estado_por_simbolo(est, sim):
    res = []
    for e in est:
        esq, prod, pos = e
        if pos < len(prod):
            if prod[pos] == sim:
                res.append(e)
    return res

def percorre_estados(est):
    global novo_estado, ests_percorridos
    for estado in est:
        simb = pega_simbolos(estado)
        for s in simb:
            novo_estado = []
            for e in estado_por_simbolo(estado, s):
                esq, prod, pos = e
                if pos < len(prod):
                    calcula_estado([e], prod[pos])
            if novo_estado not in estados:
                estados.append(novo_estado)
                ests_percorridos.append((estados.index(estado), s, novo_estado))
            else:
                ests_percorridos.append((estados.index(estado), s, estados.index(novo_estado)))
    for e, s, ests in ests_percorridos:
        ests_str = ests
        if not isinstance(ests, int):
            ests_str = ""
            for est in ests:
                est_str = []
                for letra in est[1]:
                    if letra != "Z":
                        est_str.append(char_to_str(letra))
                    else:
                        est_str.append("Z")
                est_str.insert(est[2], "●")
                est_str = "".join([f"{e} " for e in est_str])
                ests_str += f"{est_str.strip()}, "
            ests_str = ests_str[:-2]
        
        #print("goto(" + str(e) + ", " + char_to_str(str(s)) + ") => " + str(ests_str))
        gotos.append("goto(" + str(e) + ", " + char_to_str(str(s)) + ") => " + str(ests_str))
    #print("")

acao = []
desvio = []

def cria_tabela():
    global inicial_anterior
    for e in range(len(estados)):
        acao.append({})
        desvio.append({})
    
    for i in ests_percorridos:
        if isinstance(i[2], int):
            est = estados[i[2]]
            indice_est = i[2]
        else:
            est = i[2]
            indice_est = estados.index(i[2])
        for item in est:
            if i[1] in nts:
                desvio[i[0]][i[1]] = indice_est
                if i[0] == 0 and i[1] == inicial_anterior:
                    idx = estados.index(i[2])
                    acao[idx]["$"] = "aceita"
            else:
                if item[2] <= len(item[1]):
                    acao[i[0]][i[1]] = "s" + str(indice_est)
            if item[2] == len(item[1]) and item[0] != "Z":
                for f in follows[item[0]]:
                    acao[indice_est][f] = "r" + str(ordem_producoes.index((item[0], item[1])) + 1)  

def testa_sentenca(s):
    pilha = [0]
    entrada = list(s)
    entrada.append("$")
    aceita = False
    fz = ""
    string_final = ""
    try:
        while not aceita:
            sm = pilha[len(pilha) - 1]
            ai = entrada[0]
            
            pilha_print = []
            entrada_print = []

            for p in pilha:
                if isinstance(p, str):
                    pilha_print.append(char_to_str(p))
                else:
                    pilha_print.append(p)

            for e in entrada:
                if e != "$":
                    entrada_print.append(char_to_str(e))
                else:
                    entrada_print.append(e)
            
            string_final += "Pilha: " + str(pilha_print) + "\nEntrada: " + str(entrada_print) + "\n"
            if acao[sm][ai][0] == "s":
                pilha.append(ai)
                pilha.append(int(acao[sm][ai][1:]))
                entrada.pop(0)
                fz = "Empilha.\n"
            elif acao[sm][ai][0] == "r":
                smr = int(acao[sm][ai][1:])
                a, beta = ordem_producoes[smr-1]
                
                a_print = char_to_str(a)
                beta_print = ""
                for b in beta:
                    beta_print += f"{char_to_str(b)} "
                beta_print = beta_print[:-1]
                
                r = len(beta)
                for i in range(2*r):
                    pilha.pop()
                x = pilha[len(pilha) - 1]
                pilha.append(a)
                pilha.append(desvio[x][a])
                fz = "Reduz " + str(a_print) + " -> " + str(beta_print) + ".\n"
            elif acao[sm][ai] == "aceita":
                aceita = True
                fz = "Aceita.\n"
            else:
                fz = "Erro ao reconhecer sentença.\n"
            string_final += "Ação: " + fz + "\n"
    except Exception as ex:
        string_final += "Erro ao reconhecer sentença."
        return False
    return aceita

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
    aumenta_gramatica()
    percorre_estados(estados)
    cria_tabela()

'''
if __name__ == '__main__':
    txt = "X -> X FOR T | T\n" \
        "T -> T WHILE F | F\n" \
        "F -> INT X FLOAT | STRING"
    its = []

    ler_input(txt)
    print("Inicial: " + char_to_str(prod_inicial))

    for nt in nts:
        first(nt)
    
    print("\nFirsts: ")
    for k, v in firsts.items():
            its = []
            for i in v:
                its.append(char_to_str(i))
            print(char_to_str(k) + ": " + str(its))

    for nt in nts:
        follows[nt] = []

    for nt in nts:
        atual = nt
        follow(nt)
    
    print("\nFollows: ")
    for k, v in follows.items():
            its = []
            for i in v:
                if i != "$":
                    its.append(char_to_str(i))
                else:
                    its.append(i)
            print(char_to_str(k) + ": " + str(its))
    
    print("----------------------------")
    
    aumenta_gramatica()
    percorre_estados(estados)
    cria_tabela()
    
    print("Tabela ação: ")
    for i, a in enumerate(acao):
        i_f = False
        for k1, v1 in a.items():
            its = []
            for j in k1:
                if j != "$":
                    its.append(char_to_str(j))
                else:
                    its.append(j)
            print("(" + str(i) + ", " + str(its) + "): " + str(v1))
            i_f = True
        if i_f:
            print("")

    print("Tabela desvio: ")
    for i, d in enumerate(desvio):
        i_g = False
        for k1, v1 in d.items():
            its = []
            for j in k1:
                if j != "$":
                    its.append(char_to_str(j))
                else:
                    its.append(j)
            print("(" + str(i) + ", " + str(its) + "): " + str(v1))
            i_g = True
        if i_g:
            print("")

    #sentenca = input("Digite uma sentença para reconhecer: ")
    sentenca = "int string for string while string float while string for string"
    print(reconhece_sentenca(sentenca))
    #sentenca_chars = reconhece_tokens(sentenca)

    #print(sentenca_chars)

    #print(testa_sentenca(sentenca_chars))
'''