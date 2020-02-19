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
            _listOfAllDepartments.append(room["normalized department"])
    return _listOfAllDepartments

allDepartments = []
normalizedJsonDirectory = os.listdir(os.path.join(workingDirectory,normalizedFileFolder))
for fileName in normalizedJsonDirectory:
    jsonFilePath = os.path.join(workingDirectory,normalizedFileFolder,fileName)
    allDepartments = getAllDepartments(jsonFilePath,allDepartments)

uniqueDepartments = uniqueValuesAndCounts(allDepartments)
uniqueDepartmentsDf = pd.DataFrame(data=uniqueDepartments)


excelFilePath = os.path.join(workingDirectory,normalizeDepartmentKey+".xlsx")

normLogDataFrame = pd.read_excel(io=excelFilePath, sheet_name=normalizationLogSheetName)
normLogDict = normLogDataFrame.to_dict()


normKeyName = os.path.join(workingDirectory,normalizeDepartmentKey+".xlsx")
normKeyWorkbook = xlsxwriter.Workbook(normKeyName)
normLogSheet = normKeyWorkbook.add_worksheet(normalizationLogSheetName)


newNormKeySheet = normKeyWorkbook.add_worksheet(normalizationKeySheetName)
row = 0
col = 0
s = newNormKeySheet
s.write(row,col,"Departments")
s.write(row,col+1,"Count of Occurences")
for i,rowDict in enumerate(uniqueDepartments):
    for j,rowKey in enumerate(rowDict):
        dataItem = rowDict[rowKey]
        s.write(i+1,j,dataItem)

normKeyWorkbook.close()
# print(normLogDict)

