import os
import json
import random
import pandas as pd

GIT_REPO_NAME = "RapGPT"
DATA_FOLDER = "resources"
SAVE_FOLDER = "preparedData"
GENRES_FOLDER = "genres"
NO_GENRE = "NULL"
MANY_GENRES = "MANY"

noMatchesTags = []

def main():
    batches = [
       "song_batch_0.json",
       "song_batch_1.json",
       "song_batch_2.json",
       "song_batch_3.json",
       "song_batch_4.json",
       "song_batch_5.json",
       "song_batch_6.json", 
    ]
    for batch in batches:
        filterSongBatch(None, batch)

def filterSongBatch(tags, filename, selectAtRandom=True, removeNullGenres=True, removeEmptyLyrics=True, genresFileName="expandedChatGPT.json", saveFilePrefix="prepared"):
    """"""
    path = getPathToFile(filename)
    genres = getGenres(genresFileName)
    data = loadJson(path)
    textGenresPair = getTextGenrePairs(data, genres, selectAtRandom, removeNullGenres, removeEmptyLyrics)
    savePath = getPathToSaveFile(f"{saveFilePrefix}_{filename}")
    saveJson(textGenresPair, savePath)

def saveJson(data, path):
    if os.path.exists(path):
        userInput = input("Flie alreedy exist... ReAllY override this File? [y/N]")
        if userInput != "y":
            return
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file)

def getTextGenrePairs(data, genres, selectAtRandom=True, removeNullGenres=True, removeEmptyLyrics=True):
    returnList = []
    for dataPoint in data:
        textGenrePair = generateTextGenrePair(dataPoint, genres, selectAtRandom)
        if shouldSave(textGenrePair, removeNullGenres, removeEmptyLyrics):
            returnList.append(textGenrePair)
    return returnList

def shouldSave(textGenrePair, removeNullGenres, removeEmptyLyrics):
    if removeNullGenres and textGenrePair["Genres"] == NO_GENRE:
        return False;
    if removeEmptyLyrics and textGenrePair["Lyrics"] == "":
        return False;
    return True;

def generateTextGenrePair(dataPoint, genres: set, selectAtRandom = True):
    """selectAtRandom: if song has many genres, selects one at random and dismisses the others."""
    intersection = genres.intersection(dataPoint["LastFMTags"])
    if len(intersection) < 1:
        for tag in dataPoint["LastFMTags"]:
            noMatchesTags.append(tag.lower())
        return {"Lyrics": dataPoint["Lyrics"], "Genres": NO_GENRE, "GeniusId": dataPoint["GeniusId"]}
    if len(intersection) == 1:
        return {"Lyrics": dataPoint["Lyrics"], "Genres": list(intersection)[0], "GeniusId": dataPoint["GeniusId"]}
    if selectAtRandom:
        randomIndex = random.randint(0, len(intersection) - 1)
        return {"Lyrics": dataPoint["Lyrics"], "Genres": list(intersection)[randomIndex], "GeniusId": dataPoint["GeniusId"]}
    return {"Lyrics": dataPoint["Lyrics"], "Genres": MANY_GENRES}
    

def getPathToFile(filename):
    cwd = os.getcwd()
    head = cwd.split(GIT_REPO_NAME)
    if len(head) < 1:
        raise NameError("Cannot get the working Path. Look at Source Code and Debug. :/")
    return os.path.join(head[0], GIT_REPO_NAME, DATA_FOLDER, filename)

def getPathToSaveFile(filename):
    cwd = os.getcwd()
    head = cwd.split(GIT_REPO_NAME)
    if len(head) < 1:
        raise NameError("Cannot get the working Path. Look at Source Code and Debug. :/")
    return os.path.join(head[0], GIT_REPO_NAME, DATA_FOLDER, SAVE_FOLDER, filename)

def getGenres(filename) -> set:
    path = getPathToGenresFile(filename)
    genres = loadJson(path)
    if(genres.get("genres")):
        return set(genre.lower() for genre in genres.get("genres"))
    raise ValueError(f"No genres found in {path}")

def getPathToGenresFile(filename):
    #When have fun and energy, this could be refactored...
    cwd = os.getcwd()
    head = cwd.split(GIT_REPO_NAME)
    if len(head) < 1:
        raise NameError("Cannot get the working Path. Look at Source Code and Debug. :/")
    return os.path.join(head[0], GIT_REPO_NAME, DATA_FOLDER, GENRES_FOLDER, filename)

def loadJson(path):
    if not os.path.isfile(path):
        raise ValueError(f"{path} is not existente.")
    with open(path, "r", encoding="UTF-8") as file:
        returnFile = json.loads(file.read())
    return returnFile

if __name__ == "__main__":
    main()