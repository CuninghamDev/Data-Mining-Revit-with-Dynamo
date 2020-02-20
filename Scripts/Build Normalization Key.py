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

excelFilePath = os.path.join(workingDirectory,normalizeDepartmentKey+".xlsx")
normLogDataFrame = pd.read_excel(io=excelFilePath, sheet_name=normalizationLogSheetName)
normLogKeys = list(normLogDataFrame.to_dict().keys())
normLogDict = normLogDataFrame.to_dict('records')

if normLogDict:
    normLogExists = True
else:
    normLogExists = False

uniqueDepartments = uniqueValuesAndCounts(allDepartments,"Departments","Room Count")
uniqueDepartmentsDf = pd.DataFrame(data=uniqueDepartments)

normKeyName = os.path.join(workingDirectory,normalizeDepartmentKey+".xlsx")
normKeyWorkbook = xlsxwriter.Workbook(normKeyName)

newNormKeySheet = normKeyWorkbook.add_worksheet(normalizationKeySheetName)
s = newNormKeySheet
writeDictToExcelSheet(uniqueDepartments,["Room Count","Departments","Departments"],s)
s.write(0,2,"New Departments")

normLogSheet = normKeyWorkbook.add_worksheet(normalizationLogSheetName)
s = normLogSheet
if normLogExists:
    writeDictToExcelSheet(normLogDict,normLogKeys,s)
else:
    writeDictToExcelSheet(uniqueDepartments,["Room Count","Departments"],s)

normKeyWorkbook.close()


