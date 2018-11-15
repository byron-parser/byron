gramatica = {}
tabela = {}
prod_inicial = None

nts = []
firsts = {}
follows = {}
done = []

atual = None

cnt_term = []


def isterminal(inp):
    return inp.islower() or inp.isdigit()

ordem_producoes = []

def ler_input(txt):
    global prod_inicial, cnt_term
    primeiro = True

    #print("Entre com uma gramática (enter para terminar):")

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
    
    print("i0: " + str(estado))
    gotos.append("i0: " + str(estado))

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
        print("goto(" + str(e) + ", " + str(s) + ") -> " + str(ests))
        gotos.append("goto(" + str(e) + ", " + str(s) + ") -> " + str(ests))
    print("")

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
            string_final += "Pilha: " + str(pilha) + "\nEntrada: " + str(entrada) + "\n"
            if acao[sm][ai][0] == "s":
                pilha.append(ai)
                pilha.append(int(acao[sm][ai][1:]))
                entrada.pop(0)
                fz = "Empilha.\n"
            elif acao[sm][ai][0] == "r":
                smr = int(acao[sm][ai][1:])
                a, beta = ordem_producoes[smr-1]
                r = len(beta)
                for i in range(2*r):
                    pilha.pop()
                x = pilha[len(pilha) - 1]
                pilha.append(a)
                pilha.append(desvio[x][a])
                fz = "Reduz " + str(a) + "->" + str(beta) + ".\n"
            elif acao[sm][ai] == "aceita":
                aceita = True
                fz = "Aceita.\n"
            else:
                fz = "Erro ao reconhecer sentença.\n"
            string_final += "Ação: " + fz + "\n"
    except:
        string_final += "Erro ao reconhecer sentença."
    return string_final

if __name__ == '__main__':
    ler_input()
    print("Inicial: " + prod_inicial)
    
    for nt in nts:
        first(nt)
    
    print("\nFirsts: ")
    for k, v in firsts.items():
            print(k + ": " + str(v))

    for nt in nts:
        follows[nt] = []

    for nt in nts:
        atual = nt
        follow(nt)
    
    print("\nFollows: ")
    for k, v in follows.items():
            print(k + ": " + str(v))
    
    print("----------------------------")
    
    aumenta_gramatica()
    percorre_estados(estados)
    cria_tabela()
    
    print("Tabela ação: ")
    for i, a in enumerate(acao):
        i_f = False
        for k1, v1 in a.items():
            print("(" + str(i) + ", " + str(k1) + "): " + str(v1))
            i_f = True
        if i_f:
            print("")

    print("Tabela desvio: ")
    for i, d in enumerate(desvio):
        i_g = False
        for k1, v1 in d.items():
            print("(" + str(i) + ", " + str(k1) + "): " + str(v1))
            i_g = True
        if i_g:
            print("")

    testa_sentenca(input("Digite uma sentença para reconhecer: "))
