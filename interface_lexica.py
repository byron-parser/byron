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

# Form implementation generated from reading ui file 'interface_lexica.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(520, 476)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.listaTokens = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.listaTokens.setEnabled(False)
        self.listaTokens.setObjectName("listaTokens")
        self.gridLayout.addWidget(self.listaTokens, 9, 0, 1, 1)
        self.botaoReconhece = QtWidgets.QPushButton(self.centralwidget)
        self.botaoReconhece.setObjectName("botaoReconhece")
        self.gridLayout.addWidget(self.botaoReconhece, 7, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 8, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1, QtCore.Qt.AlignLeft|QtCore.Qt.AlignBottom)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 1, 1, 1)
        self.infoReconhecimento = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.infoReconhecimento.setEnabled(False)
        self.infoReconhecimento.setObjectName("infoReconhecimento")
        self.gridLayout.addWidget(self.infoReconhecimento, 9, 1, 1, 1)
        self.textoReconhecimento = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.textoReconhecimento.setObjectName("textoReconhecimento")
        self.gridLayout.addWidget(self.textoReconhecimento, 5, 1, 1, 1)
        self.botaoTokenLista = QtWidgets.QPushButton(self.centralwidget)
        self.botaoTokenLista.setObjectName("botaoTokenLista")
        self.gridLayout.addWidget(self.botaoTokenLista, 7, 0, 1, 1)
        self.botaoSLR = QtWidgets.QPushButton(self.centralwidget)
        self.botaoSLR.setEnabled(False)
        self.botaoSLR.setObjectName("botaoSLR")
        self.gridLayout.addWidget(self.botaoSLR, 10, 0, 1, 1)
        self.botaoTabular = QtWidgets.QPushButton(self.centralwidget)
        self.botaoTabular.setEnabled(False)
        self.botaoTabular.setObjectName("botaoTabular")
        self.gridLayout.addWidget(self.botaoTabular, 10, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 8, 0, 1, 1)
        self.textoTokens = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.textoTokens.setEnabled(True)
        self.textoTokens.setObjectName("textoTokens")
        self.gridLayout.addWidget(self.textoTokens, 5, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.sintaxeButton = QtWidgets.QPushButton(self.centralwidget)
        self.sintaxeButton.setObjectName("sintaxeButton")
        self.gridLayout_2.addWidget(self.sintaxeButton, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.botaoReconhece.setText(_translate("MainWindow", "Reconhece sentença"))
        self.label_4.setText(_translate("MainWindow", "Saída do reconhecimento"))
        self.label.setText(_translate("MainWindow", "Tokens"))
        self.label_2.setText(_translate("MainWindow", "Texto para reconhecimento"))
        self.botaoTokenLista.setText(_translate("MainWindow", "Cria lista de tokens"))
        self.botaoSLR.setText(_translate("MainWindow", "Análise sintática SLR"))
        self.botaoTabular.setText(_translate("MainWindow", "Análise sintática preditiva tabular"))
        self.label_3.setText(_translate("MainWindow", "Lista de tokens criados"))
        self.sintaxeButton.setText(_translate("MainWindow", "Sintaxe dos tokens"))

