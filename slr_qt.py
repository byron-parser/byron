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

import interface_slr
import analise_slr
import gerador_modulo

class SLRWindow(QMainWindow, interface_slr.Ui_MainWindow):
    def __init__(self, tokens):
        super(SLRWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Byron - Análise Sintática SLR")
        self.setWindowIcon(QIcon("byron.ico"))
        self.prontoButton.clicked.connect(self.input)
        self.testaButton.clicked.connect(self.testa)
        self.geraButton.clicked.connect(self.gera_codigo)
        self.geraButton.setEnabled(False)
        self.salvaButton.clicked.connect(self.salva)
        self.salvaButton.setEnabled(False)
        self.carregaButton.clicked.connect(self.carrega)
        self.sintaxeButton.clicked.connect(self.mostra_sintaxe)
        self.gramaticaText.setFocus()
        self.mensagem_erro = QErrorMessage()
        self.tokens = tokens
        analise_slr.tokens = {(k,v) for k,v in self.tokens}
        print(f"Interface: {self.tokens}")
        print(f"Algoritmo: {analise_slr.tokens}")

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
            gerador_modulo.gera_modulo_slr(self.tokens, self.gramaticaText.toPlainText(), caminho)

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
                analise_slr.tokens = tk
                self.tokens = tk
                self.gramaticaText.setText("")
                for linha in linhas[1][13:-3].split("\\n"):
                    self.gramaticaText.append(linha)

    def testa(self):
        try:
            txt = self.sentencaLine.text()
            txt = analise_slr.reconhece_tokens(txt)
            res = analise_slr.testa_sentenca(txt)
            self.resTeste.setText(str(res))
            self.resTeste.moveCursor(QTextCursor.End)
        except:
            self.mensagem_erro.showMessage("Erro ao reconhecer sentença.")

    def limpa(self):
        reload(analise_slr)
        analise_slr.tokens = {(k,v) for k,v in self.tokens}
        self.listFirst.clear()
        self.listFollow.clear()
        self.listGotos.clear()
        self.tableAcao.clear()
        self.tableAcao.setRowCount(0)
        self.tableAcao.setColumnCount(0)
        self.tableDesvio.clear()
        self.tableDesvio.setRowCount(0)
        self.tableDesvio.setColumnCount(0)
        self.sentencaLine.clear()
        self.resTeste.clear()

    def input(self):
        self.limpa()
        try:
            txt = self.gramaticaText.toPlainText()
            analise_slr.ler_input(txt)
            
            for nt in analise_slr.nts:
                analise_slr.first(nt)
            
            for k, v in analise_slr.firsts.items():
                v = "".join([f"{analise_slr.char_to_str(x)}, " for x in v])
                self.listFirst.addItem(analise_slr.char_to_str(k) + ": " + str(v)[:-2])
            
            for nt in analise_slr.nts:
                analise_slr.follows[nt] = []

            for nt in analise_slr.nts:
                analise_slr.atual = nt
                analise_slr.follow(nt)

            for k, v in analise_slr.follows.items():
                v_str = "".join([f"{x}, " for x in v if x == "$"])
                v_str += "".join([f"{analise_slr.char_to_str(x)}, " for x in v if x != "$"])
                self.listFollow.addItem(analise_slr.char_to_str(k) + ": " + str(v_str)[:-2])

            analise_slr.aumenta_gramatica()
            analise_slr.percorre_estados(analise_slr.estados)
            analise_slr.cria_tabela()

            for v in analise_slr.gotos:
                self.listGotos.addItem(v)

            self.tableAcao.setRowCount(len(analise_slr.acao))
            self.tableAcao.setColumnCount(len(analise_slr.cnt_term))

            self.tableDesvio.setRowCount(len(analise_slr.desvio))
            self.tableDesvio.setColumnCount(len(analise_slr.nts))
            
            idxs = []
            for x in range(0, len(analise_slr.gotos), 1):
                idxs.append(str(x))
            
            self.tableAcao.setVerticalHeaderLabels(idxs)
            labels_acao = []
            for x in analise_slr.cnt_term:
                if x != "$":
                    labels_acao.append(analise_slr.char_to_str(x))
                else:
                    labels_acao.append(x)

            self.tableAcao.setHorizontalHeaderLabels(labels_acao)

            for i in range(0, len(analise_slr.acao)):
                linha = analise_slr.acao[i]
                print(linha)
                for j in range(0, len(analise_slr.cnt_term)):
                    hd = self.tableAcao.horizontalHeaderItem(j).text()
                    print(j, hd)
                    if analise_slr.str_to_char(hd) in linha:
                        lc = linha[analise_slr.str_to_char(hd)]
                    elif hd == "$" and hd in linha:
                        lc = linha["$"]
                    else:
                        lc = None
                    if lc:
                        self.tableAcao.setItem(i, j, QTableWidgetItem(str(lc)))
                    else:
                        self.tableAcao.setItem(i, j, QTableWidgetItem(""))
                hd = None
            self.tableAcao.resizeColumnsToContents()

            self.tableDesvio.setVerticalHeaderLabels(idxs)

            labels_desvio = []
            for x in analise_slr.nts:
                labels_desvio.append(analise_slr.char_to_str(x))

            self.tableDesvio.setHorizontalHeaderLabels(labels_desvio)

            for i in range(0, len(analise_slr.desvio)):
                linha = analise_slr.desvio[i]
                for j in range(0, len(analise_slr.nts)):
                    hd = self.tableDesvio.horizontalHeaderItem(j).text()
                    if analise_slr.str_to_char(hd) in linha:
                        lc = linha[analise_slr.str_to_char(hd)]
                    else:
                        lc = None
                    if lc:
                        self.tableDesvio.setItem(i, j, QTableWidgetItem(str(lc)))
                    else:
                        self.tableDesvio.setItem(i, j, QTableWidgetItem(""))
                hd = None
            self.tableDesvio.resizeColumnsToContents()
            self.testaButton.setEnabled(True)
            self.geraButton.setEnabled(True)
            self.salvaButton.setEnabled(True)
        except:
            self.mensagem_erro.showMessage("Erro ao receber gramática.")
            self.limpa()

def main():
    app = QApplication(sys.argv)
    main_window = SLRWindow([("for", "FOR"), ("int", "INT"), ("while", "WHILE"), ("float", "FLOAT"), ("string", "STRING")])
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
