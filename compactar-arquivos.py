import heapq

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
        return self.freq == outro.freq
        

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

        #Crio um nó com valor vazio e com frequência sendo a soma dos outros nós
        merge = Node(None, esquerda.freq + direita.freq)
        merge.left = esquerda
        merge.right = direita

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

#Main
textao = "ta bad"
jacod, tree, d = compactar(textao)
print("Input:", textao)
print("Compactado:", jacod)
print("Dicionário e códigos:", d)
