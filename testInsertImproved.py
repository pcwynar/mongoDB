#!/usr/bin/env python
# the above just indicates to use python to intepret this file

# ---------------------------------------------------------------
# This mapper code will input a line of text and output <word, 1>
#
# ---------------------------------------------------------------

import sys  # a python module with system functions for this OS
import pymongo  # python MongoDB module
import datetime
import time
# connect with mongo DB here
from pymongo import MongoClient

client = MongoClient()

# set the database
db = client['moviesdb']

# set the collection
movieCollection = db.movies5_25a
# print("count->"+db.movies.count())
counter = db.moviesSunday.count()
print('{0}'.format(counter))


ratingsList = []
tagsList = []
moviesList = []



# ------------------------------------------------------------
#  this 'for loop' will set 'line' to an input line from system
#    standard input file
# ------------------------------------------------------------
# inf = open('data.txt')
# try:
#    for line in inf:
# etc
# finally:

def initTags():
    print("start Tags Load" + str(datetime.datetime.now()))
    with open('tags.dat') as inf:
        for line in inf:
            line = line.strip()
            userID, movieID, tag, timeStamp = line.split("::")  # split line at blanks (by default),
            tagNew = Tag(userID,movieID,tag)
            # print(movieID)
            # add to tagList
            #rating_record = {"movieID":movieID,"userId": userID, "rating": float(rating), "ratingDate": timeStamp}
            tagsList.append(tagNew)
    # print str
    inf.close()
    print("Ended Tags Load" + str(datetime.datetime.now()))
    return

def initMovies():
    print("start Movies Load" + str(datetime.datetime.now()))
    with open('movies.dat') as inf:
        for line in inf:
            line = line.strip()
            movieID,title,genres = line.split("::")  #split line at blanks (by default)
            movieGenres = genres.replace("|",",")
    
            movieNew = Movie(movieID,title,movieGenres)
            #print(movieID)
            #print(title)
            # add to tagList
            #rating_record = {"movieID":movieID,"userId": userID, "rating": float(rating), "ratingDate": timeStamp}
            moviesList.append(movieNew)
    # print str
    inf.close()
    print("Ended Movies Load" + str(datetime.datetime.now()))
    return

def initRatings():
    print("start Ratings Load" + str(datetime.datetime.now()))
    with open('ratings.dat') as inf:
        for line in inf:
            line = line.strip()
            userID, movieID, rating, timeStamp = line.split("::")  # split line at blanks (by default),
            ratingNew = Rating(userID,movieID,rating)

            #print("new movie id"+str(ratingNew.movieId))
            # add to tagList
            #rating_record = {"movieID":movieID,"userId": userID, "rating": float(rating), "ratingDate": timeStamp}

            ratingsList.append(ratingNew)
    # print str
    inf.close()
    print("Ended Ratings Load" + str(datetime.datetime.now()) + "_Count__=_" + str(len(ratingsList)))

    #for tester in ratingsList:
     #   print("new movie id" + str(tester.movieId))

    print("Ended Ratings Load" + str(datetime.datetime.now())+"_Count__=_"+str(len(ratingsList)))
    return

class Tag:
    def __init__(self, userId, movieId,tag):
        self.userId = userId
        self.movieId = movieId
        self.tag = tag

class Rating:
    def __init__(self, userId, movieId,rating):
        self.userId = userId
        self.movieId = movieId
        self.rating = rating

class Movie:
    def __init__(self,movieId,title,genres):
        self.movieId = movieId
        self.title = title
        self.genres = genres


def getMovie(movieId):
    #print("START Movie Query" + str(datetime.datetime.now()))
    localMoviesList =[]
    localStringList = []
    #print("inside getRatings length")
    localMoviesList = filter(lambda x: x.movieId == movieId, moviesList)
    #ratingList.remove(localRatingsList)
    for tempMovie in localMoviesList:
        movie_record = {"movieId": tempMovie.movieId,"title":tempMovie.title,"genres":tempMovie.genres}
        #movie_record = {"userId": tempRating.userId, "rating": float(tempRating.rating)}
        localStringList.append(movie_record)
        #ratingsList.remove(tempRating)

    #print(len(localRatingsList))
    #for line in ratingsList:
     #   userID, movieID, rating, timeStamp = line.split("::")  # split line at blanks (by default),
      #  if movieId == movieID:
       #     rating_record = {"userId": userID, "rating": float(rating), "ratingDate": timeStamp}
        #    localRatingsList.append(rating_record)
         #   ratingsList.remove(line)
    #localTagsList = filter(lambda x: x.movieID == movieId, tagsList)
    #print("END Movie Query" + str(datetime.datetime.now()))
    return localMoviesList


def getRatings(movieId):
    localStringList = []
    #print("inside getRatings length")
    localRatingsList = filter(lambda x: x.movieId == movieId, ratingsList)
    #ratingList.remove(localRatingsList)
    for tempRating in localRatingsList:
        rating_record = {"userId": tempRating.userId, "rating": float(tempRating.rating)}
        localStringList.append(rating_record)
    return localStringList




