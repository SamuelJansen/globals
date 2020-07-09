import os, sys
from pathlib import Path

class AttributeKey:

    KW_API = 'api'
    KW_NAME = 'name'
    KW_EXTENSION = 'extension'
    KW_DEPENDENCY = 'dependency'
    KW_LIST = 'list'
    KW_WEB = 'web'
    KW_LOCAL = 'local'
    KW_UPDATE = 'update'
    KW_RESOURCE = 'resource'

    GLOBALS_API_LIST = f'{KW_API}.{KW_LIST}'

    API_NAME = f'{KW_API}.{KW_NAME}'
    API_EXTENSION = f'{KW_API}.{KW_EXTENSION}'
    UPDATE_GLOBALS = f'{KW_UPDATE}-globals'
    PRINT_STATUS = 'print-status'
    DEPENDENCY_UPDATE = f'{KW_API}.{KW_DEPENDENCY}.{KW_UPDATE}'
    DEPENDENCY_LIST_WEB = f'{KW_API}.{KW_DEPENDENCY}.{KW_LIST}.{KW_WEB}'
    DEPENDENCY_LIST_LOCAL = f'{KW_API}.{KW_DEPENDENCY}.{KW_LIST}.{KW_LOCAL}'
    DEPENDENCY_RESOURCE_LIST = f'{KW_API}.{KW_DEPENDENCY}.{KW_LIST}.{KW_LOCAL}'

    def getKey(api,key):
        return f'{Globals.__name__}.{key}'

    def getKeyByClassNameAndKey(cls,key):
        return f'{cls.__name__}.{key}'


