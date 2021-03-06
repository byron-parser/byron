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

# Form implementation generated from reading ui file 'interface_slr.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(749, 591)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_5.addWidget(self.label_6)
        self.sentencaLine = QtWidgets.QLineEdit(self.centralwidget)
        self.sentencaLine.setObjectName("sentencaLine")
        self.verticalLayout_5.addWidget(self.sentencaLine)
        self.testaButton = QtWidgets.QPushButton(self.centralwidget)
        self.testaButton.setEnabled(False)
        self.testaButton.setObjectName("testaButton")
        self.verticalLayout_5.addWidget(self.testaButton)
        self.resTeste = QtWidgets.QTextEdit(self.centralwidget)
        self.resTeste.setEnabled(True)
        self.resTeste.setObjectName("resTeste")
        self.verticalLayout_5.addWidget(self.resTeste)
        self.gridLayout.addLayout(self.verticalLayout_5, 0, 2, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.listGotos = QtWidgets.QListWidget(self.centralwidget)
        self.listGotos.setObjectName("listGotos")
        self.verticalLayout_3.addWidget(self.listGotos)
        self.gridLayout.addLayout(self.verticalLayout_3, 1, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.listFirst = QtWidgets.QListWidget(self.centralwidget)
        self.listFirst.setObjectName("listFirst")
        self.verticalLayout_2.addWidget(self.listFirst)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.listFollow = QtWidgets.QListWidget(self.centralwidget)
        self.listFollow.setObjectName("listFollow")
        self.verticalLayout_2.addWidget(self.listFollow)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 1, 1, 1)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_6.addWidget(self.label_7)
        self.tableDesvio = QtWidgets.QTableWidget(self.centralwidget)
        self.tableDesvio.setObjectName("tableDesvio")
        self.tableDesvio.setColumnCount(0)
        self.tableDesvio.setRowCount(0)
        self.verticalLayout_6.addWidget(self.tableDesvio)
        self.gridLayout.addLayout(self.verticalLayout_6, 1, 2, 1, 1)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_4.addWidget(self.label_5)
        self.tableAcao = QtWidgets.QTableWidget(self.centralwidget)
        self.tableAcao.setObjectName("tableAcao")
        self.tableAcao.setColumnCount(0)
        self.tableAcao.setRowCount(0)
        self.verticalLayout_4.addWidget(self.tableAcao)
        self.gridLayout.addLayout(self.verticalLayout_4, 1, 1, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.sintaxeButton = QtWidgets.QPushButton(self.centralwidget)
        self.sintaxeButton.setObjectName("sintaxeButton")
        self.verticalLayout.addWidget(self.sintaxeButton)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.gramaticaText = QtWidgets.QTextEdit(self.centralwidget)
        self.gramaticaText.setAcceptRichText(False)
        self.gramaticaText.setObjectName("gramaticaText")
        self.verticalLayout.addWidget(self.gramaticaText)
        self.prontoButton = QtWidgets.QPushButton(self.centralwidget)
        self.prontoButton.setObjectName("prontoButton")
        self.verticalLayout.addWidget(self.prontoButton)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.salvaButton = QtWidgets.QPushButton(self.centralwidget)
        self.salvaButton.setObjectName("salvaButton")
        self.horizontalLayout.addWidget(self.salvaButton)
        self.carregaButton = QtWidgets.QPushButton(self.centralwidget)
        self.carregaButton.setObjectName("carregaButton")
        self.horizontalLayout.addWidget(self.carregaButton)
        self.geraButton = QtWidgets.QPushButton(self.centralwidget)
        self.geraButton.setObjectName("geraButton")
        self.horizontalLayout.addWidget(self.geraButton)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_6.setText(_translate("MainWindow", "Testa senten??a:"))
        self.testaButton.setText(_translate("MainWindow", "Testa"))
        self.label_4.setText(_translate("MainWindow", "Gotos:"))
        self.label_2.setText(_translate("MainWindow", "First:"))
        self.label_3.setText(_translate("MainWindow", "Follow:"))
        self.label_7.setText(_translate("MainWindow", "Tabela desvio:"))
        self.label_5.setText(_translate("MainWindow", "Tabela a????o:"))
        self.sintaxeButton.setText(_translate("MainWindow", "Sintaxe da gram??tica"))
        self.label.setText(_translate("MainWindow", "Gram??tica:"))
        self.prontoButton.setText(_translate("MainWindow", "Pronto"))
        self.salvaButton.setText(_translate("MainWindow", "Salva dados"))
        self.carregaButton.setText(_translate("MainWindow", "Carrega dados"))
        self.geraButton.setText(_translate("MainWindow", "Gera m??dulo Python"))