def getTags(movieId):
    #print("START Tags Query" + str(datetime.datetime.now()))
    localTagsList =[]
    localStringList =[]
    #print("inside getTags length")
    localTagsList = filter(lambda x: x.movieId == movieId, tagsList)
    #tagsList.remove(localTagsList)
    for tempTag in localTagsList:
        tag_record = {"userId": tempTag.userId,"tag":tempTag.tag,"movieId":tempTag.movieId}
        localStringList.append(tag_record)
        #tagsList.remove(tempTag)

    #print(len(localTagsList))
    #for line in ratingsList:
     #   userID, movieID, rating, timeStamp = line.split("::")  # split line at blanks (by default),
      #  if movieId == movieID:
       #     rating_record = {"userId": userID, "rating": float(rating), "ratingDate": timeStamp}
        #    localRatingsList.append(rating_record)
         #   ratingsList.remove(line)
    #localTagsList = filter(lambda x: x.movieID == movieId, tagsList)
    #print("END Tags Query" + str(datetime.datetime.now()))
    return localStringList




print("START --------LOAD" + str(datetime.datetime.now()))

#initalize all the global lists
initMovies()
initRatings()
initTags()

print("START Ratings LIST SORTaaaaa" + str(datetime.datetime.now()))
newlist = sorted(ratingsList, key=lambda x: x.movieId, reverse=False)
#ratingsList.sort(key=lambda x: x.movieId, reverse=True)

print("END Ratings LIST SORTbbbbb" + str(datetime.datetime.now())+"---RATINGS LIST COUNT---->"+str(len(newlist)))

tempRatingsMovieId = ""
localStringList =[]

ratingsCounter=0

#print("id1---"+str(ratingsList[1].movieId)+"----id 10000---"+str(ratingsList[1000].movieId)+"---10000mil---"+str(ratingsList[1000000].movieId))
for tempRating in newlist:

    rating_record = {"userId": tempRating.userId, "rating": float(tempRating.rating),"movieId":tempRating.movieId}
    #print("USER ID==>" + str(tempRating.userId))
    #time.sleep(1)
    #print("Ratings count==>"+str(ratingsCounter))

    if ratingsCounter == 0:
       tempRatingsMovieId = tempRating.movieId

    #print("MOVIE ID==>" + str(newlist[ratingsCounter].movieId)+"----TempMovieID==>"+tempRatingsMovieId + "----Ratings count==>" + str(ratingsCounter))

    ratingsCounter = ratingsCounter + 1

    #if ratingsCounter == 3045:
        #time.sleep(1)

    #print("tempId==>"+str(tempRatingsMovieId)+"------currentRating"+str(tempRating.movieId))
    #time.sleep(1)

    if str(tempRatingsMovieId) == str(tempRating.movieId):
        #add to list since these are all for the same movie
        localStringList.append(rating_record)
        #ratingsCounter = ratingsCounter + 1

        #tempRatingsMovieId = tempRating.movieId
        #print("SAME----movieId--"+str(tempRatingsMovieId)+"--------ratings array LENGTH==>" + str(len(localStringList)))
        #print(str(rating_record))
        tempRatingsMovieId = tempRating.movieId
        #time.sleep(1)

        #print(tempRating.movieId)
    else:
        #different movie id so go get movie and tags to insert into mongo
        print("CHANGED--OLD movieId---"+str(tempRatingsMovieId)+"---NEW movieID--->"+str(tempRating.movieId)+"----ratings array LENGTH==>"+str(len(localStringList)))
        #if str(tempRatingsMovieId) == "1016":
            #print("1016------------array LENGTH==>" + str(len(localStringList)))
            #time.sleep(5)

        # insert data into mongo

        newMovieList = getMovie(tempRatingsMovieId)
        if len(newMovieList) > 0:
            movie_record = {"movieId": newMovieList[0].movieId, "title": newMovieList[0].title,
                        "genres": [newMovieList[0].genres], "tags": getTags(tempRatingsMovieId),
                        "ratings":localStringList }
            movieCollection.insert_one(movie_record)
        # clear the list for the next movie
            localStringList = []
            localStringList.append(rating_record)
            tempRatingsMovieId = tempRating.movieId
        else:
            print("No movie record FOUND-movieId---" + str(tempRatingsMovieId) + "-------ratings array LENGTH==>" + str(len(localStringList)))
            localStringList = []
            localStringList.append(rating_record)
            tempRatingsMovieId = tempRating.movieId




        # print(line)
        # -----------------------------------
        # sys.stdin call 'sys' to read a line from standard input,
        # note that 'line' is a string object, ie variable, and it has methods that you can apply to it,
        # as in the next line
        # ---------------------------------
        # movie file format -->MovieID::Title::Genres
        # 1::Toy Story (1995)::Adventure|Animation|Children|Comedy|Fantasy

        #line = line.strip()  # strip is a method, ie function, associated
        #  with string variable, it will strip
        #   the carriage return (by default)

        #movieID, title, genres = line.split("::")  # split line at blanks (by default)

        # movieGenres = genres.replace("|",",")
        #movieGenres = genres.split("|")


        #print(getTags(movieID))
        #print(getRatings(movieID))

        # getTags(movieID)
        # getRatings(movieID)

        # print('{0}\t{1}\t{2}'.format(movieID, title, movieGenres) ) #the {} is replaced by 0th,1st items in format list

        # insert data into mongo
        # print('{0}\t{1}\t{2}'.format(movieID, title, movieGenres) )
        #inf.close()



print datetime.datetime.now()
print("total RATINGS===>"+str(ratingsCounter))
print("FINISH --------LOAD" + str(datetime.datetime.now()))
