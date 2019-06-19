class trieNode():
    def __init__(self):
       self.children = []
       self.char = None
       self.value = None  
       
    def insert(self, key, value):
        node = self
        for char in key:
            found = False
            for child in node.children:
                if child.char == char:
                    found = True
                    node = child
            
            if not found:
                auxnode = trieNode()
                auxnode.char = char
                node.children.append(auxnode)
                node = node.children[-1]
        node.value = value
                 
    def find(self, key):
        node = self
        for char in key:
            found = False
            for child in node.children:
                if child.char == char:
                    found = True
                    node = child
            
            if not found:
                return None
        return node.value
        
    def print(self):
        for child in self.children:
            print(child.char)
            child.print()
        
    

