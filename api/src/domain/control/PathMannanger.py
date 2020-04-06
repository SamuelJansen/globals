import os, sys
from pathlib import Path
clear = lambda: os.system('cls')
clear() # or simply os.system('cls')
# from domain.control import PathMannanger

print('PathMannanger library imported')

class PathMannanger:

    BASE_API_PATH = 'api\\src\\'
    LOCAL_GLOBALS_API_PATH = 'domain\\control\\'

    EXTENSION = 'ht'
    PYTHON_EXTENSION = 'py'

    ENCODING = 'utf-8'
    OVERRIDE = 'w+'
    READ = 'r'

    GLOBALS_NAME = 'Globals'
    API_LIST = [
        GLOBALS_NAME,
        'Application'
    ]

    CHARACTERE_FILTER = [
        '__'
    ]

    NODE_IGNORE_LIST = [
        '.git',
        '__pycache__',
        '__init__',
        '__main__'
    ]

    ### There are 'places' where backslash is not much wellcome
    ### Having it stored into a variable helps a lot
    BACK_SLASH = '\\'

    WRONG_WAY_TO_MAKE_IT_WORKS = 'WRONG_WAY_TO_MAKE_IT_WORKS'
    PROPER_WAY_TO_MAKE_IT_WORKS = 'PROPER_WAY_TO_MAKE_IT_WORKS'

    def __init__(self,
        mode = PROPER_WAY_TO_MAKE_IT_WORKS,
        encoding = ENCODING,
        printStatus = False
    ):

        self.mode = mode
        self.backSlash = PathMannanger.BACK_SLASH

        self.charactereFilterList = PathMannanger.CHARACTERE_FILTER
        self.nodeIgnoreList = PathMannanger.NODE_IGNORE_LIST
        self.configurationFileExtension = PathMannanger.EXTENSION

        self.currentPath = f'{str(Path(__file__).parent.absolute())}{self.backSlash}'
        self.localPath = f'{str(Path.home())}{self.backSlash}'

        if encoding :
            self.encoding = encoding
        else :
            self.encoding = PathMannanger.ENCODING

        self.backSlash = PathMannanger.BACK_SLASH
        self.printStatus = printStatus

        if self.mode == PathMannanger.PROPER_WAY_TO_MAKE_IT_WORKS :
            self.baseApiPath = PathMannanger.BASE_API_PATH
            self.apiPath = self.currentPath.split(self.baseApiPath)[0]
            self.apiName = self.apiPath.split(self.backSlash)[-2]
            self.apisRoot = self.currentPath.split(self.localPath)[1].split(self.apiName)[0]
            self.apiNames = PathMannanger.API_LIST

            self.globalsApiName = PathMannanger.GLOBALS_NAME
            self.localGlobalsApiFilePath = f'{PathMannanger.LOCAL_GLOBALS_API_PATH}{PathMannanger.__name__}.{PathMannanger.PYTHON_EXTENSION}'
            self.globalsApiPath = f'{self.getApiPath(self.globalsApiName)}{self.localGlobalsApiFilePath}'
            self.apisPath = f'{self.backSlash.join(self.currentPath.split(self.localGlobalsApiFilePath)[-2].split(self.backSlash)[:-2])}{self.backSlash}'

            if self.printStatus :
                print(f'''                PathMannanger = {self}
                PathMannanger.currentPath =                 {self.currentPath}
                PathMannanger.localPath =                   {self.localPath}
                PathMannanger.baseApiPath =                 {self.baseApiPath}
                PathMannanger.apiPath =                     {self.apiPath}
                PathMannanger.apiName =                     {self.apiName}
                PathMannanger.apisRoot =                    {self.apisRoot}
                PathMannanger.apiNames =                    {self.apiNames}
                PathMannanger.localGlobalsApiFilePath =     {self.localGlobalsApiFilePath}
                PathMannanger.globalsApiName =              {self.globalsApiName}
                PathMannanger.globalsApiPath =              {self.globalsApiPath}
                PathMannanger.apisPath =                    {self.apisPath}\n''')

            self.update()

        elif self.mode == PathMannanger.WRONG_WAY_TO_MAKE_IT_WORKS :
            self.localGlobalsApiFilePath = f'{PathMannanger.BASE_API_PATH}{PathMannanger.LOCAL_GLOBALS_API_PATH}'
            self.baseApiPath = f'{self.backSlash.join(self.currentPath.split(self.localGlobalsApiFilePath)[-2].split(self.backSlash)[:-1])}{self.backSlash}'
            self.apisPath = f'{self.backSlash.join(self.currentPath.split(self.localGlobalsApiFilePath)[-2].split(self.backSlash)[:-2])}{self.backSlash}'

            self.modulesNodeTree = self.getPathTreeFromPath(self.apisPath)
            self.makePathTreeVisible(self.apisPath)

            if self.printStatus :
                print(f'''                PathMannanger = {self}
                PathMannanger.currentPath =                 {self.currentPath}
                PathMannanger.localPath =                   {self.localPath}
                PathMannanger.baseApiPath =                 {self.baseApiPath}
                PathMannanger.localGlobalsApiFilePath =     {self.localGlobalsApiFilePath}
                PathMannanger.apisPath =                    {self.apisPath}\n''')
                print(f'{self.modulesNodeTree}\n')

    def getApiPath(self,apiName):
        return f'{self.localPath}{self.apisRoot}{apiName}{self.backSlash}{self.baseApiPath}'

    def update(self) :
        pathMannangerScript = []
        with open(self.globalsApiPath,PathMannanger.READ,encoding = PathMannanger.ENCODING) as pathMannangerFile :
            for line in pathMannangerFile :
                pathMannangerScript.append(line)

        for apiName in self.apiNames :
            updatingApiPath =f'{self.getApiPath(apiName)}{self.localGlobalsApiFilePath}'
            if apiName != self.globalsApiName :
                with open(updatingApiPath,PathMannanger.OVERRIDE,encoding = PathMannanger.ENCODING) as pathMannangerFile :
                    pathMannangerFile.write(''.join(pathMannangerScript))
        self.makeApisAvaliable()

    def makeApisAvaliable(self) :
        self.modulesNodeTree = []
        for apiName in PathMannanger.API_LIST :
            self.modulesNodeTree.append(self.makePathTreeVisible(self.getApiPath(apiName)))
        if self.printStatus :
            print(f'PathMannanger.modulesNodeTree = {self.modulesNodeTree}\n')

    def makePathTreeVisible(self,path):
        node = {}
        nodeSons = os.listdir(path)
        for nodeSon in nodeSons :
            if self.nodeIsValid(nodeSon) :
                nodeSonPath = f'{path}{self.backSlash}{nodeSon}'
                try :
                    node[nodeSon] = self.makePathTreeVisible(nodeSonPath)
                except : pass
        sys.path.append(path)
        return node

    def nodeIsValid(self,node):
        return self.nodeIsValidByFilter(node) and (node not in self.nodeIgnoreList)

    def nodeIsValidByFilter(self,node):
        for charactere in self.charactereFilterList :
            if not len(node.split()) == 1 :
                return False
        return True

    def getPathTreeFromPath(self,path):
        node = {}
        nodeSons = os.listdir(path)
        for nodeSon in nodeSons :
            if self.nodeIsValid(nodeSon) :
                nodeSonPath = f'{path}{self.backSlash}{nodeSon}'
                try :
                    node[nodeSon] = self.getPathTreeFromPath(nodeSonPath)
                except : pass
        return node
