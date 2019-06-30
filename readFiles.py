import csv
from trie import *
from hash import *

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

# createHashs: matrix matrix matrix -> (hash, hash)
# Objetivo: dada duas matrizes referentes a leitura dos arquivos:
# 	- movies.csv
#	- rating.csv
#	a função retorna uma tupla com o primeiro elemento sendo a hash de usuários
#	e o segundo a hash de filmes.
# 	-UserHASH: cria a hash onde cada entrada é um usuário, usando
# 		como chave o userId, e como dados uma lita de 2-upla:
# 		(movieId, rating)
# 		onde movieId é o id do filme avaliado pelo usuário e rating é a avaliação
#		que esse usuário deu para o filme em questão.
# 	-MovieHASH: cria a hash onde cada entrada é um filme, usando
# 		como chave o movieId, e como dados uma 5-upla:
# 		(genres, tags, mean, n_ratings, name)
# 		onde genres é uma lista de gêneros, tags é uma lista de tags, mean é a média
#		de avaliações, n_ratings é o número de avaliações e name é o nome do filme.
def createHashs(movieMatrix, ratingMatrix, tagMatrix):
	# Cria a hash com o dobro do número de entradas
	userHASH = Hash(len(ratingMatrix))
	movieHASH = Hash(int(movieMatrix[-1][0]))

	# Adiciona id e generos dos filmes
	for movie in movieMatrix:
		movieElement = Hash_element()
		movieElement.key = int(movie[0])
		movieElement.data = (movie[2], [], 0, 0, movie[1])
		movieHASH.insert(movieId, movieElement)

	# Para cada rating, incrementa numero de rating do filme e seu somatório de notas
	for rating in ratingMatrix:
		userElement.key = int(rating[0])
		movieElement.key = int(rating[1])
		ratingValue = float(rating[2])

		movieTemp = movieHASH.search(movieElement.key)

		if movieTemp != None:
			genres = movieTemp.data[0]
			old_num_ratings = movieTemp.data[3]
			old_sum = movieTemp.data[2]
			name = movieTemp.data[4]

			movieHASH.insert(movieId, (genres, [], old_sum + ratingValue, old_num_ratings + 1, name))

		userHASH.append(userId, (movieId, ratingValue))

	# Calcula a média de notas de cada filme
	for movie in movieMatrix:
		movieId = int(movie[0])
		movieTemp = movieHASH.search(movieId)
		if(movieTemp != None and movieTemp.data[3] != 0):
			movieHASH.insert(movieId, (movieTemp.data[0], [], movieTemp.data[2]/movieTemp.data[3], movieTemp.data[3], movieTemp.data[4]))

	# Insere as Tags na Hash de filmes.
	for tag in tagMatrix:
		movieId = int(tag[1])
		tagName = tag[2]

		movieTemp = movieHASH.search(movieId)

		if movieTemp != None and tagName not in movieTemp.data[1]:
			movieHASH.insert(movieId, (movieTemp.data[0], movieTemp.data[1] + [tagName], movieTemp.data[2], movieTemp.data[3], movieTemp.data[4]))

	return (userHASH, movieHASH)

def createTrie(movieMatrix):
	trie = trieNode()

	for movie in movieMatrix:
		trie.insert(movie[1], int(movie[0]))

	return trie
