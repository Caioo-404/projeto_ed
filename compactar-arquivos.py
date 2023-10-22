import heapq

#Criando uma classe de nós huffman
class node:
    #Construtor
    def __init__(self, valor, frequecia):
        self.char = valor
        self.freq = frequecia
        self.left = None
        self.right = None

    #Representação em string (ajuda na visualização da heap)
    def __repr__(self):
        return "( " + str(self.char) + " )"
    
    #Comparar na class
    def __lt__ (self, outra):
        return self.freq < outra.freq


def contrucaoArvore(text):
    #Ver frequência de cada caracter e colocar em um dict:
    frequencia = dict()
    for char in text:
        if char in frequencia:
            frequencia[char] += 1
        else:
            frequencia[char] = 1

    #Criar uma lista de nó-huffman (valor e frequência)
    listaNo = [node(char, freq) for char, freq in frequencia.items()]
    
    #Transformar a lista em um heapq (árvoreBin/prioridade)
    heapq.heapify(listaNo)

    #Construir a árvore de Huffman
    while len(listaNo) > 1:
        #Remover elementos de menor frequência
        esquerda = heapq.heappop(listaNo)
        direita = heapq.heappop(listaNo)

        #Crio um nó com valor vazio e com frequência sendo a soma dos outros nós
        merge = node(None, esquerda.freq + direita.freq)
        merge.left = esquerda
        merge.right = direita

        #Coloco o nó de volta na fila
        heapq.heappush(listaNo, merge)
    
    #Retornar a árvore já formada
    return listaNo[0]
