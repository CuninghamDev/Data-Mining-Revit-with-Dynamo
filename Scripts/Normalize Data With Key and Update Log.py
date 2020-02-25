import sys
import os
import json
import xlsxwriter
import pandas as pd
from datetime import date
from UtilityScripts import *
from INPUTS import workingDirectory, compiledProjectFolder, normalizedFileFolder, normalizeDepartmentKey, normalizationLogSheetName, normalizationKeySheetName

excelFilePath = os.path.join(workingDirectory,normalizeDepartmentKey+".xlsx")

normLogDataFrame = pd.read_excel(io=excelFilePath, sheet_name=normalizationLogSheetName)
normLogKeys = list(normLogDataFrame.to_dict().keys())
print(normLogKeys)
normLogDict = normLogDataFrame.to_dict('records')

normKeyDataFrame = pd.read_excel(io=excelFilePath, sheet_name=normalizationKeySheetName)
normKeyKeys = list(normKeyDataFrame.to_dict().keys())
normKeyDict = normKeyDataFrame.to_dict('records')
# for row in normKeyDict:

normKey_SearchKey = normKeyKeys[1]
normKey_AddKey = normKeyKeys[2]
normLog_SearchKey = normLogKeys[-1]
normalizationRunCount = len(normLogKeys)-1
normalizationRunName = "Normalized Departments " + str(normalizationRunCount)
for i,keyRow in enumerate(normKeyDict):
    for j,logRow in enumerate(normLogDict):
        if keyRow[normKey_SearchKey] == logRow[normLog_SearchKey]:
            logRow[normalizationRunName] = keyRow[normKey_AddKey]
normLogKeys.append(normalizationRunName)

normalizedFilesFolder = os.path.join(workingDirectory, normalizedFileFolder)
filesInNormalizedFolder = os.listdir(normalizedFilesFolder)

compiledJsons = {}
for jsonFileName in filesInNormalizedFolder:
    jsonFilePath = os.path.join(normalizedFilesFolder,jsonFileName)
    projectName = jsonFileName.split(".")[0]
    with open(jsonFilePath) as jsonFile:
        data = json.load(jsonFile)       
        compiledJsons[projectName] = data

changed = False
for project in compiledJsons:
    projectData = compiledJsons[project]
    for room in projectData["Room Data"]:
        origDept = room["department"]
        for logRow in normLogDict:
            # print(logRow)
            loggedOrigDept = logRow[normLogKeys[1]]
            if origDept == loggedOrigDept:
                
                room["normalized department"] = logRow[normLogKeys[-1]]
                if logRow[normLogKeys[-1]] != logRow[normLogKeys[-2]]:
                    changed = True
                break


    jsonFileName = project + ".json"
    projectJsonFilePath = os.path.join(normalizedFilesFolder,jsonFileName)
    with open(projectJsonFilePath,'w') as jsonFile:
        json.dump(projectData, jsonFile, indent=2)

if changed:
    normKeyName = os.path.join(workingDirectory,normalizeDepartmentKey+".xlsx")
    normKeyWorkbook = xlsxwriter.Workbook(normKeyName)

    newNormKeySheet = normKeyWorkbook.add_worksheet(normalizationKeySheetName)
    normLogSheet = normKeyWorkbook.add_worksheet(normalizationLogSheetName)

    s = normLogSheet
    writeDictToExcelSheet(normLogDict,normLogKeys,s)

    normKeyWorkbook.close()
else:
    print("no changes in the normalization key were detected")