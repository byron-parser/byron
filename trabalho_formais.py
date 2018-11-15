from itertools import groupby
from operator import itemgetter
import random
import string
gramaticas_livres = []

def menu():
    sair = False
    while not sair:
        print("1. Criar")
        print("2. Acessar")
        print("3. Editar")
        print("4. Remover")
        print("5. Eliminar simbolos inuteis")
        print("6. Retirar producoes vazias")
        print("7. Fatorar")
        print("8. Eliminar recursoes a esquerda")
        print("9. Sair")
        opcao = int(input("> "))
        if(opcao == 1):
            adiciona_gramatica()
        elif(opcao == 2):
            acessa_gramatica()
        elif(opcao == 3):
            edita_gramatica()
        elif(opcao == 4):
            remove_gramatica()
        elif(opcao == 5):
            elimina_inuteis()
        elif(opcao == 6):
            retira_vazias()
        elif(opcao == 7):
            fatora()
        elif(opcao == 8):
            elimina_recursao()
        else:
            sair = True


def adiciona_lista(lista, texto):
    continua = True
    while (continua):
        inp = str(input(texto + ": (';' para terminar) "))
        if (inp == ';'):
            continua = False
        else:
            lista.append(inp)

def cria_producoes(prods, naoterm, term):
    print("Producoes:")
    print("Palavra vazia: \"vazia\" (ou ε)")
    continua = True
    while(continua):
        lado_esq = str(input("Lado esquerdo: (';' para terminar) "))
        if (lado_esq == ';'):
            continua = False
        else:
            if lado_esq in naoterm:
                lado_dir = []
                prod = {'esq': lado_esq, 'dir': lado_dir, 'fertil': None, 'visitada': False}
                continua_interno = True
                while continua_interno:
                    p = str(input("Lado direito: (';' para terminar) "))
                    if (p == ';'):
                        continua_interno = False
                    else:
                        if p == 'vazia':
                            lado_dir.append("ε")
                        else:
                            lado_dir.append(p)
                prods.append(prod)
            else:
                print("Lado esquerdo invalido.")

def adiciona_gramatica():
    nome = str(input("Nome: "))
    nao_terminais = []
    terminais = []
    producoes = []
    print("Primeiro nao-terminal adicionado sera producao inicial.")
    adiciona_lista(nao_terminais, "Nao-terminal")
    adiciona_lista(terminais, "Terminal")
    cria_producoes(producoes, nao_terminais, terminais)
    gram = {"nome": nome,
            "naoterm": nao_terminais,
            "term": terminais,
            "prods": producoes,
            "inic": nao_terminais[0]
            }
    gramaticas_livres.append(gram)

def acessa_gramatica():
    nome = str(input("Nome: "))
    gramatica_selecionada = None
    for g in gramaticas_livres:
        if g["nome"] == nome:
            gramatica_selecionada = g
            break
    if gramatica_selecionada != None:
        print("Nome: " + gramatica_selecionada["nome"])
        print("Nao-terminais:")
        for nt in gramatica_selecionada["naoterm"]:
            print(nt)
        print("Terminais:")
        for t in gramatica_selecionada["term"]:
            print(t)
        print("Producoes:")
        for p in gramatica_selecionada["prods"]:
            print("Producao " + p["esq"] + ":")
            for e in p["dir"]:
                print(e)
        print("Producao inicial: " + gramatica_selecionada["inic"])
    else:
        print("Gramatica não encontrada.")

def edita_gramatica():
    nome = str(input("Nome: "))
    gramatica_selecionada = None
    for g in gramaticas_livres:
        if g["nome"] == nome:
            gramatica_selecionada = g
            break
    if gramatica_selecionada != None:
        if (str(input("Adicionar nao-terminais? (S/n) "))) != "n":
            adiciona_lista(gramatica_selecionada["naoterm"], "Nao-terminal")
        if (str(input("Adicionar terminais? (S/n) "))) != "n":
            adiciona_lista(gramatica_selecionada["term"], "Terminal")
        if (str(input("Adicionar producoes? (S/n)"))) != "n":
            cria_producoes(gramatica_selecionada["prods"], gramatica_selecionada["naoterm"],
                           gramatica_selecionada["term"])
    else:
        print("Gramatica não encontrada.")

