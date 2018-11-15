#!/usr/bin/python3
from collections import OrderedDict

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

def txts_to_txtc(txt_original):
    global caracteres, caracteres_maiusculos, mapa_str_char
    txt = list(OrderedDict.fromkeys(txt_original.replace("->", " ").replace("|", " ").replace("\n", " ").split()))

    for t in txt:
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

    for k, v in mapa_str_char.items():
        txt_original = txt_original.replace(v, k)

    return txt_original

def isterminal(inp):
    return inp.islower() or inp.isdigit()

ordem_producoes = []
tokens = {("for", "FOR"), ("int", "INT"), ("while", "WHILE")}

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

def testa_sentenca(s):
    pilha = ["$", prod_inicial]
    entrada = list(s)
    entrada.append("$")
    acao = ""
    try:
        while pilha != ["$"] or entrada != ["$"]:
            p = pilha[len(pilha) - 1]
            e = entrada[0]
            print("Pilha: " + str(pilha) + "\nEntrada: " + str(entrada) + "\nAção: " + acao + "\n")
            if p == "E":
                pilha.pop()
                acao = "Sentença vazia."
            elif isterminal(p):
                if p == e:
                    pilha.pop()
                    entrada.pop(0)
                    acao = "Reconhece terminal."
                else:
                    print("Erro.")
            else:
                pilha.pop()
                prod = list(tabela[p][e][1])[::-1]
                pilha.extend(prod)
                acao = str(tabela[p][e][0]) + " -> " + str(tabela[p][e][1])
        print("Pilha: " + str(pilha) + "\nEntrada: " + str(entrada) + "\nAção: Aceita.")
    except:
        print("Erro ao reconhecer gramática.")

if __name__ == '__main__':
    txt = "teste -> FOR teste | outro\n" \
        "outro -> WHILE outro | WHILE"
    ler_input(txt)

    print("Inicial: " + prod_inicial)

    for nt in nts:
        first(nt)
    
    print("Firsts: ")
    for k, v in firsts.items():
            print(k + ": " + str(v))

    input("")

    for nt in nts:
        follows[nt] = []

    for nt in nts:
        atual = nt
        follow(nt)
        #follows[nt] = follow(nt)
    
    print("Follows: ")
    for k, v in follows.items():
            print(k + ": " + str(v))

    input("")
    
    cria_tabela()
    
    print("Tabela preditiva: ")
    for k, v in tabela.items():
        print (k + ": ")
        for k1, v1 in v.items():
            print(k1 + " = " + str(v1))
        print("")

    print(tabela)

    testa_sentenca(input("Digite uma sentença para reconhecer: "))