class Globals:

    OS_SEPARATOR = os.path.sep

    ### There are 'places' where backslash is not much wellcome
    ### Having it stored into a variable helps a lot
    TAB_UNITS = 4
    SPACE = ''' '''
    TAB = TAB_UNITS * SPACE
    BACK_SLASH = '''\\'''
    SLASH = '''/'''
    HASH_TAG = '''#'''
    COLON = ''':'''
    COMA = ''','''
    SPACE = ''' '''
    DOT = '''.'''
    NEW_LINE = '''\n'''
    BAR_N = '''\\n'''
    NOTHING = ''''''
    SINGLE_QUOTE = """'"""
    DOUBLE_QUOTE = '''"'''
    TRIPLE_SINGLE_QUOTE = """'''"""
    TRIPLE_DOUBLE_QUOTE = '''"""'''
    DASH = '''-'''
    SPACE_DASH_SPACE = ''' - '''
    UNDERSCORE = '''_'''
    COLON_SPACE = ': '

    EXTENSION = 'yml'
    PYTHON_EXTENSION = 'py'

    ENCODING = 'utf-8'
    OVERRIDE = 'w+'
    READ = 'r'


    API_BACK_SLASH = f'api{OS_SEPARATOR}'
    SRC_BACK_SLASH = f'src{OS_SEPARATOR}'
    BASE_API_PATH = f'{API_BACK_SLASH}{SRC_BACK_SLASH}'

    GLOBALS_BACK_SLASH = f'globals{OS_SEPARATOR}'
    FRAMEWORK_BACK_SLASH = f'framework{OS_SEPARATOR}'
    SERVICE_BACK_SLASH = f'service{OS_SEPARATOR}'
    RESOURCE_BACK_SLASH = f'resource{OS_SEPARATOR}'
    REPOSITORY_BACK_SLASH = f'repository{OS_SEPARATOR}'
    DEPENDENCY_BACK_SLASH = f'dependency{OS_SEPARATOR}'

    LOCAL_GLOBALS_API_PATH = f'{SERVICE_BACK_SLASH}{FRAMEWORK_BACK_SLASH}{GLOBALS_BACK_SLASH}'

    PIP_INSTALL = f'pip install'
    UPDATE_PIP_INSTALL = 'python -m pip install --upgrade pip'

    CHARACTERE_FILTER = [
        '__'
    ]

    NODE_IGNORE_LIST = [
        '.git',
        'distribution',
        'dist',
        '__pycache__',
        '__init__',
        '__main__',
        'image',
        'audio',
        '.heroku',
        '.profile.d'
    ]

    STRING = 'str'
    INTEGER = 'int'
    BOOLEAN = 'bool'

    TRUE = 'True'
    FALSE = 'False'

    OPEN_TUPLE_CLASS = 'tuple'
    OPEN_LIST_CLASS = 'list'
    DICTIONARY_CLASS = 'dict'
    OPEN_TUPLE = '('
    OPEN_LIST = '['
    OPEN_DICTIONARY = '{'

    SAFE_AMOUNT_OF_TRIPLE_SINGLE_OR_DOUBLE_QUOTES_PLUS_ONE = 4

    DEBUG =     '[DEBUG  ] '
    ERROR =     '[ERROR  ] '
    WARNING =   '[WARNING] '
    SUCCESS =   '[SUCCESS] '
    FAILURE =   '[FAILURE] '
    SETTING =   '[SETTING] '

    def __init__(self, filePath,
        successStatus = False,
        settingStatus = False,
        debugStatus = False,
        warningStatus = False,
        failureStatus = False,
        errorStatus = False,
        encoding = ENCODING,
        globalsEverything = False
    ):

        clear = lambda: os.system('cls')
        ###- clear() # or simply os.system('cls')

        self.filePath = filePath
        self.successStatus = successStatus
        self.settingStatus = settingStatus
        self.debugStatus = debugStatus
        self.warningStatus = warningStatus
        self.failureStatus = failureStatus
        self.errorStatus = errorStatus
        self.globalsEverything = globalsEverything
        self.setting(self.__class__,f'successStatus={self.successStatus}, settingStatus={self.settingStatus}, debugStatus={self.debugStatus}, warningStatus={self.warningStatus}, failureStatus={self.failureStatus}, errorStatus={self.errorStatus}, globalsEverything={self.globalsEverything}')

        self.charactereFilterList = Globals.CHARACTERE_FILTER
        self.nodeIgnoreList = Globals.NODE_IGNORE_LIST
        if encoding :
            self.encoding = encoding
        else :
            self.encoding = Globals.ENCODING

        self.buildApplicationPath()

        self.settingTree = self.getSettingTree()
        self.apiName = self.getApiName()
        self.extension = self.getExtension()

        self.printStatus = self.getGlobalsPrintStatus()
        self.apiNameList = self.getGlobalsApiNameList()

        if self.printStatus :
            print(f'''            {self.__class__.__name__} = {self}
            {self.__class__.__name__}.currentPath =     {self.currentPath}
            {self.__class__.__name__}.localPath =       {self.localPath}
            {self.__class__.__name__}.baseApiPath =     {self.baseApiPath}
            {self.__class__.__name__}.apiPath =         {self.apiPath}
            {self.__class__.__name__}.apisRoot =        {self.apisRoot}
            {self.__class__.__name__}.apisPath =        {self.apisPath}
            {self.__class__.__name__}.apiPackage =      {self.apiPackage}
            {self.__class__.__name__}.apiName =         {self.apiName}
            {self.__class__.__name__}.extension =       {self.extension}\n''')

            self.printTree(self.settingTree,f'{self.__class__.__name__} settings tree')

        self.update()

    def buildApplicationPath(self):
        if self.filePath :
            self.currentPath = f'{str(Path(self.filePath).parent.absolute())}{self.OS_SEPARATOR}'
        else :
            self.currentPath = f'{str(Path(__file__).parent.absolute())}{self.OS_SEPARATOR}'
        self.localPath = f'{str(Path.home())}{self.OS_SEPARATOR}'

        self.baseApiPath = Globals.BASE_API_PATH
        self.apiPath = self.currentPath.split(self.baseApiPath)[0]

        lastLocalPathPackage = self.localPath.split(self.OS_SEPARATOR)[-2]
        firstBaseApiPath = self.baseApiPath.split(self.OS_SEPARATOR)[0]
        lastLocalPathPackageNotFound = True
        self.apiPackage = Globals.NOTHING
        for currentPackage in self.currentPath.split(self.OS_SEPARATOR) :
            if lastLocalPathPackageNotFound :
                if currentPackage == lastLocalPathPackage :
                    lastLocalPathPackageNotFound = False
            elif not currentPackage or currentPackage == firstBaseApiPath :
                break
            else :
                self.apiPackage = currentPackage

        if self.apiPackage != Globals.NOTHING :
            if len(self.currentPath.split(self.localPath)[1].split(self.apiPackage)) > 1:
                self.apisRoot = self.currentPath.split(self.localPath)[1].split(self.apiPackage)[0]
            self.apisPath = f'{self.currentPath.split(self.apiPackage)[0]}'
        else :
            self.apisRoot = Globals.NOTHING
            self.apisPath = Globals.NOTHING

    def getApiPath(self,apiName):
        if not apiName == Globals.NOTHING :
             return f'{self.localPath}{self.apisRoot}{apiName}{self.OS_SEPARATOR}{self.baseApiPath}'
        return f'{self.localPath}{self.baseApiPath}'

    def update(self) :
        self.updateDependencies()
        self.makeApiAvaliable(self.apiPackage)
        self.makeApisAvaliable(self.apisPath)
        self.giveFrameworLocalkVisibility()

    def makeApiAvaliable(self,apiPackageName) :
        self.apiTree = {}
        try :
            apiPath = self.getApiPath(apiPackageName)
            self.apiTree[apiPackageName] = self.makePathTreeVisible(self.getApiPath(apiPackageName))
        except Exception as exception :
            self.error(self.__class__,f'Not possible to make {apiPackageName} api avaliable',exception)
        if self.debugStatus :
            self.printTree(self.apiTree,'Api tree')

    def makeApisAvaliable(self,apisPath):
        if self.globalsEverything :
            apiPackageList = os.listdir(apisPath)
            for apiPackage in apiPackageList :
                if not apiPackage in list(self.apiTree.keys()) :
                    self.apiTree[apiPackage] = self.makePathTreeVisible(f'{apisPath}{apiPackage}')
        if self.debugStatus :
            self.printTree(self.apiTree,'Api tree')

    def giveFrameworLocalkVisibility(self):
        if 'PythonFramework' == self.apiName :
            localApiNameList = os.listdir(self.apisPath)
            for apiName in localApiNameList :
                if apiName not in self.apiTree.keys() :
                    self.apiTree[apiName] = {}

    def makePathTreeVisible(self,path):
        node = {}
        nodeSons = os.listdir(path)
        for nodeSon in nodeSons :
            if self.nodeIsValid(nodeSon) :
                nodeSonPath = f'{path}{self.OS_SEPARATOR}{nodeSon}'
                try :
                    node[nodeSon] = self.makePathTreeVisible(nodeSonPath)
                except :
                    node[nodeSon] = ""
        sys.path.append(path)
        return node

    def nodeIsValid(self,node):
        return self.nodeIsValidByFilter(node) and (node not in self.nodeIgnoreList)

    def nodeIsValidByFilter(self,node):
        for charactere in self.charactereFilterList :
            if not len(node.split(charactere)) == 1 :
                return False
        return True

    def getPathTreeFromPath(self,path):
        node = {}
        nodeSons = os.listdir(path)
        for nodeSon in nodeSons :
            if self.nodeIsValid(nodeSon) :
                nodeSonPath = f'{path}{self.OS_SEPARATOR}{nodeSon}'
                try :
                    node[nodeSon] = self.getPathTreeFromPath(nodeSonPath)
                except : pass
        return node

    def lineAproved(self,settingLine) :
        approved = True
        if Globals.NEW_LINE == settingLine  :
            approved = False
        if Globals.HASH_TAG in settingLine :
            filteredSettingLine = self.filterString(settingLine)
            if None == filteredSettingLine or Globals.NOTHING == filteredSettingLine or Globals.NEW_LINE == filteredSettingLine :
                approved = False
        return approved

    def overrideApiTree(self,apiName,package=None):
        if package :
            actualPackage = package + self.OS_SEPARATOR
        else :
            actualPackage = apiName + self.OS_SEPARATOR
        self.apiName = apiName
        self.apiPackage = package
        self.apiPath = f'{self.apisPath}{actualPackage}'
        settingFilePath = f'{self.apiPath}{Globals.API_BACK_SLASH}{Globals.RESOURCE_BACK_SLASH}{self.__class__.__name__}.{Globals.EXTENSION}'
        self.settingTree = self.getSettingTree(settingFilePath=settingFilePath,settingTree=self.settingTree)


    def getSettingTree(self,settingFilePath=None,settingTree=None) :
        if not settingFilePath :
            settingFilePath = f'{self.apiPath}{Globals.API_BACK_SLASH}{Globals.RESOURCE_BACK_SLASH}{self.__class__.__name__}.{Globals.EXTENSION}'
        with open(settingFilePath,Globals.READ,encoding=Globals.ENCODING) as settingsFile :
            allSettingLines = settingsFile.readlines()
        longStringCapturing = False
        quoteType = None
        longStringList = None
        depth = 0
        depthPass = None
        nodeRefference = 0
        nodeKey = Globals.NOTHING
        if not settingTree :
            settingTree = {}
        for line, settingLine in enumerate(allSettingLines) :
            if self.lineAproved(settingLine) :
                if longStringCapturing :
                    if not depthPass :
                        depthPass = Globals.TAB_UNITS
                    if not currentDepth :
                        currentDepth = 0
                    longStringList.append(settingLine[depth:])
                    if quoteType in str(settingLine) :
                        longStringList[-1] = Globals.NOTHING.join(longStringList[-1].split(quoteType))[:-1] + quoteType
                        settingValue = Globals.NOTHING.join(longStringList)
                        nodeKey = self.updateSettingTreeAndReturnNodeKey(nodeKey,settingTree,settingKey,settingValue)
                        longStringCapturing = False
                        quoteType = None
                        longStringList = None
                else :
                    currentDepth = self.getDepth(settingLine)
                    if currentDepth == depth :
                        settingKey,settingValue,nodeKey,longStringCapturing,quoteType,longStringList = self.settingsTreeInnerLoop(
                            settingLine,
                            nodeKey,
                            settingTree,
                            longStringCapturing,
                            quoteType,
                            longStringList
                        )
                    elif currentDepth > depth :
                        if not depthPass :
                            depthPass = currentDepth - depth
                        currentNodeRefference = currentDepth // (currentDepth - depth)
                        if currentNodeRefference - nodeRefference == 1 :
                            settingKey,settingValue,nodeKey,longStringCapturing,quoteType,longStringList = self.settingsTreeInnerLoop(
                                settingLine,
                                nodeKey,
                                settingTree,
                                longStringCapturing,
                                quoteType,
                                longStringList
                            )
                            nodeRefference = currentNodeRefference
                            depth = currentDepth
                    elif currentDepth < depth :
                        nodeRefference = currentDepth // depthPass
                        depth = currentDepth
                        splitedNodeKey = nodeKey.split(Globals.DOT)[:nodeRefference]
                        splitedNodeKeyLength = len(splitedNodeKey)
                        if splitedNodeKeyLength == 0 :
                            nodeKey = Globals.NOTHING
                        elif splitedNodeKeyLength == 1 :
                            nodeKey = splitedNodeKey[0]
                        else :
                            nodeKey = Globals.DOT.join(splitedNodeKey)
                        settingKey,settingValue,nodeKey,longStringCapturing,quoteType,longStringList = self.settingsTreeInnerLoop(
                            settingLine,
                            nodeKey,
                            settingTree,
                            longStringCapturing,
                            quoteType,
                            longStringList
                        )
                        depth = currentDepth
        return settingTree

    def settingsTreeInnerLoop(self,settingLine,nodeKey,settingTree,longStringCapturing,quoteType,longStringList):
        settingKey,settingValue = self.getAttributeKeyValue(settingLine)
        settingValueAsString = str(settingValue)
        if settingValue and Globals.STRING == settingValue.__class__.__name__ :
            ammountOfTripleSingleOrDoubleQuotes = settingValue.count(Globals.TRIPLE_SINGLE_QUOTE) + settingValue.count(Globals.TRIPLE_DOUBLE_QUOTE)
        else :
            ammountOfTripleSingleOrDoubleQuotes = 0
        if settingValue and (Globals.TRIPLE_SINGLE_QUOTE in settingValueAsString or Globals.TRIPLE_DOUBLE_QUOTE in settingValueAsString) and ammountOfTripleSingleOrDoubleQuotes < Globals.SAFE_AMOUNT_OF_TRIPLE_SINGLE_OR_DOUBLE_QUOTES_PLUS_ONE :
            longStringCapturing = True
            splitedSettingValueAsString = settingValueAsString.split(Globals.TRIPLE_SINGLE_QUOTE)
            if Globals.TRIPLE_SINGLE_QUOTE in settingValueAsString and splitedSettingValueAsString and Globals.TRIPLE_DOUBLE_QUOTE not in splitedSettingValueAsString[0] :
                quoteType = Globals.TRIPLE_SINGLE_QUOTE
            else :
                quoteType = Globals.TRIPLE_DOUBLE_QUOTE
            longStringList = [settingValue + Globals.NEW_LINE]
        else :
            nodeKey = self.updateSettingTreeAndReturnNodeKey(nodeKey,settingTree,settingKey,settingValue)
        return settingKey,settingValue,nodeKey,longStringCapturing,quoteType,longStringList

    def addTree(self,settingFilePath):
        newSetting = self.getSettingTree(settingFilePath=settingFilePath)
        for settingKey,settingValue in newSetting.items() :
            self.settingTree[settingKey] = settingValue

    def concatenateTree(self,settingFilePath,tree):
        newSetting = self.getSettingTree(settingFilePath=settingFilePath)
        for settingKey in newSetting :
            tree[settingKey] = newSetting[settingKey]

    def getApiSetting(self,attributeKeyWithoutApiNameAsRoot):
        return self.getSetting(AttributeKey.getKey(self,attributeKeyWithoutApiNameAsRoot))

    def getSetting(self,nodeKey,settingTree=None) :
        if not settingTree :
            settingTree = self.settingTree
        try :
            return self.accessTree(nodeKey,settingTree)
        except Exception as exception :
            self.debug(f'Not possible to get {nodeKey} node key. Cause: {str(exception)}')
            return None

    def accessTree(self,nodeKey,tree) :
        if nodeKey == Globals.NOTHING :
            try :
                return self.filterString(tree)
            except :
                return tree
        else :
            nodeKeyList = nodeKey.split(Globals.DOT)
            lenNodeKeyList = len(nodeKeyList)
            if lenNodeKeyList > 0 and lenNodeKeyList == 1 :
                 nextNodeKey = Globals.NOTHING
            else :
                nextNodeKey = Globals.DOT.join(nodeKeyList[1:])
                ###- self.debug(tree[nodeKeyList[0]],f'nextNodeKey = {nextNodeKey}')
            return self.accessTree(nextNodeKey,tree[nodeKeyList[0]])

    def getAttributeKeyValue(self,settingLine):
        settingKey = self.getAttributeKey(settingLine)
        settingValue = self.getAttibuteValue(settingLine)
        return settingKey,settingValue

    def updateSettingTreeAndReturnNodeKey(self,nodeKey,settingTree,settingKey,settingValue):
        if settingValue or settingValue.__class__.__name__ == Globals.BOOLEAN :
            self.accessTree(nodeKey,settingTree)[settingKey] = settingValue
        else :
            self.accessTree(nodeKey,settingTree)[settingKey] = {}
            if Globals.NOTHING == nodeKey :
                nodeKey += f'{settingKey}'
            else :
                nodeKey += f'{Globals.DOT}{settingKey}'
        return nodeKey

    def getDepth(self,settingLine):
        depthNotFount = True
        depth = 0
        while not settingLine[depth] == Globals.NEW_LINE and depthNotFount:
            if settingLine[depth] == Globals.SPACE:
                depth += 1
            else :
                depthNotFount = False
        return depth

    def getAttributeKey(self,settingLine):
        possibleKey = self.filterString(settingLine)
        return settingLine.strip().split(Globals.COLON)[0].strip()

    def getAttibuteValue(self,settingLine):
        possibleValue = self.filterString(settingLine)
        return self.getValue(Globals.COLON.join(possibleValue.strip().split(Globals.COLON)[1:]).strip())

    def filterString(self,string) :
        if string[-1] == Globals.NEW_LINE :
            string = string[:-1]
        strippedString = string.strip()
        surroundedBySingleQuote = strippedString[0] == Globals.SINGLE_QUOTE and strippedString[-1] == Globals.SINGLE_QUOTE
        surroundedByDoubleQuote = strippedString[0] == Globals.DOUBLE_QUOTE and strippedString[-1] == Globals.DOUBLE_QUOTE
        if Globals.HASH_TAG in strippedString and not (surroundedBySingleQuote or surroundedByDoubleQuote) :
            string = string.split(Globals.HASH_TAG)[0].strip()
        return string

    def getValue(self,value) :
        if value :
            if Globals.OPEN_LIST == value[0] :
                return self.getList(value)
            elif Globals.OPEN_TUPLE == value[0] :
                return self.getTuple(value)
            elif Globals.OPEN_DICTIONARY == value[0] :
                return self.getDictionary(value)
            try :
                return int(value)
            except :
                try :
                    return float(value)
                except :
                    try :
                        if value == Globals.TRUE : return True
                        elif value == Globals.FALSE : return False
                        return value
                    except:
                        return value

    def getList(self,value):
        roughtValues = value[1:-1].split(Globals.COMA)
        values = []
        for value in roughtValues :
            values.append(self.getValue(value.strip()))
        return values

    def getTuple(self,value):
        roughtValues = value[1:-1].split(Globals.COMA)
        values = []
        for value in roughtValues :
            values.append(self.getValue(value.strip()))
        return tuple(values)

    def getDictionary(self,value) :
        splitedValue = value[1:-1].split(Globals.COLON)
        keyList = []
        for index in range(len(splitedValue) -1) :
            keyList.append(splitedValue[index].split(Globals.COMA)[-1].strip())
        valueList = []
        valueListSize = len(splitedValue) -1
        for index in range(valueListSize) :
            if index == valueListSize -1 :
                correctValue = splitedValue[index+1].strip()
            else :
                correctValue = Globals.COMA.join(splitedValue[index+1].split(Globals.COMA)[:-1]).strip()
            valueList.append(self.getValue(correctValue))
        resultantDictionary = {}
        for index in range(len(keyList)) :
            resultantDictionary[keyList[index]] = valueList[index]
        return resultantDictionary

    def getFileNameList(self,path,fileExtension=None) :
        if not fileExtension :
            fileExtension = self.extension
        fileNames = []
        names = os.listdir(path)
        for name in names :
            splitedName = name.split('.')
            if fileExtension == splitedName[-1] :
                fileNames.append(''.join(splitedName[:-1]))
        return fileNames

    def printTree(self,tree,name,depth=0):
        print(f'\n{name}')
        self.printNodeTree(tree,depth)
        print()

    def printNodeTree(self,tree,depth):
        depthSpace = ''
        for nodeDeep in range(depth) :
            depthSpace += f'{Globals.TAB_UNITS * Globals.SPACE}'
        depth += 1
        for node in list(tree) :
            if tree[node].__class__.__name__ == Globals.DICTIONARY_CLASS :
                print(f'{depthSpace}{node}{Globals.SPACE}{Globals.COLON}')
                self.printNodeTree(tree[node],depth)
            else :
                print(f'{depthSpace}{node}{Globals.SPACE}{Globals.COLON}{Globals.SPACE}{tree[node]}')

    def updateDependencies(self):
        try :
            if self.getApiSetting(AttributeKey.DEPENDENCY_UPDATE) :
                import subprocess
                moduleList = self.getApiSetting(AttributeKey.DEPENDENCY_LIST_WEB)
                if moduleList :
                    subprocess.Popen(Globals.UPDATE_PIP_INSTALL).wait()
                    for module in moduleList :
                        subprocess.Popen(f'{Globals.PIP_INSTALL} {module}').wait()
                resourceModuleList = self.getApiSetting(AttributeKey.DEPENDENCY_LIST_LOCAL)
                if resourceModuleList :
                    for resourceModule in resourceModuleList :
                        command = f'{Globals.PIP_INSTALL} {resourceModule}'
                        processPath = f'{self.getApiPath(self.apiName)}{Globals.RESOURCE_BACK_SLASH}{Globals.DEPENDENCY_BACK_SLASH}'
                        subprocess.Popen(command,shell=True,cwd=processPath).wait()
                        ###- subprocess.run(command,shell=True,capture_output=True,cwd=processPath)
        except Exception as exception :
            self.debug(f'Not possible to update dependencies. Cause: {str(exception)}')

    def getGlobalsPrintStatus(self):
        return self.getSetting(AttributeKey.getKeyByClassNameAndKey(Globals,AttributeKey.PRINT_STATUS))

    def getGlobalsApiNameList(self):
        return self.getSetting(AttributeKey.getKeyByClassNameAndKey(Globals,AttributeKey.GLOBALS_API_LIST))

    def getApiName(self):
        try :
            return self.getSetting(f'{self.__class__.__name__}.{AttributeKey.API_NAME}')
        except Exception as exception :
            self.failure(self.__class__,'Not possible to get api name', exception)

    def getExtension(self):
        try :
            return self.getSetting(f'{self.__class__.__name__}.{AttributeKey.API_EXTENSION}')
        except Exception as exception :
            self.failure(self.__class__,'Not possible to get api extenion. Returning default estension', exception)
            return Globals.EXTENSION

    def getSettingFromSettingFilePathAndKeyPair(self,path,settingKey) :
        self.debug(f'''Getting {settingKey} from {path}''')
        with open(path,Globals.READ,encoding=Globals.ENCODING) as settingsFile :
            allSettingLines = settingsFile.readlines()
        for line, settingLine in enumerate(allSettingLines) :
            depth = self.getDepth(settingLine)
            setingKeyLine = self.getAttributeKey(settingLine)
            if settingKey == setingKeyLine :
                settingValue = self.getAttibuteValue(settingLine)
                self.debug(f'''{Globals.TAB}key : value --> {settingKey} : {settingValue}''')
                return settingValue

    def debug(self,message):
        if self.debugStatus :
            print(f'{Globals.DEBUG}{message}')

    def warning(self,string):
        if self.warningStatus :
            print(f'{Globals.WARNING}{string}')

    def error(self,classRequest,message,exception):
        if self.errorStatus :
            if classRequest == Globals.NOTHING :
                classPortion = Globals.NOTHING
            else :
                classPortion = f'{classRequest.__name__} '
            if exception == Globals.NOTHING :
                errorPortion = Globals.NOTHING
            else :
                errorPortion = f'. Cause: {str(exception)}'
            print(f'{Globals.ERROR}{classPortion}{message}{errorPortion}')

    def success(self,classRequest,message):
        if self.successStatus :
            if classRequest == Globals.NOTHING :
                classPortion = Globals.NOTHING
            else :
                classPortion = f'{classRequest.__name__} '
            print(f'{Globals.SUCCESS}{classPortion}{message}')

    def failure(self,classRequest,message,exception):
        if self.failureStatus :
            if classRequest == Globals.NOTHING :
                classPortion = Globals.NOTHING
            else :
                classPortion = f'{classRequest.__name__} '
            if exception == Globals.NOTHING :
                errorPortion = Globals.NOTHING
            else :
                errorPortion = f'. Cause: {str(exception)}'
            print(f'{Globals.FAILURE}{classPortion}{message}{errorPortion}')

    def setting(self,classRequest,message):
        if self.settingStatus :
            if classRequest == Globals.NOTHING :
                classPortion = Globals.NOTHING
            else :
                classPortion = f'{classRequest.__name__} '
            print(f'{Globals.SETTING}{classPortion}{message}')

