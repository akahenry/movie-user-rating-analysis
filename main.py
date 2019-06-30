from readFiles import *
from timeClass import Time
import pandas as pd
import os

# cls: void -> void
# Objetivo: limpa o console.
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

# movieSearch: string trieNode Hash -> pd.DataFrame
# Objetivo: dados um prefixo, uma trie e uma hash referente aos filmes, a função
#   devolve um dataframe em que as colunas são 'movieId', 'title', 'genres', 'rating'
#   e 'count'. Além disso, cada linha se refere a um filme que contém o prefixo dado
#   como prefixo de seu nome.
def movieSearch(prefix, trie, movieHASH):
    list = trie.find(prefix)
    if list != []:
        df = pd.DataFrame(columns=['movieId', 'title', 'genres', 'rating', 'count'])
        for tuple in list:
            title = tuple[0]
            movieId = tuple[1]
            element = movieHASH.search(movieId)

            genres = element.data[0]
            rating = element.data[2]
            count = element.data[3]

            auxDF = pd.DataFrame([[movieId, title, genres, rating, count]], columns=['movieId', 'title', 'genres', 'rating', 'count'])
            df = df.append(auxDF)

        return df
    else:
        return None

# userSearch: int Hash Hash -> pd.DataFrame
# Objetivo: dados um id de usuário, uma hash de usuários e uma hash de filmes, a função
#   devolve um dataframe em que as colunas são 'user_rating', 'title', 'global_rating' e
#   'count'. Além disso, cada linha se refere a um filme que esse usuário avaliou.
def userSearch(userId, userHASH, movieHASH):
    df = pd.DataFrame(columns=['user_rating', 'title', 'global_rating', 'count'])
    userTemp = userHASH.search(userId)
    if userTemp != None:
        for tuple in userTemp.data:
            user_rating = tuple[1]
            movieId = tuple[0]
            movieTemp = movieHASH.search(movieId)
            title = movieTemp.data[4]
            global_rating = movieTemp.data[2]
            count = movieTemp.data[3]

            auxDF = pd.DataFrame([[user_rating, title, global_rating, count]], columns=['user_rating', 'title', 'global_rating', 'count'])
            df = df.append(auxDF)

        print(df.to_string())
    else:
        return None

# StringToTags: str -> list
# Objetivo: dado uma string com nomes de tags no formato "'<tag1>' '<tag2>' (...)", retorna
#   uma lista com os nomes das tags. Neste caso, retornaria ["tag1", "tag2"].
def StringToTags(tagStr):
    inWord = False
    tag = ""
    tagList = []

    for ch in tagStr:
        if not inWord and ch == "'":
            inWord = True
        elif not inWord and ch != "'":
            continue
        elif inWord and ch == "'":
            inWord = False
            tagList.append(tag)
            tag = ""
        elif inWord and ch != "'":
            tag = tag + ch

    return tagList

# tagSearch: int str Hash -> pd.DataFrame
# Objetivo: dado um número n, uma string s e uma Hash de filmes, retorna um
#   dataframe em que as colunas são 'title', 'genres', 'rating' e 'count',
#   e as n linhas são um filme cada, que contém o gênero s, e no mínimo 1000
#   ratings. (ordenado pelo rating, decrescentemente)
def topSearch(n, genre, movieHASH):
    # Sub-função para inserir um filme no lugar certo,  em uma lista já
    # ordenada de filmes.
    def insort(ls, item):
        if ls == [] or item.data[2] < ls[-1].data[2]:
            ls.append(item)
        for i in range(len(ls)):
            if ls[i].data[2] < item.data[2]:
                ls.insert(i, item)
                break

    # Vai inserindo na lista, e retirando o último elemento (quando a lista
    # tem tamanho n)
    movieList = []
    for movie in movieHASH.iterable():
        ## ATENÇÃO: QUANDO FOR RODAR COM RATING.CSV, TROCAR 10 POR 1000 ##
        if movie.data[3] >= 10:
            if genre in movie.data[0].split('|'):
                if len(movieList) < n:
                    insort(movieList, movie)
                elif movie.data[2] > movieList[-1].data[2]:
                    insort(movieList, movie)
                    movieList = movieList[:n]

    # Cria e retorna o dataframe
    df = pd.DataFrame(columns=['title', 'genres', 'rating', 'count'])
    for movie in movieList:
        title = movie.data[4]
        genres = movie.data[0]
        rating = movie.data[2]
        count = movie.data[3]

        auxDF = pd.DataFrame([[title, genres, rating, count]], columns=['title', 'genres', 'rating', 'count'])
        df = df.append(auxDF)

    return df

