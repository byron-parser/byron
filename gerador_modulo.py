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

import pathlib
import shutil

def gera_modulo_slr(tokens, gramatica, diretorio):
        caminho = f"{diretorio}/modulo_slr"

        p = pathlib.Path(caminho).mkdir(exist_ok=True, parents=True) 
        shutil.copy("template_slr.py", caminho)

        f = open(f"{caminho}/__init__.py", "w+")
        f.close()

        gramatica_preparada = [f"{g}\\n" for g in gramatica.splitlines()]

        with open(f"{caminho}/slr.py", "w+") as modulo:
                modulo.write(f"from . import template_slr as t\n" + 
                                f"t.tokens = {tokens}\n" +
                                f"t.ler_input('{''.join(gramatica_preparada)}')\n" +
                                f"t.prepara_dados()\n" +
                                f"def reconhece_sentenca(sentenca):\n" +
                                f"\tsentenca_chars = t.reconhece_tokens(sentenca)\n" +
                                f"\treturn t.testa_sentenca(sentenca_chars)")

def gera_modulo_tabular(tokens, gramatica, diretorio):
        caminho = f"{diretorio}/modulo_tabular"

        p = pathlib.Path(caminho).mkdir(exist_ok=True, parents=True) 
        shutil.copy("template_tabular.py", caminho)

        f = open(f"{caminho}/__init__.py", "w+")
        f.close()

        gramatica_preparada = [f"{g}\\n" for g in gramatica.splitlines()]

        with open(f"{caminho}/tabular.py", "w+") as modulo:
                modulo.write(f"from . import template_tabular as t\n" + 
                                f"t.tokens = {tokens}\n" +
                                f"t.ler_input('{''.join(gramatica_preparada)}')\n" +
                                f"t.prepara_dados()\n" +
                                f"def reconhece_sentenca(sentenca):\n" +
                                f"\tsentenca_chars = t.reconhece_tokens(sentenca)\n" +
                                f"\treturn t.testa_sentenca(sentenca_chars)")

def salva_dados(tokens, gramatica, caminho):
        gramatica_preparada = [f"{g}\\n" for g in gramatica.splitlines()]

        with open(caminho, "w+") as modulo:
                modulo.write(f"tokens = {tokens}\n" +
                            f"gramatica = '{''.join(gramatica_preparada)}'")