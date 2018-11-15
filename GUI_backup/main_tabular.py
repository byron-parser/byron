#!/usr/bin/python3
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView

import analise_tabular_gui as gui
import analise_sintatica_tabular as analise_sintatica

class MainWindow(QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.prontoButton.clicked.connect(self.input)
        self.testaButton.clicked.connect(self.testa)
        self.gramaticaText.setFocus()

    def testa(self):
        txt = self.sentencaLine.text()
        res = analise_sintatica.testa_sentenca(txt)
        self.resTeste.setText(str(res))

    def input(self):
        txt = self.gramaticaText.toPlainText()
        analise_sintatica.ler_input(txt)
        
        for nt in analise_sintatica.nts:
            analise_sintatica.first(nt)
        
        for k, v in analise_sintatica.firsts.items():
            v = "".join([f"{analise_sintatica.char_to_str(x)}, " for x in v])
            self.listFirst.addItem(analise_sintatica.char_to_str(k) + ": " + str(v)[:-2])
        
        for nt in analise_sintatica.nts:
            analise_sintatica.follows[nt] = []

        for nt in analise_sintatica.nts:
            analise_sintatica.atual = nt
            analise_sintatica.follow(nt)

        for k, v in analise_sintatica.follows.items():
            v_str = "".join([f"{x}, " for x in v if x == "$"])
            v_str += "".join([f"{analise_sintatica.char_to_str(x)}, " for x in v if x != "$"])
            self.listFollow.addItem(analise_sintatica.char_to_str(k) + ": " + str(v_str)[:-2])

        #analise_sintatica.aumenta_gramatica()
        #analise_sintatica.percorre_estados(analise_sintatica.estados)
        analise_sintatica.cria_tabela()

        #for v in analise_sintatica.gotos:
        #    self.listGotos.addItem(v)

        self.tableAcao.setRowCount(len(analise_sintatica.cnt_term))
        self.tableAcao.setColumnCount(len(analise_sintatica.nts))

        labels_acao = []
        for x in analise_sintatica.cnt_term:
            if x != "$":
                labels_acao.append(analise_sintatica.char_to_str(x))
            else:
                labels_acao.append(x)

        labels_nt = []
        for x in analise_sintatica.nts:
            labels_nt.append(analise_sintatica.char_to_str(x))

        self.tableAcao.setVerticalHeaderLabels(labels_nt)
        self.tableAcao.setHorizontalHeaderLabels(labels_acao)

        for i in range(0, len(analise_sintatica.tabela)):
            linha = list(analise_sintatica.tabela.items())[i]
            print(analise_sintatica.mapa_str_char[list(linha[1].items())[0][0]])
            print(f"{labels_nt.index(analise_sintatica.char_to_str(linha[0]))} {linha}")
            for j in range(0, len(analise_sintatica.cnt_term)):
                if self.tableAcao.horizontalHeaderItem(j) != None:
                    hd = self.tableAcao.horizontalHeaderItem(j).text()
                    if hd in linha[1]:
                        lc = linha[1][hd]
                    else:
                        lc = None
                    if lc:
                        self.tableAcao.setItem(i, j, QTableWidgetItem(str(lc)))
                    else:
                        self.tableAcao.setItem(i, j, QTableWidgetItem(""))
            hd = None
            self.tableAcao.resizeColumnsToContents()

        '''
        for i in range(0, len(analise_sintatica.tabela)):
            linha = analise_sintatica.tabela[i]
            for j in range(0, len(analise_sintatica.cnt_term)):
                hd = self.tableAcao.horizontalHeaderItem(j).text()
                if hd in linha:
                    lc = linha[hd]
                else:
                    lc = None
                if lc:
                    self.tableAcao.setItem(i, j, QTableWidgetItem(str(lc)))
                else:
                    self.tableAcao.setItem(i, j, QTableWidgetItem(""))
            hd = None
        self.tableAcao.resizeColumnsToContents()
        '''
        self.testaButton.setEnabled(True)

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
