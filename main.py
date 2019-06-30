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
def movieSearch(prefix, trie, movieHash):
    list = trie.find(prefix)
    if list != []:
        df = pd.DataFrame(columns=['movieId', 'title', 'genres', 'rating', 'count'])
        for tuple in list:
            title = tuple[0]
            movieId = tuple[1]
            element = movieHash.search(movieId)
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
def userSearch(userId, userHash, movieHash):
    df = pd.DataFrame(columns=['user_rating', 'title', 'global_rating', 'count'])
    userTemp = userHash.search(userId)
    if userTemp != None:
        for tuple in userTemp.data:
            user_rating = tuple[1]
            movieId = tuple[0]
            movieTemp = movieHash.search(movieId)
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
def topSearch(n, genre, movieHash):
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
    for movie in movieHash.iterable():
        if movie.data[3] >= 1000:
            if genre in movie.data[0].split('|'):
                if len(movieList) <= n:
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
def tagSearch(tagList, movieHash):
    movieList = []
    df = pd.DataFrame(columns=['title', 'genres', 'rating', 'count'])
    for movie in movieHash.iterable():
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
ratingMatrix = readCSV("minirating.csv")
tagMatrix = readCSV("tag.csv")

time.time("load_files")

trie = createTrie(movieMatrix)

time.time("create_trie")

Hashs = createHashs(movieMatrix, ratingMatrix, tagMatrix)

userHash = Hashs[0]
movieHash = Hashs[1]

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
            dataframe = movieSearch(prefix, trie, movieHash)
        elif auxVector[0] == "user":
            userId = int(auxVector[1])
            dataframe = userSearch(userId, userHash, movieHash)
        elif auxVector[0][0:3] == "top":
            dataframe = topSearch(int(auxVector[0][3:]), auxVector[1].strip("'"), movieHash)
        elif auxVector[0] == "tags":
            taglist = StringToTags(strIn.replace("tags ", ""))
            dataframe = tagSearch(taglist, movieHash)

        if type(dataframe) != type(None):
            print(dataframe.to_string())

    strIn = input()
