# Byron - ferramenta de apoio ao desenvolvimento de compiladores

![Ícone da ferramenta Byron](https://raw.githubusercontent.com/ghuwe/byron/master/byron.ico)

## Sobre Byron

Byron é uma ferramenta multiplataforma de apoio ao desenvolvimento de compiladores desenvolvida em Python 3, com intuito de uso em sala de aula, e apresenta as seguintes funcionalidades:

* Análise léxica (utilizando expressões regulares)
* Análise sintática preditiva tabular
* Análise sintática SLR
* Salvar e carregar informações (tokens e gramáticas)
* Geração de módulos Python

## Captura de telas

* Análise léxica
![Análise léxica](https://i.imgur.com/rYXcNwZ.jpg)

* Análise sintática preditiva tabular
![Análise sintática preditiva tabular](https://i.imgur.com/wNXHevh.jpg)

* Análise sintática SLR
![Análise sintática SLR](https://i.imgur.com/YvRGSzQ.jpg)

## Instruções de execução

Para rodar a ferramenta em um ambiente Unix ou Unix-like, deve-se rodar ./byron.py.
A ferramenta depende de Python 3.6 ou mais recente, e o módulo PyQt5.
Para instalar PyQt5, rode o comando `pip3 install pyqt5 --user`.

Em um sistema Windows, pode-se utilizar o executável encontrado na página de release.

## Uso da ferramenta

Para informações do uso do Byron, leia o arquivo manual_byron.doc.

## Licença

A ferramenta Byron utiliza a licença GPL 3.
