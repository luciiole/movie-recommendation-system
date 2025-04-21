import pandas as pd
ERROR = 'no movies found'
import main

def readBoxd():
    try:
        watched = pd.read_csv('watched.csv')
        return watched
    except:
        print('error loading in your watched data :(')
        return False #put in main to stop program if readBoxd = false

def findGenre(watched):
    movies = main.readFile()
    byGenre = {}
    for i, row in movies.iterrows():
        genres = row['genres'].split('|') #file uses these instead of commas
        for genre in genres:
            genre = genre.strip().lower()##
            if genre not in byGenre:
                byGenre[genre] = [] #check if genre alr in dict, if not it makes a new term for the new genre
            #now we can add the name of the movie to its correct genre
            byGenre[genre].append(row['title'])

    genres = list(byGenre.keys())
    genreCount = {}
    for genre in genres:
        genreCount[genre] = 0 #create an empty dict to count how often each genre comes up

    for key in byGenre: #for each genre in byGenre,
        for movie in byGenre[key]: #loop thro each movie in current genre in byGenre
            movieAndDate = movie.split(' (') #cos the format of movies in the kaggle file has the date in the title but letterboxd doesnt
            movie = movieAndDate[0]
            for i, row in watched.iterrows():
                if movie == row['Name']:
                    genreCount[key] += 1

    #find most watched genre
    #print(genreCount)
    orderedGenres = sorted(genreCount.items(), key=lambda x:x[1], reverse=True)
    mostWatchedGenre = orderedGenres[0][0]
    #print(mostWatchedGenre)
    return mostWatchedGenre, movies

def main3():
    print('loading in the data...')
    watched = readBoxd()
    mostWatchedGenre, movies = findGenre(watched)
    print('...data loaded in!')
    print(f"your most watched genre is {mostWatchedGenre}!")
    try:
        recs = int(input('how many recommendations do you want?'))
        if recs > 0:
            valid = True
        else:
            print('whole numbers above 0 please!!')
    except ValueError:
        print('positive integers please!')
        valid = False
    main.hashTable(movies, mostWatchedGenre, recs)

if __name__ == '__main__':
    main3()