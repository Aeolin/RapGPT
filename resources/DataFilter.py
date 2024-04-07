import os
import json

GIT_REPO_NAME = "RapGPT"
DATA_FOLDER = "resources"

def main():
    filterSongBatch(None, "song_batch_0.json")

def filterSongBatch(tags, filename):
    #get path
    path = getPathToFile(filename)
    #load file
    data = loadJson(path)
    print(data[0]["LastFMTags"])
    print(getPathToFile(filename))
    #filter by tag
    #save file

def getPathToFile(filename):
    cwd = os.getcwd()
    head = cwd.split(GIT_REPO_NAME)
    if len(head) < 1:
        raise NameError("Cannot get the working Path. Look at Source Code and Debug. :/")
    return os.path.join(head[0], GIT_REPO_NAME, DATA_FOLDER, filename)

def loadJson(path):
    if not os.path.isfile(path):
        raise ValueError(f"{path} is not existente.")
    with open(path, "r", encoding="UTF-8") as file:
        returnFile = json.loads(file.read())
    return returnFile

if __name__ == "__main__":
    main()