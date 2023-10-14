#Criando uma classe de nos huffman
class node:
    #Construtor
    def __init__(self, valor, frequecia):
        self.char = valor
        self.freq = frequecia
        self.left = None
        self.right = None

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
    #Pro resto aprender a usar heap