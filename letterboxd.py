import pandas as pd
ERROR = 'no movies found'
import main

def readBoxd():
    try:
        watched = pd.read_csv('watched.csv')
        ratings = pd.read_csv('ratings.csv')
        databaseRatings = pd.read_csv('databaseRatings.csv')
        return watched, ratings, databaseRatings
    except:
        print('error loading in your watched data :(')
        return False #put in main to stop program if readBoxd = false

def findGenre(watched, ratings, databaseRatings):
    movies = main.readFile()
    byGenre = {}
    movieAndId = {} ##
    for i, row in movies.iterrows():
        genres = row['genres'].split('|') #file uses these instead of commas
        for genre in genres:
            genre = genre.strip().lower()##
            if genre not in byGenre:
                byGenre[genre] = [] #check if genre alr in dict, if not it makes a new term for the new genre
            #now we can add the name of the movie to its correct genre
            byGenre[genre].append(row['title'])
            movieAndId[row['title']] = row['movieId'] ##

    movieAndUserId = {}
    userMovieandRatings = {}
    #for movie in movieAndId: #use
        #id = movieAndId[movie]
    for j, row in databaseRatings.iterrows():
        user = int(row['userId'])
        id = int(row['movieId'])
        if id not in movieAndUserId:
            movieAndUserId[id] = []
        movieAndUserId[id].append(user)
        if user not in userMovieandRatings:
            userMovieandRatings[user] = []
        userMovieandRatings[int(row['userId'])].append(int(row['movieId']))
        userMovieandRatings[int(row['userId'])].append(float(row['rating']))
    #so now wehave a dictionary of movie ids and userids of those who watched it
    #and we have {user:movie, rating}

    genres = list(byGenre.keys())
    #print(movieAndId) #works!
    genreCount = {}
    mostLikedGenre = {}
    for genre in genres:
        genreCount[genre] = 0 #create an empty dict to count how often each genre comes up
        mostLikedGenre[genre] = 0 #same for dict of most liked genre!

    #finding most watched genre, and most liked genres
    bestMovies = []
    for key in byGenre: #for each genre in byGenre,
        for movie in byGenre[key]: #loop thro each movie in current genre in byGenre
            movieAndDate = movie.split(' (') #cos the format of movies in the kaggle file has the date in the title but letterboxd doesnt
            movie = movieAndDate[0]
            for i, row in watched.iterrows(): #if the current movie in the genre thing is in user's letterboxd watched, add 1 to genre count
                if movie == row['Name']:
                    genreCount[key] += 1
            for j, row2 in ratings.iterrows():
                if movie == row2['Name'] and row2['Rating'] >= 4:
                    mostLikedGenre[key] += 1
                    bestMovies.append(row2['Name']) #this will use letterboxd format not kaggle w date
    #find most watched genre
    #print(genreCount)
    orderedGenres = sorted(genreCount.items(), key=lambda x:x[1], reverse=True)
    orderedMostLikedGenre = sorted(mostLikedGenre.items(), key=lambda x:x[1], reverse=True)
    bestGenre = orderedMostLikedGenre[0][0]
    secondBestGenre = orderedMostLikedGenre[1][0]
    mostWatchedGenre = orderedGenres[0][0]
    #print(orderedMostLikedGenre) ##
    #print(mostWatchedGenre)

    #find similar users
    Ids = []
    similarUsers = []
    #for movie in bestMovies: ###################
    for i in range(1): #maybe an onhover or on click, then sub i for movie user hovers onto
        movie = bestMovies[i] #change i for the index of the movie that the user clicks so take user input then loop thro bestmovies to find the movie's index
        for a, row in movies.iterrows(): #could do this using movieAndId???
            titleAndDate = row['title'].split(' (')
            title = titleAndDate[0]
            if title == movie:
                Ids.append(row['movieId'])
            #print(Ids) ##
        for id in Ids:
            for b, user in databaseRatings.iterrows():
                if user['userId'] not in similarUsers and id == user['movieId'] and user['rating'] >= 4.0:
                   similarUsers.append(int(user['userId']))
            #print(similarUsers) ##
    #print(similarUsers)
    #print(Ids)
    #print(bestMovies) #all works up to here!

    #make rec
    #best genre
    #use recAverages
    recAverages = {}
    for movie in byGenre[bestGenre]:
        score = 0
        '''
        score = 0
        for a, row in movies.iterrows():
            movieAndDate = row['title'].split(' (')
            title2 = movieAndDate[0]
            print(movie) #
            print(title2) #
            if title2 == movie:
                movieId = row['movieId']
                break ##
        '''
        movieId = movieAndId[movie] #find the movie id
        #print(movieAndUserId) #runs perfectly!
        try:
            usersThatWatched = movieAndUserId[movieId]
        except KeyError: #incase its a movie eg 1076 which nobody has watched, so its not in the usersThatWatched dictionary
            pass
        #print(usersThatWatched) #i think it works now!
        count = 0
        #print(movieId)#
        run = True
        for user in usersThatWatched:
            if user in similarUsers:
                movieIdAndRating = userMovieandRatings.get(user)
                for i, m_Id in enumerate(movieIdAndRating):
                    if m_Id == movieId:
                        rating = movieIdAndRating[i+1]
                        score += rating
                        count += 1
        '''for b, row2 in databaseRatings.iterrows(): #line below checks it is a similar user, check we're not rec a movie the user has watched before and
            run = True
            #only runs if the similar user's watched movie is in our most liked genre (movieId is the id of a movie in this genre), and the user is a siimilar user, and < movieId speeds it up
            while (int(row2['movieId']) == movieId) and run == True and int(row2['userId'] in similarUsers) and movieId not in Ids: #so it goes to next user
                #print('running!')#
                print(print(int(row2['userId']), int(row2['movieId']), movieId))
                #print(row2['userId'])
                #below line lowkey unneeded
                #the blocks below + the count + score all work!
                if int(row2['userId']) in similarUsers and movieId not in Ids and movieId == int(row2['movieId']):
                    score += float(row2['rating'])
                    print(score)
                    count += 1
                    #print(row2['movieId'])
                    print(f" count {count} yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")##
                run = False'''
        try:
            averageScore = score / count
        except ZeroDivisionError:
            averageScore = 0
        recAverages[movie] = averageScore

    orderedBestRec = sorted(recAverages.items(), key=lambda x: x[1], reverse=True)

    #print(orderedBestRec) #it works!!!
    print(f"users like you also watched {orderedBestRec[0][0]}, {orderedBestRec[1][0]}, {orderedBestRec[2][0]}")

    return mostWatchedGenre, movies, bestGenre, secondBestGenre, orderedBestRec

def main3():
    print('loading in the data...')
    watched, ratings, databaseRatings = readBoxd()
    print('...data loaded in! calculating stats..', end='')
    mostWatchedGenre, movies, bestGenre, secondBestGenre, orderedBestRec = findGenre(watched, ratings, databaseRatings)
    print('results are in!!')
    print(f"your most watched genre is {mostWatchedGenre}!")
    print(f"your most liked genre is {bestGenre}, followed by {secondBestGenre}!")
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