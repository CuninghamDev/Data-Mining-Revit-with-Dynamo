import sys
import os
import json
import csv
from datetime import datetime
from UtilityScripts import *
from INPUTS import workingDirectory, compiledProjectFolder, normalizedFileFolder

jsonOutHumanReadable = True
exportJson = True
exportCsv = True
compiledFileName = "compiledBuildingData"

compiledProjectPath = os.path.join(workingDirectory, compiledProjectFolder)
print(createDirectoryIfDoesntExist(compiledProjectPath))
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")

normalizedFilesFolder = os.path.join(workingDirectory, normalizedFileFolder)
filesInNormalizedFolder = os.listdir(normalizedFilesFolder)
print(filesInNormalizedFolder)

compiledJsons = {}
for jsonFileName in filesInNormalizedFolder:
    jsonFilePath = os.path.join(normalizedFilesFolder,jsonFileName)
    projectName = jsonFileName.split(".")[0]
    with open(jsonFilePath) as jsonFile:
        data = json.load(jsonFile)       
        compiledJsons[projectName] = data

if exportJson:
    compiledJsonFileName = timestamp + compiledFileName + ".json"
    compiledJsonFilePath = os.path.join(compiledProjectPath,compiledJsonFileName)
    with open(compiledJsonFilePath, 'w') as jsonFile:
        if jsonOutHumanReadable:
            json.dump(compiledJsons, jsonFile, indent=2)
        else:
            json.dump(compiledJsons, jsonFile)

if exportCsv:
    buildingsToCsv = []
    for building in compiledJsons:
        buildingData = compiledJsons[building]
        for room in buildingData["Room Data"]:
            roomObj = {}
            roomObj["building"] = building
            roomObj["from analysis"] = buildingData["Analysis Name"]
            for roomProperty in room:
                roomPropData = room[roomProperty]
                if type(roomPropData) != list and type(roomPropData) != bool:
                    roomObj[roomProperty] = roomPropData
            buildingsToCsv.append(roomObj)

    compiledCsvFileName = timestamp + compiledFileName + ".csv"
    compiledCsvFilePath = os.path.join(compiledProjectPath,compiledCsvFileName)

    csvHeaders = list(buildingsToCsv[0].keys())
    with open(compiledCsvFilePath, 'w') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames = csvHeaders, delimiter = ',', lineterminator = '\n')
        writer.writeheader()
        for row in buildingsToCsv:
            writer.writerow(row)
    
