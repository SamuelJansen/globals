import os, sys, subprocess, site
from pathlib import Path
from python_helper import Constant, log

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

    TOKEN_PIP_USER = '__TOKEN_PIP_USER__'
    KW_SPACE_PIP_USER = f'{Constant.SPACE}--user'
    PIP_INSTALL = f'python -m pip install --upgrade{TOKEN_PIP_USER} --force-reinstall'
    UPDATE_PIP_INSTALL = f'python -m pip install --upgrade {TOKEN_PIP_USER} pip'

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

    DIST_DIRECTORY_PATH = f'{OS_SEPARATOR}statics'

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
        printRootPathStatus = False,
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
        self.printRootPathStatus = printRootPathStatus
        self.globalsEverything = globalsEverything
        self.setting(self.__class__,f'successStatus={self.successStatus}, settingStatus={self.settingStatus}, debugStatus={self.debugStatus}, warningStatus={self.warningStatus}, failureStatus={self.failureStatus}, errorStatus={self.errorStatus}, globalsEverything={self.globalsEverything}')
        self.debug(f'{self.__class__.__name__}.filePath = {self.filePath}')

        self.charactereFilterList = Globals.CHARACTERE_FILTER
        self.nodeIgnoreList = Globals.NODE_IGNORE_LIST
        self.encoding = self.getEncoding(encoding)

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

        self.updateDependencyStatus = self.getApiSetting(AttributeKey.DEPENDENCY_UPDATE)
        self.update()

    def buildApplicationPath(self):
        self.distPackage = self.getDistPackagePath()
        if self.filePath :
            self.currentPath = f'{str(Path(self.filePath).parent.absolute())}{self.OS_SEPARATOR}'
        else :
            self.currentPath = f'{str(Path(__file__).parent.absolute())}{self.OS_SEPARATOR}'
        self.localPath = str(Path.home())
        if not self.localPath[-1] == str(self.OS_SEPARATOR) :
            self.localPath = f'{self.localPath}{self.OS_SEPARATOR}'

        self.baseApiPath = Globals.BASE_API_PATH
        self.apiPath = self.currentPath.split(self.baseApiPath)[0]

        lastLocalPathPackage = self.localPath.split(self.OS_SEPARATOR)[-2]
        firstBaseApiPath = self.baseApiPath.split(self.OS_SEPARATOR)[0]
        lastLocalPathPackageNotFound = True
        self.apiPackage = Constant.NOTHING
        for currentPackage in self.currentPath.split(self.OS_SEPARATOR) :
            if lastLocalPathPackageNotFound :
                if currentPackage == lastLocalPathPackage :
                    lastLocalPathPackageNotFound = False
            elif not currentPackage or currentPackage == firstBaseApiPath :
                break
            else :
                self.apiPackage = currentPackage

        if self.apiPackage != Constant.NOTHING :
            if len(self.currentPath.split(self.localPath)[1].split(self.apiPackage)) > 1:
                self.apisRoot = self.currentPath.split(self.localPath)[1].split(self.apiPackage)[0]
            self.apisPath = f'{self.currentPath.split(self.apiPackage)[0]}'
        else :
            self.apisRoot = Constant.NOTHING
            self.apisPath = Constant.NOTHING

    def getApiPath(self,apiPackageName):
        if not apiPackageName == Constant.NOTHING :
             return f'{self.localPath}{self.apisRoot}{apiPackageName}{self.OS_SEPARATOR}'###-'{self.baseApiPath}'
        if self.apisPath :
            return self.apisPath
        if self.localPath :
            return self.localPath
        return f'{self.OS_SEPARATOR}'

    def update(self) :
        self.updateDependencies()
        self.makeApiAvaliable(self.apiPackage)
        self.makeApisAvaliable(self.apisPath)
        self.printRootPath(self.localPath)

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
            try :
                apiPackageList = os.listdir(apisPath)
                for apiPackage in apiPackageList :
                    if not apiPackage in list(self.apiTree.keys()) :
                        self.apiTree[apiPackage] = self.makePathTreeVisible(f'{apisPath}{apiPackage}')
                if self.debugStatus :
                    self.printTree(self.apiTree,f'{Constant.DEBUG}Api tree (globalsEverithing is active)')
            except Exception as exception :
                self.error(self.__class__,f'Not possible to run makeApisAvaliable({apisPath}) rotine',exception)


    def printRootPath(self,rootPath) :
        if self.printRootPathStatus :
            try :
                rootTree = {}
                apiPackageList = os.listdir(rootPath)
                for apiPackage in apiPackageList :
                    rootTree[apiPackage] = self.addNode(f'{rootPath}{apiPackage}')
                if self.debugStatus :
                    self.printTree(rootTree,f'{Constant.DEBUG}Root tree (globalsEverithing is active)')
            except Exception as exception :
                self.error(self.__class__,f'Not possible to run printRootPath({rootPath}) rotine',exception)


    def giveLocalVisibilityToFrameworkApis(self,apiPackageNameList):
        if apiPackageNameList :
            localPackageNameList = os.listdir(self.apisPath)
            for packageName in localPackageNameList :
                if packageName not in self.apiTree.keys() and packageName in apiPackageNameList :
                    packagePath = f'{self.apisPath}{packageName}'
                    try :
                        self.apiTree[packageName] = self.makePathTreeVisible(packagePath)
                    except :
                        self.apiTree[packageName] = Constant.NOTHING
            if self.debugStatus :
                self.printTree(self.apiTree,f'{Constant.DEBUG}Api tree')

    def makePathTreeVisible(self,path):
        node = {}
        nodeSons = os.listdir(path)
        for nodeSon in nodeSons :
            if self.nodeIsValid(nodeSon) :
                nodeSonPath = f'{path}{self.OS_SEPARATOR}{nodeSon}'
                try :
                    node[nodeSon] = self.makePathTreeVisible(nodeSonPath)
                except :
                    node[nodeSon] = Constant.NOTHING
        sys.path.append(path)
        return node

    def addNode(self,nodePath):
        node = {}
        try :
            nodeSons = os.listdir(nodePath)
            for nodeSon in nodeSons :
                nodeSonPath = f'{nodePath}{self.OS_SEPARATOR}{nodeSon}'
                try :
                    node[nodeSon] = self.addNode(nodeSonPath)
                except :
                    node[nodeSon] = Constant.NOTHING
        except Exception as exception :
            self.error(self.__class__,f'Not possible to run addNode({nodePath}) rotine',exception)
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
        if Constant.NEW_LINE == settingLine  :
            approved = False
        if Constant.HASH_TAG in settingLine :
            filteredSettingLine = self.filterString(settingLine)
            if None == filteredSettingLine or Constant.NOTHING == filteredSettingLine or Constant.NEW_LINE == filteredSettingLine :
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
        nodeKey = Constant.NOTHING
        if not settingTree :
            settingTree = {}
        for line, settingLine in enumerate(allSettingLines) :
            if self.lineAproved(settingLine) :
                if longStringCapturing :
                    if not depthPass :
                        depthPass = Constant.TAB_UNITS
                    if not currentDepth :
                        currentDepth = 0
                    longStringList.append(settingLine[depth:])
                    if quoteType in str(settingLine) :
                        longStringList[-1] = Constant.NOTHING.join(longStringList[-1].split(quoteType))[:-1] + quoteType
                        settingValue = Constant.NOTHING.join(longStringList)
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
                        splitedNodeKey = nodeKey.split(Constant.DOT)[:nodeRefference]
                        splitedNodeKeyLength = len(splitedNodeKey)
                        if splitedNodeKeyLength == 0 :
                            nodeKey = Constant.NOTHING
                        elif splitedNodeKeyLength == 1 :
                            nodeKey = splitedNodeKey[0]
                        else :
                            nodeKey = Constant.DOT.join(splitedNodeKey)
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
        if settingValue and Constant.STRING == settingValue.__class__.__name__ :
            ammountOfTripleSingleOrDoubleQuotes = settingValue.count(Constant.TRIPLE_SINGLE_QUOTE) + settingValue.count(Constant.TRIPLE_DOUBLE_QUOTE)
        else :
            ammountOfTripleSingleOrDoubleQuotes = 0
        if settingValue and (Constant.TRIPLE_SINGLE_QUOTE in settingValueAsString or Constant.TRIPLE_DOUBLE_QUOTE in settingValueAsString) and ammountOfTripleSingleOrDoubleQuotes < Globals.SAFE_AMOUNT_OF_TRIPLE_SINGLE_OR_DOUBLE_QUOTES_PLUS_ONE :
            longStringCapturing = True
            splitedSettingValueAsString = settingValueAsString.split(Constant.TRIPLE_SINGLE_QUOTE)
            if Constant.TRIPLE_SINGLE_QUOTE in settingValueAsString and splitedSettingValueAsString and Constant.TRIPLE_DOUBLE_QUOTE not in splitedSettingValueAsString[0] :
                quoteType = Constant.TRIPLE_SINGLE_QUOTE
            else :
                quoteType = Constant.TRIPLE_DOUBLE_QUOTE
            longStringList = [settingValue + Constant.NEW_LINE]
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
        if nodeKey == Constant.NOTHING :
            try :
                return self.filterString(tree)
            except :
                return tree
        else :
            nodeKeyList = nodeKey.split(Constant.DOT)
            lenNodeKeyList = len(nodeKeyList)
            if lenNodeKeyList > 0 and lenNodeKeyList == 1 :
                 nextNodeKey = Constant.NOTHING
            else :
                nextNodeKey = Constant.DOT.join(nodeKeyList[1:])
                ###- self.debug(tree[nodeKeyList[0]],f'nextNodeKey = {nextNodeKey}')
            return self.accessTree(nextNodeKey,tree[nodeKeyList[0]])

    def getAttributeKeyValue(self,settingLine):
        settingKey = self.getAttributeKey(settingLine)
        settingValue = self.getAttibuteValue(settingLine)
        return settingKey,settingValue

    def updateSettingTreeAndReturnNodeKey(self,nodeKey,settingTree,settingKey,settingValue):
        if settingValue or settingValue.__class__.__name__ == Constant.BOOLEAN :
            self.accessTree(nodeKey,settingTree)[settingKey] = settingValue
        else :
            self.accessTree(nodeKey,settingTree)[settingKey] = {}
            if Constant.NOTHING == nodeKey :
                nodeKey += f'{settingKey}'
            else :
                nodeKey += f'{Constant.DOT}{settingKey}'
        return nodeKey

    def getDepth(self,settingLine):
        depthNotFount = True
        depth = 0
        while not settingLine[depth] == Constant.NEW_LINE and depthNotFount:
            if settingLine[depth] == Constant.SPACE :
                depth += 1
            else :
                depthNotFount = False
        return depth

    def getAttributeKey(self,settingLine):
        possibleKey = self.filterString(settingLine)
        return settingLine.strip().split(Constant.COLON)[0].strip()

    def getAttibuteValue(self,settingLine):
        possibleValue = self.filterString(settingLine)
        return self.getValue(Constant.COLON.join(possibleValue.strip().split(Constant.COLON)[1:]).strip())

    def filterString(self,string) :
        if string[-1] == Constant.NEW_LINE :
            string = string[:-1]
        strippedString = string.strip()
        surroundedBySingleQuote = strippedString[0] == Constant.SINGLE_QUOTE and strippedString[-1] == Constant.SINGLE_QUOTE
        surroundedByDoubleQuote = strippedString[0] == Constant.DOUBLE_QUOTE and strippedString[-1] == Constant.DOUBLE_QUOTE
        if Constant.HASH_TAG in strippedString and not (surroundedBySingleQuote or surroundedByDoubleQuote) :
            string = string.split(Constant.HASH_TAG)[0].strip()
        return string

    def getValue(self,value) :
        if value :
            if Constant.OPEN_LIST == value[0] :
                return self.getList(value)
            elif Constant.OPEN_TUPLE == value[0] :
                return self.getTuple(value)
            elif Constant.OPEN_DICTIONARY == value[0] :
                return self.getDictionary(value)
            try :
                return int(value)
            except :
                try :
                    return float(value)
                except :
                    try :
                        if value == Constant.TRUE : return True
                        elif value == Constant.FALSE : return False
                        return value
                    except:
                        return value

    def getList(self,value):
        roughtValues = value[1:-1].split(Constant.COMA)
        values = []
        for value in roughtValues :
            values.append(self.getValue(value.strip()))
        return values

    def getTuple(self,value):
        roughtValues = value[1:-1].split(Constant.COMA)
        values = []
        for value in roughtValues :
            values.append(self.getValue(value.strip()))
        return tuple(values)

    def getDictionary(self,value) :
        splitedValue = value[1:-1].split(Constant.COLON)
        keyList = []
        for index in range(len(splitedValue) -1) :
            keyList.append(splitedValue[index].split(Constant.COMA)[-1].strip())
        valueList = []
        valueListSize = len(splitedValue) -1
        for index in range(valueListSize) :
            if index == valueListSize -1 :
                correctValue = splitedValue[index+1].strip()
            else :
                correctValue = Constant.COMA.join(splitedValue[index+1].split(Constant.COMA)[:-1]).strip()
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
            depthSpace += f'{Constant.TAB_UNITS * Constant.SPACE}'
        depth += 1
        for node in list(tree) :
            if tree[node].__class__.__name__ == Globals.DICTIONARY_CLASS :
                print(f'{depthSpace}{node}{Constant.SPACE}{Constant.COLON}')
                self.printNodeTree(tree[node],depth)
            else :
                print(f'{depthSpace}{node}{Constant.SPACE}{Constant.COLON}{Constant.SPACE}{tree[node]}')

    def updateDependencies(self):
        try :
            if self.updateDependencyStatus :
                moduleList = self.getApiSetting(AttributeKey.DEPENDENCY_LIST_WEB)
                localPackageNameList = self.getApiSetting(AttributeKey.DEPENDENCY_LIST_LOCAL)
                if moduleList or localPackageNameList :
                    self.runUpdateCommand(Globals.UPDATE_PIP_INSTALL)
                if moduleList :
                    for module in moduleList :
                        command = f'{Globals.PIP_INSTALL} {module}'
                        self.runUpdateCommand(command)
                if localPackageNameList :
                    for localPackageName in localPackageNameList :
                        localPackagePath = f'"{self.apiPath}{Globals.API_BACK_SLASH}{Globals.RESOURCE_BACK_SLASH}{Globals.DEPENDENCY_BACK_SLASH}{localPackageName}"'
                        command = f'{Globals.PIP_INSTALL} {localPackagePath}'
                        self.runUpdateCommand(command)
        except Exception as exception :
            self.error(self.__class__,'Not possible to update dependencies',exception)

    def runUpdateCommand(self,command):
        commonExceptionMessage = 'Not possible to update dependencies'
        LOG_FIRST_TRY =     '[FIRST_TRY ]'
        LOG_SECOND_TRY =    '[SECOND_TRY]'
        LOG_COMMAND = f'command'
        LOG_RESPONSE = f'response'
        LOG_SUCCESS = 'SUCCESS'
        LOG_FAIL = 'FAIL'
        KW_DIDNT_RUN = 'DIDNT_RUN'
        def getCommandLog(tryOrder,command):
            return f'{tryOrder}{Constant.SPACE}{LOG_COMMAND}{Constant.COLON_SPACE}{command}'
        def getResponseLog(tryOrder,command,response):
            logResponse = f'{tryOrder}{Constant.SPACE}{LOG_COMMAND}{Constant.COLON_SPACE}{command}'
            logResponse = f'{logResponse}{Constant.SPACE_DASH_SPACE}{LOG_RESPONSE}{Constant.COLON_SPACE}'
            if 1 == response :
                return f'{logResponse}{LOG_FAIL}'
            elif 0 == response :
                return f'{logResponse}{LOG_SUCCESS}'
            else :
                return f'{logResponse}{response}'
        commandFirstTry = command.replace(self.TOKEN_PIP_USER,self.KW_SPACE_PIP_USER)
        self.debug(getCommandLog(LOG_FIRST_TRY,commandFirstTry))
        responseFirstTry = KW_DIDNT_RUN
        try :
            responseFirstTry = subprocess.Popen(commandFirstTry).wait()
            self.debug(getResponseLog(LOG_FIRST_TRY,commandFirstTry,responseFirstTry))
        except Exception as exceptionFirstTry :
            self.error(self.__class__,f'{commonExceptionMessage}',exceptionFirstTry)
        if KW_DIDNT_RUN == responseFirstTry or 1 == responseFirstTry :
            commandSecondTry = command.replace(self.TOKEN_PIP_USER,Constant.NOTHING)
            self.debug(getCommandLog(LOG_SECOND_TRY,commandSecondTry))
            responseSecondTry = KW_DIDNT_RUN
            try :
                responseSecondTry = subprocess.Popen(commandSecondTry).wait()
                self.debug(getResponseLog(LOG_SECOND_TRY,commandSecondTry,responseSecondTry))
            except Exception as exceptionSecondTry :
                self.error(self.__class__,f'{commonExceptionMessage}',exceptionSecondTry)
            if KW_DIDNT_RUN == responseFirstTry and KW_DIDNT_RUN == responseSecondTry :
                log.error(self.__class__,f'Not possible to run {commandFirstTry}',Exception(f'Both attempt failed'))

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
                self.debug(f'''{Constant.TAB}key : value --> {settingKey} : {settingValue}''')
                return settingValue

    def getDistPackagePath(self) :
        distPackageList = site.getsitepackages()
        self.debug(f'Dist packages list: {distPackageList}. Picking the first one')
        distPackage = str(distPackageList[0])
        distPackage = distPackage.replace(f'{self.BACK_SLASH}{self.BACK_SLASH}',self.OS_SEPARATOR)
        distPackage = distPackage.replace(self.SLASH,self.OS_SEPARATOR)
        distPackage = distPackage.replace(self.BACK_SLASH,self.OS_SEPARATOR)
        if distPackage[-1] == str(self.OS_SEPARATOR) or distPackage[-1] == self.SLASH :
            distPackage = distPackage[:-1]
        distPackage = f'{distPackage}{self.DIST_DIRECTORY_PATH}'
        if distPackage and distPackage.lower().endswith(f'{self.OS_SEPARATOR}lib{self.OS_SEPARATOR}site-packages') :
            distPackage = distPackage.replace(f'{self.OS_SEPARATOR}lib{self.OS_SEPARATOR}site-packages',Constant.NOTHING)
        if distPackage and os.path.isdir(f'.{self.OS_SEPARATOR}{distPackage}') :
            try :
                sys.path.append(f'.{self.OS_SEPARATOR}{distPackage}')
            except Exception as exception :
                self.error(self.__class__,f'Not possible to append static file directory: "{distPackage}"',exception)
        self.debug(f'Dist package: "{distPackage}"')
        return distPackage

    def getEncoding(self, encoding) :
        if encoding :
            return encoding
        else :
            return Globals.ENCODING

    def debug(self,message):
        if self.debugStatus :
            print(f'{Constant.DEBUG}{message}')

    def warning(self,string):
        if self.warningStatus :
            print(f'{Constant.WARNING}{string}')

    def error(self,classRequest,message,exception):
        if self.errorStatus :
            if classRequest == Constant.NOTHING :
                classPortion = Constant.NOTHING
            else :
                classPortion = f'{classRequest.__name__} '
            if exception == Constant.NOTHING :
                errorPortion = Constant.NOTHING
            else :
                errorPortion = f'. Cause: {str(exception)}'
            print(f'{Constant.ERROR}{classPortion}{message}{errorPortion}')

    def success(self,classRequest,message):
        if self.successStatus :
            if classRequest == Constant.NOTHING :
                classPortion = Constant.NOTHING
            else :
                classPortion = f'{classRequest.__name__} '
            print(f'{Constant.SUCCESS}{classPortion}{message}')

    def failure(self,classRequest,message,exception):
        if self.failureStatus :
            if classRequest == Constant.NOTHING :
                classPortion = Constant.NOTHING
            else :
                classPortion = f'{classRequest.__name__} '
            if exception == Constant.NOTHING :
                errorPortion = Constant.NOTHING
            else :
                errorPortion = f'. Cause: {str(exception)}'
            print(f'{Constant.FAILURE}{classPortion}{message}{errorPortion}')

    def setting(self,classRequest,message):
        if self.settingStatus :
            if classRequest == Constant.NOTHING :
                classPortion = Constant.NOTHING
            else :
                classPortion = f'{classRequest.__name__} '
                print(f'{Constant.SETTING}{classPortion}{message}')

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
