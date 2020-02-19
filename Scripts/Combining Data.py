import sys
import os
import json
from datetime import datetime
from UtilityScripts import *
from INPUTS import workingDirectory, compiledProjectFolder, normalizedFileFolder

jsonOutHumanReadable = True

compiledProjectPath = os.path.join(workingDirectory, compiledProjectFolder)
print(createDirectoryIfDoesntExist(compiledProjectPath))

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

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
compiledJsonFileName = timestamp + "compiledBuildingData" + ".json"
compiledJsonFilePath = os.path.join(compiledProjectPath,compiledJsonFileName)
with open(compiledJsonFilePath, 'w') as jsonFile:
    if jsonOutHumanReadable:
        json.dump(compiledJsons, jsonFile, indent=2)
    else:
        json.dump(compiledJsons, jsonFile)
