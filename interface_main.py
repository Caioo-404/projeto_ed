import tkinter as tk
from tkinter import filedialog
import os
from compactar_arquivos import *

def escolherArquivo():
    filepath = filedialog.askopenfilename()

    if filepath:
        #O nome do arquivo e a extensão
        nome_arquivo, extensao = os.path.splitext(os.path.basename(filepath))

        if extensao != ".bin":
            novo_nome = f"{nome_arquivo}_Binário"
        else:
            novo_nome = f"{nome_arquivo}_Descompactado"

        entrarNome.delete(0, tk.END)
        entrarNome.insert(0, novo_nome)

    entrarArquivo.delete(0, tk.END)
    entrarArquivo.insert(0, filepath)


def compactarIG():
    enderecoFile = entrarArquivo.get()
    newName = entrarNome.get()

    if not enderecoFile or not newName:
        status.config(text="Por favor, escolha um arquivo e digite um novo nome.")
        return

    with open(enderecoFile, 'rb') as file:
        bits = bitarray()
        bits.fromfile(file)
        bits = bits.to01()

        data = list()
        tam = 0
        for i in range(0, len(bits), 8):
            tam += 8
            data.append(bits[i:tam])

    dataCompactada, arvoreHuffman, dictDeHuffman = compactar(data)

    arquivoBin(arvoreHuffman, dataCompactada, newName)

    status.config(text=f"Arquivo compactado e salvo como: {newName}.bin")


def descompactarIG():
    enderecoFile = entrarArquivo.get()
    newName = entrarNome.get()

    if not enderecoFile or not newName:
        status.config(text="Por favor, escolha um arquivo e digite um novo nome.")
        return
    
    textoDescompactado = rollback(enderecoFile)

    with open(newName, "wb+") as file:
        file.write(textoDescompactado.tobytes())

    status.config(text=f"Arquivo descompactado e salvo como: {newName}")


#Interface 
janela = tk.Tk()
janela.title("Compactador e Descompactador Huffman")
janela.geometry("640x150")

#Criando locais de entrada
texto = tk.Label(janela, text="Escolha o arquivo para compactar/descompactar:", bg="#296073", fg="white")
entrarArquivo = tk.Entry(janela, width=35)
botao = tk.Button(janela, text="Escolher Arquivo", command=escolherArquivo)

texto1 = tk.Label(janela, text="Digite um novo nome pro arquivo:", bg="#296073", fg="white")
entrarNome = tk.Entry(janela, width=35)

botaoCompactar = tk.Button(janela, text="Compactar e Salvar", command=compactarIG)
botaoDescompactar = tk.Button(janela, text="Descompactar e Salvar", command=descompactarIG)

status = tk.Label(janela, text="", bg="#296073", fg="white")


#Locais/bonitin
janela.configure(bg="#296073")
texto.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
entrarArquivo.grid(row=0, column=1, padx=10, pady=5)
botao.grid(row=0, column=2, padx=10, pady=5)

texto1.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
entrarNome.grid(row=1, column=1, padx=10, pady=5)

botaoCompactar.grid(row=2, column=0, pady=10)
botaoDescompactar.grid(row=2, column=1, pady=10)

status.grid(row=3, column=0, columnspan=2)


janela.mainloop()