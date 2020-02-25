"""
_____INPUTS FILE_____
This file exists as the centralized inputs file for all python scripts in this directory

Ideally the only inputs a user will need to manage are those in the directories section, but if folder / file naming conventions are desired these can be adjusted as well

Once a set of runs have begun it is advised not to adjust parameters as these could have unanticipated consequences

__Dependencies__
XlsxWriter
pandas
xlrd
"""

##############################################################################################################################################################

"""
_____DIRECTORIES_____
These are the directory paths that will be used in the analysis

The inputDirectory is the file directory containing all the json files exported from Revit with the Dynamo data mining script

The workingDirectory is the file directory that will be used to contain the data files used when normalizing the departments and compiling the project data
This can be the same directory as the inputDirectory or a different one
The selected folder will have numerous folders and files added to it, so for purposes of clarity it should be set aside for running these scripts as it's primary purpose

**note the triple backslash in the file path names given as an example.  This is important because of how Python treats these characters**
"""
inputDirectory = "\\\cga\Data\General\Dept\KnowledgeMgmt\ReCouncil\\03_Project Folders\Programming_Data_Management\Data_Mining\High School Data\Data From Projects"
workingDirectory = "\\\cga\Data\General\Dept\KnowledgeMgmt\ReCouncil\\03_Project Folders\Programming_Data_Management\Data_Mining\High School Data"

##############################################################################################################################################################

"""
_____FOLDER NAMES_____
The names of folders where files will be saved within the working directory

The normalizedFileFolder is where data that has extra parameters for the normalization process will be saved and resaved as the "Create or Update Working Directory.py" script is run.  This script will not overwrite existing data in the directory, but will add new files with the normalization parameters if they cannot be found in the directory

The compiledProjectFolder is where time / date stamped compiled data will be saved when the "Combining Data.py" script is run.  This script will not delete older data, but a user will likely want to manually manage this to avoid a build up over files.
"""
normalizedFileFolder = "NormalizedData"
compiledProjectFolder = "CompiledData"

##############################################################################################################################################################

"""
_____FILE NAMES_____
The names of the supplementary files that will be generated and used as an ongoing resource for these scripts

The normalizedDepartmentKey will be an excel file with two sheets
one sheet will function as a key for generating new normalized department parameters based on the original parameters
another sheet will function as a log for all keys that have been used to generate normalized parameters
(a long term future for these files could be to guide a ML algorithm and automate this process, but this would likely require substantial amounts of data... so please save them)
"""
normalizeDepartmentKey = "NormalizeDeptsKey"
normalizationLogSheetName = "normalization log"
normalizationKeySheetName = "current normalization key"

##############################################################################################################################################################
