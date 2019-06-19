from readFiles import *
from timeClass import Time

time = Time("main")

movieMatrix = readCSV("movie.csv")
ratingMatrix = readCSV("minirating.csv")

time.time("load_files")

trie = createTrie(movieMatrix)

time.time("create_trie")

movieHash = createMovieHash(movieMatrix, ratingMatrix)

time.time("create_hash")

time.print()
