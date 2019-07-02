class trieNode():
    def __init__(self):
       self.children = []
       self.key = None
       self.data = None

    # insert: string Any -> trieNode
    # Objetivo: dada uma árvore trie, uma string e dados satélites, essa função
    #   insere essa string na árvore trie segundo o prefixo da string dada.
    def insert(self, key, data):
        node = self
        for char in key:
            found = False
            for child in node.children:
                if child.key == char:
                    found = True
                    node = child

            if not found:
                auxnode = trieNode()
                auxnode.key = char
                node.children.append(auxnode)
                node = node.children[-1]
        node.data = data

    # find: string -> list
    # Objetivo: dada um prefixo e uma trie, a função verifica se o prefixo
    #   está na trie, retornando uma lista de tuplas dadas por:
    #   (string, data), onde:
    #   - string: palavra inteira que contém o prefixo dado como entrada.
    #   - data: dados satélites dessa palavra que estão contidos na trie.
    def find(self, key):
        node = self
        for char in key:
            flag = False
            for child in node.children:
                if child.key == char:
                    node = child
                    flag = True
                    break
            if not flag:
                return []

        def listByPrefix(node, string):
            list = []
            if node.data != None:
                list.append((string, node.data))
            for child in node.children:
                str = string
                str += child.key
                list += listByPrefix(child, str)
            return list

        return listByPrefix(node, key)

    def print(self):
        for child in self.children:
            print(child.key)
            child.print()
