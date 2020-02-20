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
normLogKeys = normLogDataFrame.to_dict().keys()
normLogDict = normLogDataFrame.to_dict('records')

print(normLogKeys)
print(normLogDict)

normKeyDataFrame = pd.read_excel(io=excelFilePath, sheet_name=normalizationKeySheetName)
normKeyKeys = normKeyDataFrame.to_dict().keys()
normKeyDict = normKeyDataFrame.to_dict('records')

print(normKeyKeys)
print(normKeyDict)
