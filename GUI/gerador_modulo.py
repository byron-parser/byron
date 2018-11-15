import pathlib
import shutil

def gera_modulo(tokens, gramatica):
    caminho = "teste"

    p = pathlib.Path(caminho).mkdir(exist_ok=True, parents=True) 
    shutil.copy("template_analise_sintatica.py", caminho)

    f = open(f"{caminho}/__init__.py", "w+")
    f.close()

    with open(f"{caminho}/modulo.py", "w+") as modulo:
        modulo.write(f"import template_analise_sintatica\n" + 
                    f"template_analise_sintatica.tokens = {tokens}\n" +
                    f"template_analise_sintatica.gramatica = {gramatica}\n")