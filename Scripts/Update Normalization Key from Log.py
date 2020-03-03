import sys
import os
import json
import xlsxwriter
import pandas as pd
from datetime import date
from UtilityScripts import *
from INPUTS import workingDirectory, compiledProjectFolder, normalizedFileFolder, normalizeDepartmentKey, normalizationLogSheetName, normalizationKeySheetName

def getAllDepartments(_jsonFilePath,_listOfAllDepartments):
    with open(_jsonFilePath) as jsonFile:
        data = json.load(jsonFile)
        for room in data["Room Data"]:
            _listOfAllDepartments.append(room["department"])
    return _listOfAllDepartments

normalizedFilesFolder = os.path.join(workingDirectory, normalizedFileFolder)
filesInNormalizedFolder = os.listdir(normalizedFilesFolder)

allDepartments = []
normalizedJsonDirectory = os.listdir(os.path.join(workingDirectory,normalizedFileFolder))
for fileName in normalizedJsonDirectory:
    jsonFilePath = os.path.join(workingDirectory,normalizedFileFolder,fileName)
    allDepartments = getAllDepartments(jsonFilePath,allDepartments)

excelFilePath = os.path.join(workingDirectory,normalizeDepartmentKey+".xlsx")
normLogDataFrame = pd.read_excel(io=excelFilePath, sheet_name=normalizationLogSheetName)
normLogKeys = list(normLogDataFrame.to_dict().keys())
normLogDict = normLogDataFrame.to_dict('records')

if normLogDict:
    normLogExists = True
    if len(normLogKeys) == 2:
        originalLogs = True
    elif len(normLogKeys) > 2:
        originalLogs = False
else:
    normLogExists = False

if not normLogExists:
    #create the basic logs
    uniqueDepartments = uniqueValuesAndCounts(allDepartments,"Departments","Room Count")
    uniqueDepartmentsDf = pd.DataFrame(data=uniqueDepartments)
    print("normalization log doesn't exist")
    print(uniqueDepartmentsDf)

else:
    if originalLogs:
        uniqueDepartments = uniqueValuesAndCounts(allDepartments,"Departments","Room Count")
        uniqueDepartmentsDf = pd.DataFrame(data=uniqueDepartments)
        print("normalization log exists, but no changes have been made")
        print(uniqueDepartmentsDf)

    else:
        #go through each row of the logs, create a new key based on the last column of data
        compiledJsons = {}
        for jsonFileName in filesInNormalizedFolder:
            jsonFilePath = os.path.join(normalizedFilesFolder,jsonFileName)
            projectName = jsonFileName.split(".")[0]
            with open(jsonFilePath) as jsonFile:
                data = json.load(jsonFile)       
                compiledJsons[projectName] = data

        allDepartments = []
        unmatchedDepartments = []
        allMatched = True
        for project in compiledJsons:
            projectData = compiledJsons[project]
            for room in projectData["Room Data"]:
                matched = False
                origDept = room["department"]
                if origDept == '':
                    origDept = " "
                for logRow in normLogDict:
                    loggedOrigDept = logRow[normLogKeys[1]]
                    if origDept == loggedOrigDept:
                        matched = True
                        room["normalized department"] = logRow[normLogKeys[-1]]
                        allDepartments.append(room["normalized department"])
                        break
                if not matched:
                    allMatched = False
                    unmatchedDepartments.append(origDept)

            jsonFileName = project + ".json"
            projectJsonFilePath = os.path.join(normalizedFilesFolder,jsonFileName)
            with open(projectJsonFilePath,'w') as jsonFile:
                json.dump(projectData, jsonFile, indent=2)

    uniqueDepartments = uniqueValuesAndCounts(allDepartments,"Departments","Room Count")
    uniqueDepartmentsDf = pd.DataFrame(data=uniqueDepartments)
    print("a normalization log was found, and the last entry in this log was used to construct a key and update the rooms in the normalized JSONS")
    print(uniqueDepartmentsDf)

normKeyName = os.path.join(workingDirectory,normalizeDepartmentKey+".xlsx")
normKeyWorkbook = xlsxwriter.Workbook(normKeyName)

newNormKeySheet = normKeyWorkbook.add_worksheet(normalizationKeySheetName)
s = newNormKeySheet
writeDictToExcelSheet(uniqueDepartments,["Room Count","Departments","Departments"],s)
s.write(0,2,"New Departments")

normLogSheet = normKeyWorkbook.add_worksheet(normalizationLogSheetName)
s = normLogSheet
if normLogExists and allMatched:
    writeDictToExcelSheet(normLogDict,normLogKeys,s)
elif normLogExists and not allMatched:
    print("departments were found that did not fit any original department name in the normalization log")
    origDeptKey = normLogKeys[1]
    origDeptCountKey = normLogKeys[0]
    normRunKey = normLogKeys[-1]
    uniqueNewDepts = uniqueValuesAndCounts(unmatchedDepartments,origDeptKey,origDeptCountKey)
    # print(uniqueNewDepts)
    for obj in uniqueNewDepts:
        newLogEntry = {}
        for key in normLogKeys:
            if key == origDeptKey:
                newLogEntry[origDeptKey] = obj[origDeptKey]
            elif key == origDeptCountKey:
                newLogEntry[origDeptCountKey] = obj[origDeptCountKey]
            elif key == normRunKey:
                newLogEntry[normRunKey] = obj[origDeptKey]
            else:
                newLogEntry[key] = ''
        normLogDict.append(newLogEntry)
    writeDictToExcelSheet(normLogDict,normLogKeys,s)

else:
    writeDictToExcelSheet(uniqueDepartments,["Room Count","Departments"],s)

normKeyWorkbook.close()


