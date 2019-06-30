# Hash_element: todo elemento dessa classe contém 3 parâmetros:
#   - key = é a chave do elemento, que irá ser utilizado para localizar
#       o elemento dentro da tabela e deve ser um número inteiro.
#   - data = são os dados satélites do elemento.
#   - used = é uma flag que informa se esse elemento é/já foi utilizado
#       em algum momento, para auxílio na função de inserção e busca, por
#       exemplo.
class Hash_element():
    def __init__(self):
        self.key = None
        self.data = None
        self.used = False

# Hash: todo elemento dessa classe contém 2 parâmetros:
#   - length: tamanho da tabela.
#   - hash_list: uma lista de Hash_element que se trata da tabela de Hash.
# Observação: funciona de maneira muito mais eficiente se não houver colisões
#   na tabela, devido a função de hash escolhida.
class Hash():
    def __init__(self, length):
        self.length = length
        self.hash_list = list()
        for i in range(length):
            self.hash_list.append(Hash_element())

    # h_function: int -> int
    # Objetivo: dado um número inteiro, essa função mapeia esse número a outro número
    #   de acordo com a função de Hash proposta pelo livro "The Art of Computer Programming"
    #   na seção 6.4.
    def h_function(self, key):
        return key

    # insert: int int -> boolean
    # Objetivo: dado uma chave e dados satélites, essa função realiza algumas coisas
    #   de acordo com a presença ou não dessa chave na tabela:
    #   - Se está presente: se os dados satélites que se encontram junto a chave se trata
    #       de uma lista ordenada de tuplas, então é apenas acrescentada a tupla a lista
    #       de forma a manter a ordenação. Senão, então é feito a atualização dos dados.
    #   - Se não está presente: então a função insere a chave e os dados satélites na tabela.
    # Observação: se a tabela estiver cheia e não possuir a chave dada, a função devolve False.
    #   Senão, devolve True.
    def insert(self, key, data):
        index = key%self.length
        self.hash_list[index].key = key
        self.hash_list[index].data = data
        self.hash_list[index].used = True

    def append(self, key, data):
        index = key%self.length
        if not self.hash_list[index].used:
            self.insert(key, [data])
        else:
            self.hash_list[index].data.append(data)


    # search: int -> Hash_element
    # Objetivo: dada uma chave inteira a função devolve o Hash_element referente a essa chave
    #   se ela está presente na lista. Senão, devolve None.
    def search(self, key):
        index = key%self.length
        if self.hash_list[index].key == key:
            return self.hash_list[index]
        else:
            return None

    def iterable(self):
        for hash_element in self.hash_list:
            if hash_element.key != None:
                yield hash_element
