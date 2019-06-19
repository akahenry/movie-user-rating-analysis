import time

# Função para auxiliar no debug do tempo. exemplo de uso depois da definição.
class Time():
    def __init__(self, timesTag):
        self.timeList = [time.time()]
        self.labels = []
        self.tag = timesTag

    def time(self, label):
        self.timeList.append(time.time())
        self.labels.append(label)

    def print(self):
        if (len(self.labels) != len(self.timeList) - 1):
            print("Number of labels is incompatible with number of time values")
        else:
            print('\n{s:{c}^{n}}'.format(s= self.tag + " timings",n=50,c='-'))
            for i in range(len(self.labels)):
                print("{}: {:.3f}s".format(self.labels[i], self.timeList[i+1]-self.timeList[i]))
            print('{s:{c}^{n}}'.format(s="",n=50,c='-'))

# # Exemplo de uso:
# time = Time("label do conjunto de tempos")
# # <bloco de codigo>
# time.time("bloco de codigo 1")
# # <bloco de codigo>
# time.time("bloco de codigo 2")
# # <bloco de codigo>
# time.time("bloco de codigo 3")
# time.print()
