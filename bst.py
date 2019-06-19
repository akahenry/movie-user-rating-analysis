# Classe da Árvore Binária de Busca. deve ser inicializada com um valor na raiz.
class BST:
    def __init__(self, key, data):
        self.l = None
        self.r = None
        self.key = key
        self.data = data

    # Insere na BST, e se a chave já existe, atualiza os dados.
    def insert(self, key, data):
        if(key == self.key):
            self.data = data

        elif(key < self.key):
            if(self.l != None):
                self.l.insert(key, data)
            else:
                self.l = BST(key, data)
        else:
            if(self.r != None):
                self.r.insert(key, data)
            else:
                self.r = BST(key, data)

    # Procura na Árvore - retorna None caso não ache.
    def search(self, key):
        if(key == self.key):
            return self.data

        elif(key < self.key):
            if(self.l != None):
                return self.l.search(key)
            else:
                return None
        else:
            if(self.r != None):
                return self.r.search(key)
            else:
                return None

    def print(self):
        self._print(0)

    def _print(self, n):
        print('  ' * n + str(self.key) + " - " + str(self.data))
        if(self.l != None):
            self.l._print(n+1)
        if(self.r != None):
            self.r._print(n+1)

# # Exemplo de uso:
# # (funciona com números e strings de chave, e qualquer coisa de dados)
# bst = BST("marcos", 99999)
# bst.insert("fred", 2)
# bst.insert("zenry", 3)
# bst.print()
# print(bst.search("zenry"))
