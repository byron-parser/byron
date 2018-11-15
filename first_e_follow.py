#!/usr/bin/python3
import itertools
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
    def __init__(self, simbolo, gramatica):
        self.gramatica = gramatica
        self.simbolo = simbolo
        self.producoes = []
        self._first = []
        self._follow = []
        self.first_status = False
        self.follow_status = False

    def tem_epsilon(self):
        for p in self.producoes:
            for d in p.direita:
                if EPSILON in d:
                    return True
            return False

    def adiciona_producao(self, *p):
        for sp in p:
            self.producoes.append(sp)
            
    def first(self, d=0):
        self.first_status = True
        
        for pr_atual in self.producoes:
            for p in pr_atual.direita:
                if p[d] in self.gramatica.terminais:
                    self._first.append(p[d])
                elif p[d] == EPSILON:
                    self._first.append(EPSILON)
                    
                for nt in self.gramatica.nao_terminais:
                    for pr in nt.producoes:
                        if nt.simbolo == p[d]:
                            nt.first(d)
                            self._first = list(set(self._first + nt._first))
                            if nt.tem_epsilon() and d < len(p):
                                pass
                                #self.first(d+1)
                    

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
gr.adiciona_terminal("a", "i", "t", "b", "e")
gr.adiciona_nao_terminal(NaoTerminal("S", gr), NaoTerminal("X", gr), NaoTerminal("E", gr))
'''for nt in gr.nao_terminais:
    nt.adiciona_producao(Producao(nt.simbolo, ["T", "E'"]), Producao("E'", ["v", "T", "E'"], ["ε"]), Producao("T", ["F", "T'"]), Producao("T'", ["&", "F", "T'"], ["ε"]), Producao("F", ["¬", "F"], ["id"]))
  '''  
gr.nao_terminais[0].adiciona_producao(Producao(gr.nao_terminais[0].simbolo, ["i", "E", "t", "S", "X"], ["a"]))
gr.nao_terminais[1].adiciona_producao(Producao(gr.nao_terminais[1].simbolo, ["e", "S"], ["ε"]))
gr.nao_terminais[2].adiciona_producao(Producao(gr.nao_terminais[2].simbolo, ["b"]))

gr.producao_inicial = "S"

for nt in gr.nao_terminais:
    if not nt.first_status:
        nt.first()

for nt in gr.nao_terminais:
    for prods in nt.producoes:
        print(prods)
  
print("-------------------")

for nt in gr.nao_terminais:
    print(nt._first)
