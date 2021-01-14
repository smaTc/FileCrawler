import sys,os,shutil,traceback
from pathlib import Path

def getFilesInPath(path,pattern,wantString):
    #posixPaths = list(Path(path).rglob(pattern))
    posixPaths = list()
    for p in pattern:
        posixPaths.extend(list(Path(path).rglob(p)))

    if wantString:
        pathStrings = []
        for p in posixPaths:
            pathStrings.append(str(p.resolve()))
        return pathStrings
    else:
        return posixPaths

def extendToFullPath(path):
    currPath = os.getcwd()
    os.chdir(path)
    newPath = os.getcwd()
    os.chdir(currPath)
    return newPath

def helpMessage(err=""):
    if err != "":
        print(err)
    else:
        print("\nFileCrawler can be executed with: ")
    print("(python) FileCrawler(.py)")
    print("(python) FileCrawler(.py) -p PATH -t TYPE -o OUTPUT  -> omit python and .py if executable")
    print("Example: python FileCrawler.py -p ~/Documents -t pdf -o Docs")
    print("Note: -p, -t and -o are optional. Default values are: -p -> ./; -t pdf,epub,azw3 (comma separated); -o  \"CrawledFiles\"")
    

# Default Values
newDir = "CrawledFiles"
path = "./"
fileType = ["pdf","epub","azw3"]

print("Running FileCrawler Script\n")
args = sys.argv[1:]

i = 0
while i < len(args):
    if args[i] == "-p" or args[i] == "-path":
        path = args[i+1]
    elif args[i] == "-t" or args[i] == "-type":
        fileType = args[i+1].replace(" ", "").split(",")
    elif args[i] == "-o" or args[i] == "-out":
        newDir = args[i+1]
    
    i += 1

i = 0
while i < len(fileType):
    fileType[i] = "*." + fileType[i]
    i += 1
    
if path is None or fileType is None:
    #print()
    helpMessage("Path or fileType argument missing. Please execute the script as follows:")
    sys.exit()
    

# Extend paths
path = extendToFullPath(path)

# Get directory names
fileDirSplitList = path.split("/")
fileDir = fileDirSplitList[len(fileDirSplitList)-1]

if os.path.isdir(newDir):
    shutil.rmtree(newDir)

os.mkdir(newDir)
copyTree = getFilesInPath(path,fileType,False)

"""
copyTree = []
for f in fileType:
    print(f)
    copyTree.append(getFilesInPath(path,f,False))
"""

print("Copying Files:")
copied = 0
failed = 0
for c in copyTree:
    try:
        nameArr = str(c).split("/")
        name = nameArr[len(nameArr)-1]
        shutil.copy(str(c),newDir+"/"+name)
        print(name)
        copied += 1
    except:
        traceback.print_exc()
        copied -= 1
        failed += 1

print("Done")
print("Copied: " + str(copied))
if failed > 0:
    print("Failed: " + str(failed))
