import os
import xlsxwriter

"""
Finds the unique values in a list
"""
def uniqueValues(_listOfValues):
    _valuesOut = []
    _valuesOut.append(_listOfValues.pop(0))
    
    for value in _listOfValues:
        isUnique = True
        
        for uniqueValue in _valuesOut:
            if value == uniqueValue:
                isUnique = False
                break

        if isUnique:
            _valuesOut.append(value)
            
    _valuesOut.sort()        
    return _valuesOut


"""
Finds all the unique values in a list, and returns a list of these values and a list of the number of their occurences
"""
def uniqueValuesAndCounts(_listOfValues,_valueKey,_countKey):
    _listsOut = []
    _valuesOut = []
    _countsOfValues = []
    _valuesOut.append(_listOfValues.pop(0))
    _countsOfValues.append(1)

    for i,value in enumerate(_listOfValues):
        isUnique = True
        
        for j,uniqueValue in enumerate(_valuesOut):
            if value == uniqueValue:
                isUnique = False
                uniqueIndex = j
                break

        if isUnique:
            _valuesOut.append(value)
            _countsOfValues.append(1)
        else:
            _countsOfValues[uniqueIndex] += 1
            
    for i,uniqueVal in enumerate(_valuesOut):
        rowObj = {}
        itemCount = _countsOfValues[i]
        rowObj[_countKey] = int(itemCount)
        rowObj[_valueKey] = uniqueVal
        _listsOut.append(rowObj)

    _sortedListOut = sorted(_listsOut, key=lambda i: (i[_countKey], i[_valueKey]), reverse=True)
    return _sortedListOut


"""
Creates a human readable print output for a single item or list of items
"""
def logger(_listOfItemsToPrint):
    print()
    print("-------------------------------------------------------------------------------------")
    for item in _listOfItemsToPrint:
        print(item)
        print("-------------------------------------------------------------------------------------")
    print()
    print("/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")


"""
Checks if a directory exists and if it does not, it creates it
It returns a string for printing purposes that will inform the user if the directory did or did not exist
THIS SCRIPT REQUIRES THE OS LIBRARY TO BE LOADED
"""
def createDirectoryIfDoesntExist(_path):
    if os.path.isdir(_path):
        textOut = "the path " + str(_path) + " already exists"
    else:
        textOut = "a directory has been created at " + str(_path)
        os.mkdir(_path)
    return textOut

"""
This function is used with the xlsx writer package to write a list of dictionaries to a given sheet of a workbook
Each dictionary represents a row of the excel file, and the keys represent the headers
This function will not work properly if the dictionaries do not have identical keys
"""
def writeDictToExcelSheet(_listOfDicts,_listOfKeys,_sheet):
    for i,_key in enumerate(_listOfKeys):
        _sheet.write(0,i,_key)
    for i,_rowDict in enumerate(_listOfDicts):
        for j,_key in enumerate(_listOfKeys):
            for _itemKey in _rowDict:
                if _itemKey == _key:
                    _sheet.write(i+1,j,_rowDict[_key])
            

