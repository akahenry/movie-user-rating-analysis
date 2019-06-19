# Classe da Hash. Usa função de hash polinomial, com linear probing.
# Como dados, deve ser uma tupla cujo primeiro elemento é a chave.
# exemplo de uso em baixo da definição da classe.
class Hash():
    def __init__ (self, length):
        self.length = length
        self.hash_list = list()
        for i in range(length):
            self.hash_list.append(None)

    # A função de Hash
    def get_index (self, key):
        index = 0
        i = 0
        digit_key = key
        while (digit_key != 0):
            index += (digit_key % 10) * 41**i
            digit_key = digit_key // 10
            i += 1
        return index

    def insert (self, key, data):
        index = self.get_index(key) % self.length
        for i in range(self.length):
            if self.hash_list[(index + i) % self.length] == None:
                self.hash_list[(index + i) % self.length] = data
                break

    def search (self, key):
        index = self.get_index(key) % self.length
        for i in range(self.length):
            if self.hash_list[(index + i) % self.length][0] == key:
                return self.hash_list[(index + i) % self.length]
                break

    def change (self, key, data):
        index = self.get_index(key) % self.length
        for i in range(self.length):
            if self.hash_list[(index + i) % self.length][0] == key:
                self.hash_list[(index + i) % self.length] = data
                break

# # Exemplo de uso:
# hash = Hash(30)
# hash.insert(10)
# hash.insert(20)
# hash.insert(30)
# print(hash.hash_list)
