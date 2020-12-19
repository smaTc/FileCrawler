import sys,os,shutil,traceback
from pathlib import Path

def getFilesInPath(path,pattern,wantString):
    #return list(Path(".").rglob("*.[tT][xX][tT]"))
    posixPaths = list(Path(path).rglob(pattern))
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

print("FileCrawler")
# Default Values
newDir = "CrawledFiles"

# Check args
paths = sys.argv[1:]
if len(paths) < 2 or len(paths) > 3:
    print("Not enough (at least 2) or too many (more than 3) arguments")
    sys.exit()
elif paths[0] == "" or paths[1] == "":
    print("source path or filetype cannot be empty")
    sys.exit()
elif len(paths) == 3:
    newDir = paths[2]

# Extend paths
paths[0] = extendToFullPath(paths[0])

# Get directory names
fileDirSplitList = paths[0].split("/")
fileDir = fileDirSplitList[len(fileDirSplitList)-1]

if os.path.isdir(newDir):
    shutil.rmtree(newDir)

os.mkdir(newDir)
copyTree = getFilesInPath(paths[0],paths[1],False)

print("Copying Files:")
for c in copyTree:
    try:
        nameArr = str(c).split("/")
        name = nameArr[len(nameArr)-1]
        shutil.copy(str(c),newDir+"/"+name)
        print(name)
    except:
        traceback.print_exc()

print("done")