import heapq
import pickle
from bitarray import bitarray
import subprocess
import sys

#Criando uma classe de nós huffman
class Node:
    #Construtor
    def __init__(self, valor, frequecia):
        self.char = valor
        self.freq = frequecia
        self.left = None
        self.right = None

    #Representação em string (ajudar na visualização)
    def __str__(self):
        return "(" + str(self.char) + "," + str(self.freq) + ")"
    
    #Comparar na class (< e ==)
    def __lt__(self, outro):
        return self.freq < outro.freq
    
    def __eq__(self, outro ):
        return self.freq == outro.freq and self.char == outro.char       


#Construir árvore huffman 
def contrucaoArvore(data):
    #Ver frequência de cada caracter e colocar em um dict:
    frequencia = dict()
    for char in data:
        if char in frequencia:
            frequencia[char] += 1
        else:
            frequencia[char] = 1

    #Criar uma lista de nó-huffman (valor e frequência)
    listaNo = [Node(char, freq) for char, freq in frequencia.items()]
    
    #Transformar a lista em um heapq (prioridade) -> pega o menor elemento
    heapq.heapify(listaNo)

    #Construir a árvore de Huffman
    while len(listaNo) > 1:
        #Remover elementos de menor frequência
        esquerda = heapq.heappop(listaNo)
        direita = heapq.heappop(listaNo)
        print(esquerda, direita)

        #Crio um nó com valor vazio e com frequência sendo a soma dos outros nós
        merge = Node(None, esquerda.freq + direita.freq)
        merge.left = esquerda
        merge.right = direita
        print(f'\nMerge dos nós {esquerda} + {direita}:', merge)
        print('---'*15)

        #Coloco o nó de volta na fila
        heapq.heappush(listaNo, merge)
    
    #Retornar a árvore já formada
    return listaNo[0]


#Criar um dicionário com o codigo de huff para cada valor
def criarHuffmanCod(no, codigoDaLetra, dicio):
    if no is None:
        return

    if no.char is not None:
        dicio[no.char] = codigoDaLetra
        return

    criarHuffmanCod(no.left, codigoDaLetra + "0", dicio)
    criarHuffmanCod(no.right, codigoDaLetra + "1", dicio)


#Cromprimir
def compactar(dados):
    arvore = contrucaoArvore(dados)
    huffmanCodigos = dict()
    criarHuffmanCod(arvore, "", huffmanCodigos)
    textoCodificado = "".join(huffmanCodigos[char] for char in dados)
    return textoCodificado, arvore, huffmanCodigos


#Descomprimir 
def descompactar(textoCodi, arvoreHuff):
    nodeH = arvoreHuff
    descodificado = ""

    for bit in textoCodi:
        if bit == '0':
            nodeH = nodeH.left
        else:
            nodeH = nodeH.right

        if nodeH.char is not None:
            descodificado += nodeH.char
            nodeH = arvoreHuff

    descodificado = bitarray(descodificado)
    return descodificado


def arquivoBin(tree, textoCod, nomeArq):
    nomeArq += ".bin"
    sequenciaBits = bitarray(textoCod)

    with open(nomeArq, "wb+") as arquivo:
        # Colocar a árvore no arquivo
        listinha = [tree, len(textoCod)]
        pickle.dump(listinha, arquivo)
        arquivo.write(sequenciaBits.tobytes())


#Tirar o arq de binário
def rollback(nomeArq):
    bitsLidos = bitarray()
    #Abrir o arquivo
    with open(nomeArq, "rb+") as arquivo:
        #Pego a árvore e o texto (byte)
        arvore_Len = pickle.load(arquivo)
        bitsLidos.frombytes(arquivo.read())

    bitsLidos = bitsLidos[:arvore_Len[1]]
    sequenciaBits = bitsLidos.to01()

    return descompactar(sequenciaBits, arvore_Len[0])


#Compactar usando o terminal
if __name__ == "__main__":
    #Verifica se foram fornecidos três argumentos na linha de comando
    if len(sys.argv) != 4:
        print("Modo de Uso: python testesHuff.py compress/descompress nome_arquivo.txt nome_arquivo_saida")
    else:
        modo = sys.argv[1]
        arquivoParaProcessar = sys.argv[2]
        novoNome = sys.argv[3]

        #Modo de compressão
        if modo == "compress":
            with open(arquivoParaProcessar, "rb+") as file:
                bits = bitarray()
                bits.fromfile(file)
                bits = bits.to01()

                data = list()
                tam = 0
                for i in range(0, len(bits), 8):
                    tam += 8
                    data.append(bits[i:tam])

            dataCompactada, arvoreHuffman, dictDeHuffman = compactar(data)

            arquivoBin(arvoreHuffman, dataCompactada, novoNome)

            print(f"Arquivo compactado salvo como {novoNome}.bin")


        #Modo de descompressão
        elif modo == "descompress":
            arquivoDescompactado = rollback(arquivoParaProcessar)

            with open(novoNome, "wb+") as file:
                file.write(arquivoDescompactado.tobytes())

            print(f"Arquivo descompactado salvo como {novoNome}")

        else:
            print("Modo não reconhecido. Use 'compress' ou 'descompress'.")

#Como usar no terminal:
#"Modo de Uso: python testesHuff.py compress/descompress nome_arquivo.txt nome_arquivo_saida"
