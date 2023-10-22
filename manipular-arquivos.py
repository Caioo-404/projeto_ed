'''
-----Códigos para arquivos:
"r" -> Usar para ler
"w" -> Usar para escrever
"r+" -> Ler e Escrever
"a" -> acrescentar algo (não apaga tudo como o "W")
"x" -> cria
*Modo texto ("t")
*Modo binário ("b")
Ex: "wb" representa escrever em modo binário.


-----Arquivo:
open("nome_arquivo", "tipo do que for fazer")
arq.close() -> Fecha o arquivo
arq.write("texto") -> escrever
arq.readlines() -> retorna uma lista com o texto
arq.read() -> normal


-----Estrutura Arquivos(Fecha auto)
with open('nome_do_arquivo.txt', "w") as arquivo:
    ...código...

    
-----Excluir arquivo:
import os
os.remove("sample_file.txt")
'''