def remove_gramatica():
    nome = str(input("Nome: "))
    for g in gramaticas_livres:
        if g["nome"] == nome:
            gramatica_selecionada = g
            break
    if gramatica_selecionada != None:
        gramaticas_livres.remove(gramatica_selecionada)
        print("Gramatica removida.")
    else:
        print("Gramatica não encontrada.")

def recur_fertil(gram, prod):
    for d in prod["dir"]:
        num_nt = 0
        num_fert = 0
        for l in list(d):
            if l in gram["naoterm"]:
                num_nt += 1
                for p2 in gram["prods"]:
                    if p2["esq"] == l:
                        if p2['fertil'] == True:
                                num_fert += 1
                                p2["visitada"] == True
                        elif p2['visitada'] == False:
                            p2['visitada'] = True
                            p2['fertil'] = recur_fertil(gram, p2)
        if num_nt == num_fert or num_nt == 0:
            prod['fertil'] = True
    prod['visitada'] = True
    if prod['fertil'] == True:
        return True
    else:
        return False

def elimina_inuteis():
    nome = str(input("Nome: "))
    for g in gramaticas_livres:
        if g["nome"] == nome:
            gramatica_selecionada = g
            break
    if gramatica_selecionada != None:
        for p in gramatica_selecionada["prods"]:
            for d in p["dir"]:
                num_nterms = 0
                for l in list(d):
                    if l in gramatica_selecionada["naoterm"]:
                        num_nterms += 1
                if num_nterms == 0 or d == 'ε':
                    p["fertil"] = True
        for p in gramatica_selecionada["prods"]:
            p['fertil'] = recur_fertil(gramatica_selecionada, p)
        for p in gramatica_selecionada["prods"]:
            if p['fertil'] != True:
                for p2 in gramatica_selecionada["prods"]:
                    for d in p2['dir']:
                        for l in list(d):
                            if l == p["esq"]:
                                p2['dir'].remove(d)
                                break
        for p in gramatica_selecionada["prods"]:
            if p['fertil'] != True:
                gramatica_selecionada["naoterm"].remove(p["esq"])
                gramatica_selecionada["prods"].remove(p)
        for t in gramatica_selecionada["term"]:
            n_refs = 0
            for p in gramatica_selecionada['prods']:
                for d in p['dir']:
                    for l in list(d):
                        if t == l:
                            n_refs += 1
            if n_refs == 0:
                gramatica_selecionada["term"].remove(t)
        for p in gramatica_selecionada['prods']:
            n_refs = 0
            for p2 in gramatica_selecionada['prods']:
                for d in p2['dir']:
                    for l in list(d):
                        if p['esq'] != p2['esq'] and l == p['esq']:
                            n_refs += 1
            if gramatica_selecionada['inic'] != p['esq'] and n_refs == 0:
                gramatica_selecionada['naoterm'].remove(p['esq'])
                gramatica_selecionada['prods'].remove(p)
        for t in gramatica_selecionada["term"]:
            n_refs = 0
            for p in gramatica_selecionada['prods']:
                for d in p['dir']:
                    for l in list(d):
                        if t == l:
                            n_refs += 1
            if n_refs == 0:
                gramatica_selecionada["term"].remove(t)
    else:
        print("Gramatica não encontrada.")

