import heapq
import pickle

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
def contrucaoArvore(text):
    #Ver frequência de cada caracter e colocar em um dict:
    frequencia = dict()
    for char in text:
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

    return descodificado


#Criar o arquivo em binário
def arquivoBin(tree, textoCod, nomeArq):
    nomeArq += ".bin"
    sequenciaBits = textoCod
    with open(nomeArq, "wb+") as arquivo:
        #Colocar a arvore no arq
        pickle.dump(tree, arquivo)

        #Colocar o texto
        byte = 0
        bitsEscritos = 0
        for bit in sequenciaBits:
            byte = (byte << 1) | int(bit)
            bitsEscritos += 1

            if bitsEscritos == 8:
                arquivo.write(bytes([byte]))
                byte = 0
                bitsEscritos = 0

        if bitsEscritos > 0:
            byte <<= 8 - bitsEscritos
            arquivo.write(bytes([byte]))


#Tirar o arq de binário
def rollback(nomeArq):
    #Abrir o arquivo
    with open(nomeArq, "rb+") as arquivo:
        #Pego a árvore e o texto (byte)
        arvore = pickle.load(arquivo)
        bytes_lidos = arquivo.read()
        
    bits = []
    #Percorra cada byte lido
    for byte in bytes_lidos:
        #Converte o byte em uma sequência de 8 bits
        byte_bits = format(byte, '08b')
        #Adiciona os bits à lista
        bits.extend(byte_bits)

    #Converte a lista de bits de volta para uma sequência de bits como uma string
    sequencia_bits = "".join(bits)
        
    return descompactar(sequencia_bits, arvore)


with open("texto1.txt.txt", "r") as file:
    textao = file.read()

jacod, tre, di = compactar(textao)

arquivoBin(tre, jacod, "newlucky")

deecodificado = rollback("newlucky.bin")

with open("descompresso.bin", "w+") as file:
    file.write(deecodificado)

#Main
'''
textao = "qualquer coisaaa"
jacod, tree, di = compactar(textao)
jadecod = descompactar(jacod, tree)
print("\nInput (texto):", textao)
print("\nCompactado:", jacod)
print("\nDescompactado:", jadecod)
print("\nDicionário e códigos:", di)



#Abrir e ler o arquivo:
with open("texto.txt", "r", encoding="utf-8") as arquivo:
    textoConteudo = arquivo.read()

#compactar e criar um novo arquivo compresso
jacod, tree, dic = compactar(texto)
jadecod = descompactar(jacod, tree)

with open("compresso.bin, "w+") as file:
    file.write(jacod)

with open("descompresso.bin", "w+") as file:
    file.write(jadecod)
'''