def getGlobals() :
    try :
        from app import globals
        return globals
    except :
        try :
            from run import globals
            return globals
        except : pass

def getApi() :
    return getGlobals().api

def addTo(self) :
    self.globals = getGlobals()
    self.globals.api = self

def GlobalsResourceMethod(outerMethod,*args,**kwargs):
    def innerMethod(*args,**kwargs):
        try :
            if not args[0].api :
                args[0].api = getApi()
        except :
            try :
                args[0].api = getApi()
            except : pass
        return outerMethod(*args,**kwargs)
    return innerMethod

def GlobalsResource(*argument,**keywordArgument) :
    def Wrapper(OuterClass,*args,**kwargs):
        class InnerClass(OuterClass):
            url = keywordArgument.get('path')
            def __init__(self,*args,**kwargs):
                OuterClass.__init__(self,*args,**kwargs)
                self.api = getApi()
        InnerClass.__name__ = OuterClass.__name__
        InnerClass.__module__ = OuterClass.__module__
        InnerClass.__qualname__ = OuterClass.__qualname__
        # printClass(InnerClass)
        return InnerClass
    return Wrapper

def printClass(Class) :
    print(f'    Class.__name__ = {Class.__name__}')
    print(f'    Class.__module__ = {Class.__module__}')
    print(f'    Class.__qualname__ = {Class.__qualname__}')