def chama_r_vazias(gramatica_selecionada):
    for p in gramatica_selecionada["prods"]:
        inicial = False
        if "ε" in p["dir"]:
            if p["esq"] == gramatica_selecionada["inic"]:
                inicial = True
            for p2 in gramatica_selecionada["prods"]:
                aux = []
                for d in p2["dir"]:
                    novo = d
                    for l in list(d):
                        if l == p["esq"]:
                            novo = novo.replace(l, '')
                            if novo == '':
                                novo = 'ε'
                    aux.append(novo)
                for a in aux:
                    if a not in p2["dir"]:
                        p2["dir"].append(a)
            p["dir"].remove("ε")
            if inicial:
                achou = False
                novo_simb = ''
                while not achou:
                    novo_simb = str(random.choice(string.ascii_uppercase))
                    if novo_simb not in gramatica_selecionada["naoterm"]:
                        achou = True
                        novo_naoterm = novo_simb
                        nova_prod = {'esq': novo_simb, 'dir': [p['esq'], 'ε'], 'fertil': True, 'visitada': False}
    if inicial:
        gramatica_selecionada["inic"] = novo_naoterm
        gramatica_selecionada["naoterm"].append(novo_naoterm)
        gramatica_selecionada["prods"].append(nova_prod)

def retira_vazias():
    nome = str(input("Nome: "))
    for g in gramaticas_livres:
        if g["nome"] == nome:
            gramatica_selecionada = g
            break
    if gramatica_selecionada != None:
        chama_r_vazias(gramatica_selecionada)
    else:
        print("Gramatica não encontrada.")

def fatora():
    nome = str(input("Nome: "))
    for g in gramaticas_livres:
        if g["nome"] == nome:
            gramatica_selecionada = g
            break
    if gramatica_selecionada != None:
        chama_r_vazias(gramatica_selecionada)
        n_prods = []
        for p in gramatica_selecionada["prods"]:
            aux = []
            for i, d in groupby(p['dir'], key=itemgetter(0)):
                aux2 = [i]
                for l in d:
                    aux2.append(l[1:])
                aux.append(aux2)
            for a in aux:
                aux3 = []
                for x in p['dir']:
                    if x[0] == a[0]:
                       if len(a) > 2:
                            aux3.append(x)
                for a3 in aux3:
                    p['dir'].remove(a3)
                if len(aux3) > 0:
                    achou = False
                    novo_simb = ''
                    while not achou:
                        novo_simb = str(random.choice(string.ascii_uppercase))
                        if novo_simb not in gramatica_selecionada["naoterm"]:
                            achou = True
                            gramatica_selecionada["naoterm"].append(novo_simb)
                            novo_dir = []
                            for a3 in aux3:
                                if a3[1:] == '':
                                    novo_dir.append('ε')
                                else:
                                    novo_dir.append(a3[1:])
                            n_prods.append({'esq': novo_simb, 'dir': novo_dir, 'fertil': None, 'visitada': False})
                            p['dir'].append(''.join([a[0], novo_simb]))
        for pr in n_prods:
            gramatica_selecionada["prods"].append(pr)
    else:
        print("Gramatica não encontrada.")

def elimina_recursao():
    nome = str(input("Nome: "))
    for g in gramaticas_livres:
        if g["nome"] == nome:
            gramatica_selecionada = g
            break
    if gramatica_selecionada != None:
        for p in gramatica_selecionada["prods"]:
            for d in p["dir"]:
                if d[0] == p['esq']:
                    aux = d
                    p["dir"].remove(d)
                    aux = aux[1:]
                    achou = False
                    novo_simb = ''
                    while not achou:
                        novo_simb = str(random.choice(string.ascii_uppercase))
                        if novo_simb not in gramatica_selecionada["naoterm"]:
                            achou = True
                            gramatica_selecionada["naoterm"].append(novo_simb)
                            gramatica_selecionada["prods"].append({'esq': novo_simb, 'dir': [''.join([aux, novo_simb]), 'ε'], 'fertil': True, 'visitada': False})
                    nova_dir = []
                    for d1 in p["dir"]:
                        if d1 != 'ε':
                            nova_dir.append(''.join([d1, novo_simb]))
                        else:
                            nova_dir.append(novo_simb)
                    p['dir'] = nova_dir
    else:
        print("Gramatica não encontrada.")

if __name__ == '__main__':
    menu()