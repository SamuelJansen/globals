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
    GLOBALS = 'Globals'

    API_LIST = [
        GLOBALS,
        'Application'
    ]

    NODE_IGNORE = [
        'image',
        'audio',
        '__pycache__',
        '__init__',
        '__main__'
    ]

    BACK_SLASH = '\\' ### there ar moduler where backslash is not much wellcome

    def __init__(self):

        self.currentPath = str(Path(__file__).parent.absolute())
        self.localPath = f'{str(Path.home())}\\'

        self.baseApiPath = PathMannanger.BASE_API_PATH
        self.apiPath = self.currentPath.split(self.baseApiPath)[0]
        self.apiName = self.apiPath.split('\\')[-2]
        self.apisRoot = self.currentPath.split(self.localPath)[1].split(self.apiName)[0]
        self.apiNames = PathMannanger.API_LIST

        self.globalsApiName = PathMannanger.GLOBALS
        self.localGlobalsApiPath = f'{PathMannanger.LOCAL_GLOBALS_API_PATH}{PathMannanger.__name__}.py'
        self.globalsApiPath = f'{self.getApiPath(self.globalsApiName)}{self.localGlobalsApiPath}'

        self.backSlash = PathMannanger.BACK_SLASH

        self.update()
        ###- self.newApplicationHandler()

    def getApiPath(self,apiName):
        return f'{self.localPath}{self.apisRoot}{apiName}\\{self.baseApiPath}'

    def update(self) :
        # https://stackoverflow.com/questions/3430372/how-do-i-get-the-full-path-of-the-current-files-directory
        # from pathlib import Path
        globalsScript = []
        with open(self.globalsApiPath,"r",encoding="utf-8") as globalsFile :
            for line in globalsFile :
                globalsScript.append(line)

        for apiName in self.apiNames :
            updatingApiPath =f'{self.getApiPath(apiName)}{self.localGlobalsApiPath}'
            if apiName != self.globalsApiName :
                with open(updatingApiPath,"w+",encoding="utf-8") as PathMannangerFile :
                    PathMannangerFile.write(''.join(globalsScript))

        # https://stackabuse.com/how-to-copy-a-file-in-python/
        # import shutil
        # shutil.copy2('file1.txt', 'file2.txt')

        self.makeApisAvaliable()

    def makeApisAvaliable(self) :
        self.modulesNodeTree = []
        for apiName in PathMannanger.API_LIST :
            self.modulesNodeTree.append(self.makePathTreeAvaliable(self.getApiPath(apiName)))
        print(f'PathMannanger.modulesNodeTree = {self.modulesNodeTree}')

    def getPathTreeFromPath(self,path):
        node = {}
        nodeSons = os.listdir(path)
        for nodeSon in nodeSons :
            if self.nodeIsValid(nodeSon) :
                nodeSonPath = f'{path}\\{nodeSon}'
                try :
                    node[nodeSon] = self.getPathTreeFromPath(nodeSonPath)
                except : pass
        return node

    def makePathTreeAvaliable(self,path):
        node = {}
        nodeSons = os.listdir(path)
        for nodeSon in nodeSons :
            if self.nodeIsValid(nodeSon) :
                nodeSonPath = f'{path}\\{nodeSon}'
                try :
                    node[nodeSon] = self.makePathTreeAvaliable(nodeSonPath)
                except : pass
        sys.path.append(path)
        return node

    def nodeIsValid(self,node):
        return (len(node.split('__')) == 1) and (node not in PathMannanger.NODE_IGNORE)

    def getExtension(self):
        return PathMannanger.EXTENSION

    # def newApplicationHandler(self):
    #     import ApplicationHandler
    #     self.applicationHandler = ApplicationHandler.ApplicationHandler(self)
