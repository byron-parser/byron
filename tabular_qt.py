#!/usr/bin/env python3
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

import sys
from pathlib import Path
import ast
from importlib import reload

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QHeaderView, QFileDialog, QErrorMessage
from PyQt5.QtGui import QTextCursor, QIcon

import interface_tabular
import analise_tabular
import gerador_modulo

class MainWindow(QMainWindow, interface_tabular.Ui_MainWindow):
    def __init__(self, tokens):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Byron - Análise Sintática Preditiva Tabular")
        self.setWindowIcon(QIcon("byron.ico"))
        self.prontoButton.clicked.connect(self.input)
        self.testaButton.clicked.connect(self.testa)
        self.geraButton_2.clicked.connect(self.gera_codigo)
        self.geraButton_2.setEnabled(False)
        self.salvaButton_2.clicked.connect(self.salva)
        self.salvaButton_2.setEnabled(False)
        self.carregaButton_2.clicked.connect(self.carrega)
        self.sintaxeButton.clicked.connect(self.mostra_sintaxe)
        self.gramaticaText.setFocus()
        self.mensagem_erro = QErrorMessage()
        self.tokens = tokens
        analise_tabular.tokens = {(k,v) for k,v in self.tokens}
        print(f"Interface: {self.tokens}")
        print(f"Algoritmo: {analise_tabular.tokens}")

    def mostra_sintaxe(self):
        msg = QMessageBox()
        msg.information(self, "Sintaxe", '''Para utilizar a interface de análise sintática, é necessário fornecer uma gramática ao programa, sendo esta neste formato:
naoterminal -> outro TERMINAL | EXEMPLO
outro -> SIMBOLO
sendo cada linha regras de produção. No lado esquerdo da seta, deve-se conter um símbolo não-terminal, e do lado direito, pode haver combinação de não-terminais e terminais.
Um espaço separa símbolos e uma barra (“|”) separa produções diferentes. Por exemplo, “naoterminal -> outro TERMINAL” e “naoterminal -> EXEMPLO” são produções distintas.
Se um símbolo se encontra na tabela de tokens, será tratado como um terminal. Caso contrário será um não-terminal.
As letras maíusculas E e Z são reservadas, a letra E representa uma sentença vazia.''')

    def gera_codigo(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)
        caminho = dlg.getExistingDirectory(self, "Gerar código em", str(Path().resolve()), QFileDialog.ShowDirsOnly)
        print(f"gera_codigo: {caminho}")
        if caminho != "" and caminho != None:
            gerador_modulo.gera_modulo_tabular(self.tokens, self.gramaticaText.toPlainText(), caminho)

    def salva(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        arquivo = dlg.getSaveFileName(self, "Salvar em", str(Path().resolve()))
        print(f"salva: {arquivo}")
        if arquivo[0] != "" and arquivo[0] != None:
            gerador_modulo.salva_dados(self.tokens, self.gramaticaText.toPlainText(), arquivo[0])

    def carrega(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.ExistingFile)
        arquivo = dlg.getOpenFileName(self, "Abrir", str(Path().resolve()))
        print(f"carrega: {arquivo}")
        if arquivo[0] != "" and arquivo[0] != None:
            with open(arquivo[0], "r") as arq:
                linhas = arq.readlines()
                tk = ast.literal_eval(linhas[0][9:-1])
                analise_tabular.tokens = tk
                self.tokens = tk
                self.gramaticaText.setText("")
                for linha in linhas[1][13:-3].split("\\n"):
                    self.gramaticaText.append(linha)

    def testa(self):
        try:
            txt = self.sentencaLine.text()
            txt = analise_tabular.reconhece_tokens(txt)
            res = analise_tabular.testa_sentenca(txt)
            self.resTeste.setText(str(res))
            self.resTeste.moveCursor(QTextCursor.End)
        except:
            self.mensagem_erro.showMessage("Erro ao reconhecer sentença.")

    def limpa(self):
        reload(analise_tabular)
        analise_tabular.tokens = {(k,v) for k,v in self.tokens}
        self.listFirst.clear()
        self.listFollow.clear()
        self.tableAcao.clear()
        self.tableAcao.setRowCount(0)
        self.tableAcao.setColumnCount(0)
        self.sentencaLine.clear()
        self.resTeste.clear()

    def input(self):
        self.limpa()
        try:
            txt = self.gramaticaText.toPlainText()
            analise_tabular.ler_input(txt)
            
            for nt in analise_tabular.nts:
                analise_tabular.first(nt)
            
            for k, v in analise_tabular.firsts.items():
                v = "".join([f"{analise_tabular.char_to_str(x)}, " if x != "E" else "ε, " for x in v])
                self.listFirst.addItem(analise_tabular.char_to_str(k) + ": " + str(v)[:-2])
            
            for nt in analise_tabular.nts:
                analise_tabular.follows[nt] = []

            for nt in analise_tabular.nts:
                analise_tabular.atual = nt
                analise_tabular.follow(nt)

            for k, v in analise_tabular.follows.items():
                v_str = "".join([f"{x}, " for x in v if x == "$"])
                v_str += "".join([f"{analise_tabular.char_to_str(x)}, " for x in v if x != "$"])
                self.listFollow.addItem(analise_tabular.char_to_str(k) + ": " + str(v_str)[:-2])

            #analise_tabular.aumenta_gramatica()
            #analise_tabular.percorre_estados(analise_tabular.estados)
            analise_tabular.cria_tabela()

            #for v in analise_tabular.gotos:
            #    self.listGotos.addItem(v)

            self.tableAcao.setRowCount(len(analise_tabular.nts))
            self.tableAcao.setColumnCount(len(analise_tabular.cnt_term))

            labels_acao = []
            for x in analise_tabular.cnt_term:
                if x != "$":
                    labels_acao.append(analise_tabular.char_to_str(x))
                else:
                    labels_acao.append(x)

            labels_nt = []
            for x in analise_tabular.nts:
                labels_nt.append(analise_tabular.char_to_str(x))

            self.tableAcao.setVerticalHeaderLabels(labels_nt)
            self.tableAcao.setHorizontalHeaderLabels(labels_acao)

            for i in range(0, len(analise_tabular.tabela)):
                linha = list(analise_tabular.tabela.items())[i]
                #print(analise_tabular.mapa_str_char[list(linha[1].items())[0][0]])
                #print(f"{labels_nt.index(analise_tabular.char_to_str(linha[0]))} {linha}")
                #print(analise_tabular.nts)
                for j in range(0, len(analise_tabular.cnt_term)):
                    if self.tableAcao.horizontalHeaderItem(j) != None:
                        hd = self.tableAcao.horizontalHeaderItem(j).text()
                        if analise_tabular.str_to_char(hd) in linha[1]:
                            lc = linha[1][analise_tabular.str_to_char(hd)]
                            lc_print = f"{analise_tabular.char_to_str(lc[0])} -> "
                            for l in lc[1]:
                                if l != "E":
                                    lc_print += f"{analise_tabular.char_to_str(l)} "
                                else:
                                    lc_print += "ε "
                            lc = lc_print[:-1]
                        elif hd == "$" and hd in linha[1]:
                            lc = linha[1]["$"]
                            lc_print = f"{analise_tabular.char_to_str(lc[0])} -> "
                            for l in lc[1]:
                                if l != "E":
                                    lc_print += f"{analise_tabular.char_to_str(l)} "
                                else:
                                    lc_print += "ε "
                            lc = lc_print[:-1]
                        else:
                            lc = None
                        if lc:
                            self.tableAcao.setItem(i, j, QTableWidgetItem(str(lc)))
                        else:
                            self.tableAcao.setItem(i, j, QTableWidgetItem(""))
                hd = None
                self.tableAcao.resizeColumnsToContents()

            self.testaButton.setEnabled(True)
            self.geraButton_2.setEnabled(True)
            self.salvaButton_2.setEnabled(True)
        except:
            self.mensagem_erro.showMessage("Erro ao receber gramática.")
            self.limpa()

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow([("for", "FOR"), ("int", "INT"), ("while", "WHILE"), ("float", "FLOAT"), ("string", "STRING")])
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
