import csv
from trie import *
from hash import *
from bst import *

def transpose(matrix):
	return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

def readCSV(filename):
	file = open(filename, 'r', encoding='utf-8')

	csvreader = csv.reader(file)

	return_list = list(list(csvreader))

	# Tira o header
	return_list = return_list[1:]

	file.close()

	return return_list

# Cria a hash onde cada entrada é um filme, usando
# como chave o movieId, e como dados uma 4-upla:
# (movieId, genres, mean, n_ratings)
# onde mean é a média de avaliações e n_ratings é o número de avaliações.
# <ADICIONAR NESSA FUNÇÃO A PARTE DE CRIAR A BST (NO MESMO LOOP DO ratingMatrix)>
def createMovieHash(movieMatrix, ratingMatrix):
	# Cria a hash com o dobro do número de entradas
	hash = Hash(len(movieMatrix)*2)

	# Inicializando a BST com a primeira chave, e um dado qualquer
	# (será atualizado mais tarde)
	bst = BST(ratingMatrix[0][0], 0)

	# Adiciona id e generos dos filmes
	for movie in movieMatrix:
		movieId = int(movie[0])
		genres = movie[2]
		hash.insert(movieId, (movieId, genres, 0, 0))

	# Para cada rating, incrementa numero de rating do filme e seu somatório de notas
	for rating in ratingMatrix:
		userId = int(rating[0])
		movieId = int(rating[1])
		ratingValue = float(rating[2])

		movieTemp = hash.search(movieId)

		genres = movieTemp[1]
		old_num_ratings = movieTemp[3]
		old_sum = movieTemp[2]

		hash.change(movieId, (movieId, genres, old_sum + ratingValue, old_num_ratings + 1))

	# Calcula a média de notas de cada filme
	for movie in movieMatrix:
		movieId = int(movie[0])
		movieTemp = hash.search(movieId)
		if(movieTemp[3] != 0):
			hash.change(movieId, (movieTemp[0], movieTemp[1], movieTemp[2]/movieTemp[3], movieTemp[3]))

	return hash

def createTrie(movieMatrix):
	trie = trieNode()

	posKey = 1
	posId = 0

	for row in movieMatrix:
		for i in range(0, len(row)):
			if i == posKey:
				key = row[i]
			elif i == posId:
				Id = row[i]
		trie.insert(key, Id)

	return trie
