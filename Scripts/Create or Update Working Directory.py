import sys
import os
"xlsx writer will need to be installed with pip"
import xlsxwriter
import shutil
import json
from UtilityScripts import *
from INPUTS import inputDirectory,workingDirectory,normalizedFileFolder,normalizeDepartmentKey

inputDirectory = os.path.normpath(inputDirectory)
workingDirectory = os.path.normpath(workingDirectory)

normalizedFileDirectory = os.path.join(workingDirectory,normalizedFileFolder)
normalizedDirText = createDirectoryIfDoesntExist(normalizedFileDirectory)
logger(["input directory...",inputDirectory,"working directory...",workingDirectory,normalizedDirText,normalizedFileDirectory])

buildingJsonNames = []
filesInInputDirectory = os.listdir(inputDirectory)
for fileName in filesInInputDirectory:
    if ".json" in fileName and "_log" not in fileName:
        buildingJsonNames.append(fileName)


def addParamsAndWriteToDirectory(_existingFilePath,_newFilePath):
    with open(_existingFilePath) as originalJson:
        data = json.load(originalJson)
        for room in data["Room Data"]:
            room["normalized department"] = room["department"]
        with open(_newFilePath, 'w') as newJson:
            json.dump(data, newJson, indent=2)

filesInNormDirectory = os.listdir(normalizedFileDirectory)
addedToNormDirectory = []
if filesInNormDirectory:
    for newFileName in buildingJsonNames:
        unpaired = True
        for existingFileName in filesInNormDirectory:
            if newFileName == existingFileName:
                unpaired = False
                break
        if unpaired:
            existingFilePath = os.path.join(inputDirectory,newFileName)
            newFilePath = os.path.join(normalizedFileDirectory,newFileName)
            addedToNormDirectory.append(newFilePath)
            addParamsAndWriteToDirectory(existingFilePath,newFilePath)
else:
    for fileName in buildingJsonNames:
        existingFilePath = os.path.join(inputDirectory,fileName)
        newFilePath = os.path.join(normalizedFileDirectory,fileName)
        addedToNormDirectory.append(newFilePath)
        addParamsAndWriteToDirectory(existingFilePath,newFilePath)

if addedToNormDirectory:
    print('')
    print("the following items were added to the normalized data folder in the working directory")
    logger(addedToNormDirectory)

normKeyName = os.path.join(workingDirectory,normalizeDepartmentKey+".xlsx")

if not os.path.exists(normKeyName):
    normKeyWorkbook = xlsxwriter.Workbook(normKeyName)
    normLogSheet = normKeyWorkbook.add_worksheet("normalization log")
    newNormKeySheet = normKeyWorkbook.add_worksheet("current normalization key")
    normKeyWorkbook.close()
    logger(["created a new excel file to use when tracking the department normalization process","the file name is...",normKeyName])