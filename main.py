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

        if type(dataframe) != type(None):
            print(dataframe.to_string())

    strIn = input()
