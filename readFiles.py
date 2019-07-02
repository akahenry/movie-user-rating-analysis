import csv
from trie import *
from hash import *

# createHashs: matrix matrix matrix -> (hash, hash)
# Objetivo: dados três arquivos:
# 	- movies.csv
#	- rating.csv
#	- tag.csv
#	a função retorna uma tupla com o primeiro elemento sendo a hash de filmes
#	e o segundo a hash de usuários.
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
def createHashs(rating_file, movie_file, tag_file):
	# Escolhe o tamanho e cria a hash de filmes
	movie_file.seek(0)
	for line in movie_file:
		last_line = line
	movieHASH = Hash(int(last_line.split(",")[0]))
	movie_file.seek(0)
	next(movie_file)

	# Adiciona id e generos dos filmes
	for movie in csv.reader(movie_file):
		movieId = int(movie[0])
		name = movie[1]
		genres = movie[2]
		movieHASH.insert(movieId, (genres, [], 0, 0, name))

	# Escolhe o tamanho e cria a hash de ususários
	movie_file.seek(0)
	next(rating_file)
	biggest_ID = 0
	for line in rating_file:
		next_id = int(line.split(",")[0])
		if next_id > biggest_ID:
			biggest_ID = next_id
	userHASH = Hash(biggest_ID)
	rating_file.seek(0)
	next(rating_file)

	# Para cada rating, incrementa numero de rating do filme e seu somatório de notas
	for rating_str in rating_file:
		rating = rating_str.split(",")
		userId = int(rating[0])
		movieId = int(rating[1])
		ratingValue = float(rating[2])

		userHASH.append(userId, (movieId, ratingValue))
		aux = movieHASH.search(movieId)
	    #(genres, tags, mean, n_ratings, name)
		if aux != None:
			movieHASH.insert(movieId, (aux.data[0], aux.data[1], aux.data[2] + ratingValue, aux.data[3] + 1, aux.data[4]))

	# Calcula a média de notas de cada filme
	for movie in movieHASH.iterable():
		if movie.data[3] != 0:
			movieHASH.insert(movie.key, (movie.data[0], [], movie.data[2]/movie.data[3], movie.data[3], movie.data[4]))

	# Insere as Tags na Hash de filmes.
	tag_file.seek(0)
	next(tag_file)
	for tag in csv.reader(tag_file):
		movieId = int(tag[1])
		tagName = tag[2]

		movieTemp = movieHASH.search(movieId)

		if movieTemp != None and tagName not in movieTemp.data[1]:
			movieHASH.insert(movieId, (movieTemp.data[0], movieTemp.data[1] + [tagName], movieTemp.data[2], movieTemp.data[3], movieTemp.data[4]))

	return (movieHASH, userHASH)

def createTrie(movie_file):
	trie = trieNode()

	movie_file.seek(0)
	next(movie_file)

	for movie in csv.reader(movie_file):
		trie.insert(movie[1], int(movie[0]))

	return trie
