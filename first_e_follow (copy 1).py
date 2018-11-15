#!/usr/bin/python3
EPSILON = "ε"

class Producao:
    def __init__(self, e, *d):
        self.esquerda = e
        self.direita = []
        for sd in d:
            self.direita.append(sd)
    
    def __str__(self):
        return self.esquerda + " -> " + " | ".join(["".join(d) for d in self.direita])

class NaoTerminal:
    def __init__(self, simbolo):
        self.simbolo = simbolo
        self.producoes = []
        self._first = []
        self._follow = []

    def adiciona_producao(self, *p):
        for sp in p:
            self.producoes.append(sp)

class Gramatica:
    def __init__(self):
        self.terminais = []
        self.nao_terminais = []
        self.producao_inicial = None

    def adiciona_terminal(self, *t):
        for st in t:
            self.terminais.append(st)
        
    def adiciona_nao_terminal(self, *n):
        for sn in n:
            self.nao_terminais.append(sn)

                

gr = Gramatica()
gr.adiciona_terminal("v", "id", "¬", "&")
gr.adiciona_nao_terminal(NaoTerminal("E"), NaoTerminal("E'"), NaoTerminal("T"), NaoTerminal("T'"), NaoTerminal("F"))
'''for nt in gr.nao_terminais:
    nt.adiciona_producao(Producao(nt.simbolo, ["T", "E'"]), Producao("E'", ["v", "T", "E'"], ["ε"]), Producao("T", ["F", "T'"]), Producao("T'", ["&", "F", "T'"], ["ε"]), Producao("F", ["¬", "F"], ["id"]))
  '''  
gr.nao_terminais[0].adiciona_producao(Producao(gr.nao_terminais[0].simbolo, ["T", "E"]))
gr.nao_terminais[1].adiciona_producao(Producao(gr.nao_terminais[1].simbolo, ["v", "T", "E"], ["ε"]))
gr.nao_terminais[2].adiciona_producao(Producao(gr.nao_terminais[2].simbolo, ["F", "T"]))
gr.nao_terminais[3].adiciona_producao(Producao(gr.nao_terminais[3].simbolo, ["&", "F", "T"], ["ε"]))
gr.nao_terminais[4].adiciona_producao(Producao(gr.nao_terminais[4].simbolo, ["¬", "F"], ["id"]))

gr.producao_inicial = "E"
#gr.first("E")

for nt in gr.nao_terminais:
    for prods in nt.producoes:
        print(prods)
    
print("-------------------")

#print(gr._first)
