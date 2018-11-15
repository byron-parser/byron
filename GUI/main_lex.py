#!/usr/bin/python3
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView

import gui_lex
import analise_lexica
import main_slr

class MainWindow(QMainWindow, gui_lex.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.botaoTokenLista.clicked.connect(self.criaLista)
        self.botaoReconhece.clicked.connect(self.reconhece)
        self.botaoSLR.clicked.connect(self.abre_slr)
        self.textoTokens.setFocus()
        self.botaoReconhece.setDisabled(True)
        self.res = ""
        self.slr = None

    def abre_slr(self):
        self.slr = main_slr.SLRWindow(analise_lexica.tokens)
        self.slr.show()

    def criaLista(self):
        txt = self.textoTokens.toPlainText()
        self.res = str(analise_lexica.ler_input(txt))
        self.listaTokens.document().setPlainText(self.res)
        self.botaoReconhece.setDisabled(False)
        self.botaoSLR.setDisabled(False)
        self.botaoTabular.setDisabled(False)

    def reconhece(self):
        txt = self.textoReconhecimento.toPlainText()
        res = analise_lexica.reconhece(txt)
        self.infoReconhecimento.document().setPlainText(str(res))

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()