# tagSearch: list -> pd.DataFrame
# Objetivo: dados uma lista de tags, a função devolve um dataframe em que as colunas
#   são 'title', 'genres', 'rating' e 'count', onde cada linha é um filme que contém
#   todas as tags na lista de tags.
def tagSearch(tagList, movieHASH):
    movieList = []
    df = pd.DataFrame(columns=['title', 'genres', 'rating', 'count'])
    for movie in movieHASH.iterable():
        # Coloca todos filmes da primeira tag
        tag = tagList[0]
        if tag in movie.data[1]:
            if movie not in movieList:
                movieList.append(movie)

    # Tira os filmes que não tem as outras tags
    for tag in tagList[1:]:
        filter(lambda x: tag in x.data[1], movieList)

    for movie in movieList:
        title = movie.data[4]
        genres = movie.data[0]
        rating = movie.data[2]
        count = movie.data[3]

        auxDF = pd.DataFrame([[title, genres, rating, count]], columns=['title', 'genres', 'rating', 'count'])
        df = df.append(auxDF)

    if movieList != []:
        return df
    else:
        return None


time = Time("main")

# Lendo arquivos CSV
movieMatrix = readCSV("movie.csv")
ratingMatrix = readCSV("rating.csv")
tagMatrix = readCSV("tag.csv")

print("Li CSV")

time.time("load_files")

trie = createTrie(movieMatrix)

print("Criei Trie")

time.time("create_trie")

userHASH = Hash(len(ratingMatrix))
movieHASH = Hash(int(movieMatrix[-1][0]))

time.time("initialize_hash")

time.print()

# Adiciona id e generos dos filmes
for movie in movieMatrix:
    movieId = int(movie[0])
    name = movie[1]
    genres = movie[2]
    movieHASH.insert(movieId, (genres, [], 0, 0, name))

time.time("add_movie_id")

time.print()

# Para cada rating, incrementa numero de rating do filme e seu somatório de notas
for rating in ratingMatrix:
    userId = int(rating[0])
    movieId = int(rating[1])
    ratingValue = float(rating[2])

    userHASH.append(userId, (movieId, ratingValue))
    aux = movieHASH.search(movieId)
#(genres, tags, mean, n_ratings, name)
    if aux != None:
        movieHASH.insert(movieId, (aux.data[0], aux.data[1], aux.data[2] + ratingValue, aux.data[3] + 1, aux.data[4]))

del ratingMatrix

time.time("read rating")

time.print()

# Calcula a média de notas de cada filme
for movie in movieMatrix:
    movieId = int(movie[0])
    movieTemp = movieHASH.search(movieId)
    if(movieTemp != None and movieTemp.data[3] != 0):
        movieHASH.insert(movieId, (movieTemp.data[0], [], movieTemp.data[2]/movieTemp.data[3], movieTemp.data[3], movieTemp.data[4]))

del movieMatrix

time.time("calculate_media")

time.print()

# Insere as Tags na Hash de filmes.
for tag in tagMatrix:
    movieId = int(tag[1])
    tagName = tag[2]

    movieTemp = movieHASH.search(movieId)

    if movieTemp != None and tagName not in movieTemp.data[1]:
        movieHASH.insert(movieId, (movieTemp.data[0], movieTemp.data[1] + [tagName], movieTemp.data[2], movieTemp.data[3], movieTemp.data[4]))

del tagMatrix
time.time("insert_tag")

time.time("create_hash")

time.print()

# Console:
strIn = input()
while strIn != "Exit":
    cls()
    auxVector = strIn.split(' ')
    dataframe = None
    if len(auxVector) <= 1:
        print("Error.")
    else:
        if auxVector[0] == "movie":
            prefix = strIn.replace("movie ", "")
            print(prefix)
            dataframe = movieSearch(prefix, trie, movieHASH)
        elif auxVector[0] == "user":
            userId = int(auxVector[1])
            dataframe = userSearch(userId, userHASH, movieHASH)
        elif auxVector[0][0:3] == "top":
            dataframe = topSearch(int(auxVector[0][3:]), auxVector[1].strip("'"), movieHASH)
        elif auxVector[0] == "tags":
            taglist = StringToTags(strIn.replace("tags ", ""))
            dataframe = tagSearch(taglist, movieHASH)

        if type(dataframe) != type(None):
            print(dataframe.to_string())

    strIn = input()
