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

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QErrorMessage, QMessageBox

import interface_lexica
import analise_lexica
import tabular_qt
import slr_qt

class MainWindow(QMainWindow, interface_lexica.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Byron - Análise Léxica")
        self.botaoTokenLista.clicked.connect(self.criaLista)
        self.botaoReconhece.clicked.connect(self.reconhece)
        self.botaoSLR.clicked.connect(self.abre_slr)
        self.botaoTabular.clicked.connect(self.abre_tabular)
        self.sintaxeButton.clicked.connect(self.mostra_sintaxe)
        self.textoTokens.setFocus()
        self.botaoReconhece.setDisabled(True)
        self.mensagem_erro = QErrorMessage()
        self.res = ""
        self.slr = None
        self.tabular = None

    def mostra_sintaxe(self):
        msg = QMessageBox()
        msg.information(self, "Sintaxe", "Em cada linha, deve-se inserir uma expressão regular e um símbolo que a represente, separados por dois pontos (:)")

    def abre_slr(self):
        self.slr = slr_qt.SLRWindow(analise_lexica.tokens)
        self.slr.show()

    def abre_tabular(self):
        self.tabular = tabular_qt.MainWindow(analise_lexica.tokens)
        self.tabular.show()

    def criaLista(self):
        try:
            txt = self.textoTokens.toPlainText()
            self.res = str(analise_lexica.ler_input(txt))
            self.listaTokens.document().setPlainText(self.res)
            self.botaoReconhece.setDisabled(False)
            self.botaoSLR.setDisabled(False)
            self.botaoTabular.setDisabled(False)
        except:
            self.mensagem_erro.showMessage("Erro ao criar tabela de tokens.")

    def reconhece(self):
        try:
            txt = self.textoReconhecimento.toPlainText()
            res = analise_lexica.reconhece(txt)
            self.infoReconhecimento.document().setPlainText(str(res))
        except:
            self.mensagem_erro.showMessage("Erro ao reconhecer sentença.")

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()