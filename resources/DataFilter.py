import os
import json
import random
import pandas as pd

GIT_REPO_NAME = "RapGPT"
DATA_FOLDER = "resources"
GENRES_FOLDER = "genres"

noMatchesTags = []

def main():
    filterSongBatch(None, "song_batch_3.json")

def filterSongBatch(tags, filename, genresFileName="expandedChatGPT.json"):
    #get path
    path = getPathToFile(filename)
    genres = getGenres(genresFileName)
    #load file
    data = loadJson(path)

    noMatches = 0
    oneMatch = 0
    manyMatches = 0
    for dataPoint in data:
        textGenrePair = generateTextGenrePair(dataPoint, genres)
        if textGenrePair["Genres"] == "Null":
            noMatches += 1
        elif textGenrePair["Genres"] == "Many":
            manyMatches += 1
        else:
            oneMatch += 1
    print(f"One Matches: {oneMatch}: {100* float(oneMatch) / len(data)}%")
    print(f"No Matches: {noMatches}: {100* float(noMatches) / len(data)}%")
    print(f"Many Matches: {manyMatches}: {100* float(manyMatches) / len(data)}%")
    #countOthers()

def countOthers():
    df = pd.DataFrame({"Tag": noMatchesTags})
    print(df.value_counts())


def generateTextGenrePair(dataPoint, genres: set, selectAtRandom = True):
    #validate dataPoint?
    #intersect
    intersection = genres.intersection(dataPoint["LastFMTags"])
    #if intersect, return text + genre
    if len(intersection) < 1:
        for tag in dataPoint["LastFMTags"]:
            noMatchesTags.append(tag.lower())
        return {"Lyrics": dataPoint["Lyrics"], "Genres": "Null"}
    if len(intersection) == 1:
        return {"Lyrics": dataPoint["Lyrics"], "Genres": list(intersection)[0]}
    if selectAtRandom:
        randomIndex = random.randint(0, len(intersection) - 1)
        return {"Lyrics": dataPoint["Lyrics"], "Genres": list(intersection)[randomIndex]}
    return {"Lyrics": dataPoint["Lyrics"], "Genres": "Many"}
    

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