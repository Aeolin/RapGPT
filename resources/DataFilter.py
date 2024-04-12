import os
import json
import random
import pandas as pd

GIT_REPO_NAME = "RapGPT"
DATA_FOLDER = "resources"
GENRES_FOLDER = "genres"
NO_GENRE = "NULL"
MANY_GENRES = "MANY"

noMatchesTags = []

def main():
    filterSongBatch(None, "song_batch_3.json")

def filterSongBatch(tags, filename, genresFileName="expandedChatGPT.json"):
    path = getPathToFile(filename)
    genres = getGenres(genresFileName)
    data = loadJson(path)
    textGenresPair = [generateTextGenrePair(dataPoint, genres) for dataPoint in data]
    saveJson()

def saveJson():
    pass

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