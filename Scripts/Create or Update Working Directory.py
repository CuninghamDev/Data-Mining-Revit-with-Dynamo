import sys
import os
"xlsx writer will need to be installed with pip"
import xlsxwriter
import shutil
import json
from UtilityScripts import *

#########################################################################################################
#########################################    USER INPUTS    #############################################
#########################################################################################################
#########################################################################################################
#########################################################################################################
#########################################################################################################
"ideally only the only inputs a user will need to change are the directories listed below."
"in some cases a user may find they need to change additional directory information (such as folder names), but hopefully this would be relatively rare"

"the input directory is the file directory containing all the json files exported from Revit with the Dynamo data mining script"
inputDirectory = "\\\cga\Data\General\Dept\BIM\Dynamo\Mining Program Data\Data\Campus4\RawData"

"the directory that will be used to contain all normalized project data.  This can be the same directory as the input, or can be totally different."
"several folders will be created in the working directory, so it should be flexible enough to have a lot of new data added to it."
workingDirectory1 = "\\\cga\Data\General\Dept\BIM\Dynamo\Mining Program Data\Data\Campus4"
workingDirectory2 = "\\\cga\Data\General\Dept\BIM\Dynamo\Mining Program Data\Data\TestNormalizationFolder"

"the name of the folder in the working directory which will contain the normalized data"
normalizedFileFolder = "NormalizedData"

"the name of the excel file that will act as a key for normalizing department data"
normalizeDepartmentKey = "NormalizeDeptsKey"
#########################################################################################################
#########################################################################################################
#########################################################################################################
#########################################################################################################
#########################################################################################################
#########################################################################################################
#########################################################################################################
#########################################################################################################
#########################################################################################################

inputDirectory = os.path.normpath(inputDirectory)
workingDirectory = os.path.normpath(workingDirectory1)

normalizedFileDirectory = os.path.join(workingDirectory,normalizedFileFolder)

if os.path.isdir(normalizedFileDirectory):
    normalizedDirText = "the specified directory for normalized data already exists at..."
else:
    normalizedDirText = "the specified directory for normalized data did not exist, but has been created at..."
    os.mkdir(normalizedFileDirectory)

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