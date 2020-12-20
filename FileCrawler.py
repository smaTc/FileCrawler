import sys,os,shutil,traceback
from pathlib import Path

def getFilesInPath(path,pattern,wantString):
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

# Default Values
newDir = "CrawledFiles"
path = None
fileType = None

print("Running FileCrawler Script\n")
args = sys.argv[1:]

i = 0
while i < len(args):
    if args[i] == "-p" or args[i] == "-path":
        path = args[i+1]
    elif args[i] == "-t" or args[i] == "-type":
        fileType = "*." + args[i+1]
    elif args[i] == "-o" or args[i] == "-out":
        newDir = args[i+1]
    
    i += 1

if path is None or fileType is None:
    print("Path or fileType argument missing. Please execute the script as follows:")
    print("python FileCrawler.py -p PATH -t TYPE -o OUTPUT")
    print("Example: python FileCrawler.py -p ~/Documents -t pdf -o Docs")
    print("Note: -o is optional. Default directory is \"CrawledFiles\"")
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