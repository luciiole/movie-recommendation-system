import pandas as pd
import time
ERROR = 'no movies found'

def readFile():
    try:
        movies = pd.read_csv('movies.csv')
        return movies
    except:
        print('File not found')
        return False

#linear search
def linearSearch(movies, user, recs):
    start = time.time()
    #findMovies = movies[movies['genres'].str.lower().str.contains(user, na=False)] #not case sensitive
    found = False #tweak to run n times
    findMovies = []
    for i, movie in movies.iterrows():
        m = movie['genres'].split('|')
        m = [x.lower() for x in m] #loop thro to lower each item so can match
        #loop thro whole list
        for item in m:
            if item == user:
                found = True
                break #need at least 1 genre to match
        if found == True and movie['title'] not in findMovies:
            findMovies.append(movie['title'])
        if len(findMovies) == recs:
            break
        found = False
    print('\nLinear Search Results + Stats:')
    if len(findMovies) == 0:
        print(ERROR)
    else:
        print(findMovies)
    end = time.time()
    print(f"linear search duration: {round(end - start, 5)} seconds\n")
    return round(end - start, 5)

#hash table
def hashTable(movies, user, recs):
    #setting up the dictionary
    byGenre = {}
    for i, row in movies.iterrows():
        genres = row['genres'].split('|') #file uses these instead of commas
        for genre in genres:
            genre = genre.strip().lower()##
            if genre not in byGenre:
                byGenre[genre] = [] #check if genre alr in dict, if not it makes a new term for the new genre
            #now we can add the name of the movie to its correct genre
            byGenre[genre].append(row['title'])

    #hash table search
    start = time.time()
    search = byGenre.get(user, ERROR) #checks if the genre is in the dict, if it isnt it returns an empty list
    print('Hash Table Results + Stats:')
    if search != ERROR:
        print(search[:recs])
    else:
        print(ERROR)
    end = time.time()
    print(f"hash table: {round(end - start, 5)} seconds")
    return round(end - start, 5)

def userInput():
    user = str(input('whats ur fave genre?')).lower().strip()
    return user

def main():
    valid = False
    print('Welcome to the Movie Recommendation System !!!')
    movies = readFile()
    if movies is False:
        print('....File not found :(')
    else:
        user = userInput()
        while valid == False:
            try:
                recs = int(input('how many recommendations do you want?'))
                if recs > 0:
                    valid = True
                else:
                    print('whole numbers above 0 please!!')
            except ValueError:
                print('positive integers please!')
                valid = False
        linearTime = linearSearch(movies, user, recs)
        hashTime = hashTable(movies, user, recs)
    return linearTime, hashTime
if __name__ == '__main__':
    main()