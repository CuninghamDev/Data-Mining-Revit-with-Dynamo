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

        if isUnique:
            _valuesOut.append(value)
            
    _valuesOut.sort()        
    return _valuesOut


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

