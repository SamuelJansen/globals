import os, sys

class AttributeKey:

    KW_API = 'api'
    KW_EXTENSION = 'extension'
    KW_DEPENDENCY = 'dependency'
    KW_LIST = 'list'
    KW_UPDATE = 'update'
    KW_RESOURCE = 'resource'

    GLOBALS_API_LIST = f'{KW_API}.{KW_LIST}'

    API_EXTENSION = f'{KW_API}.{KW_EXTENSION}'
    UPDATE_GLOBALS = f'{KW_UPDATE}-globals'
    PRINT_STATUS = 'print-status'
    DEPENDENCY_UPDATE = f'{KW_API}.{KW_DEPENDENCY}.{KW_UPDATE}'
    DEPENDENCY_LIST = f'{KW_API}.{KW_DEPENDENCY}.{KW_LIST}'
    DEPENDENCY_RESOURCE_LIST = f'{KW_API}.{KW_DEPENDENCY}.{KW_RESOURCE}.{KW_LIST}'

    def getKey(api,key):
        return f'{api.apiName}.{key}'

    def getKeyByClassNameAndKey(cls,key):
        return f'{cls.__name__}.{key}'


class Globals:
    ### There are 'places' where backslash is not much wellcome
    ### Having it stored into a variable helps a lot
    TAB_UNITS = 2
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

    BASE_API_PATH = f'api{BACK_SLASH}src{BACK_SLASH}'
    LOCAL_GLOBALS_API_PATH = f'domain{BACK_SLASH}control{BACK_SLASH}'

    EXTENSION = 'gbl'
    PYTHON_EXTENSION = 'py'

    ENCODING = 'utf-8'
    OVERRIDE = 'w+'
    READ = 'r'

    RESOURCE_BACK_SLASH = f'resource{BACK_SLASH}'
    REPOSITORY_BACK_SLASH = f'repository{BACK_SLASH}'

    PIP_INSTALL = f'pip install'
    UPDATE_PIP_INSTALL = 'python -m pip install --upgrade pip'

    CHARACTERE_FILTER = [
        '__'
    ]

    NODE_IGNORE_LIST = [
        '.git',
        '__pycache__',
        '__init__',
        '__main__',
        'image',
        'audio'
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

    WRONG_WAY_TO_IMPLEMENT_IT = 'WRONG_WAY_TO_IMPLEMENT_IT'
    PROPER_WAY_TO_IMPLEMENT_IT = 'PROPER_WAY_TO_IMPLEMENT_IT'

    GIT_COMMITTER = 'git-committer'
    OFFICE_TRACK_INTEGRATION_TESTS = 'office-track-integration-tests'
    VOICE_ASSISTANT = 'voice-assistant'
    WEB_SCRAP_HELPER = 'web-scraper'
    CIFRAS_CLUB_WEB_SCRAPER = f'cifras-club-{WEB_SCRAP_HELPER}'
    FACEBOOK_CLASS_MANAGER = f'facebook-class'
    API_SYS_ARGV_INDEX = 1

    SYSTEM_HELPER_NAME = 'SystemHelper'

    DEBUG = '[Debug] '
    ERROR = '[Error] '

    def __init__(self,
        mode = PROPER_WAY_TO_IMPLEMENT_IT,
        encoding = ENCODING,
        debugStatus = False
    ):

        from pathlib import Path
        clear = lambda: os.system('cls')
        ###- clear() # or simply os.system('cls')

        self.globalsApiName = self.__class__.__name__
        self.debugStatus = debugStatus
        self.debug('Debug mode on')

        self.mode = mode
        self.backSlash = Globals.BACK_SLASH
        self.charactereFilterList = Globals.CHARACTERE_FILTER
        self.nodeIgnoreList = Globals.NODE_IGNORE_LIST
        self.currentPath = f'{str(Path(__file__).parent.absolute())}{self.backSlash}'
        self.localPath = f'{str(Path.home())}{self.backSlash}'
        if encoding :
            self.encoding = encoding
        else :
            self.encoding = Globals.ENCODING
        if self.mode == Globals.PROPER_WAY_TO_IMPLEMENT_IT :
            self.baseApiPath = Globals.BASE_API_PATH
            self.apiPath = self.currentPath.split(self.baseApiPath)[0]
            self.apiName = self.apiPath.split(self.backSlash)[-2]
            self.systemHelperRunning = (self.apiName == Globals.SYSTEM_HELPER_NAME)
            self.apisRoot = self.currentPath.split(self.localPath)[1].split(self.apiName)[0]

            self.settingTree = self.getSettingTree()
            try :
                self.extension = self.getSetting(f'{self.globalsApiName}.{AttributeKey.API_EXTENSION}',self.settingTree)
            except :
                self.extension = Globals.EXTENSION

            self.printStatus = self.getGlobalsPrintStatus()
            self.apiNameList = self.getGlobalsApiList()

            self.localGlobalsApiFilePath = f'{Globals.LOCAL_GLOBALS_API_PATH}{self.globalsApiName}.{Globals.PYTHON_EXTENSION}'
            self.globalsApiPath = f'{self.getApiPath(self.globalsApiName)}{self.localGlobalsApiFilePath}'
            self.apisPath = f'{self.currentPath.split(self.apiName)[0]}'

            self.updateGlobals = self.getUpdateGlobalsClassFile()

            if self.printStatus :
                print(f'''                {self.__class__.__name__} = {self}
                {self.__class__.__name__}.currentPath =                 {self.currentPath}
                {self.__class__.__name__}.localPath =                   {self.localPath}
                {self.__class__.__name__}.baseApiPath =                 {self.baseApiPath}
                {self.__class__.__name__}.apiPath =                     {self.apiPath}
                {self.__class__.__name__}.apiName =                     {self.apiName}
                {self.__class__.__name__}.apisRoot =                    {self.apisRoot}
                {self.__class__.__name__}.apiNameList =                 {self.apiNameList}
                {self.__class__.__name__}.localGlobalsApiFilePath =     {self.localGlobalsApiFilePath}
                {self.__class__.__name__}.globalsApiName =              {self.globalsApiName}
                {self.__class__.__name__}.globalsApiPath =              {self.globalsApiPath}
                {self.__class__.__name__}.apisPath =                    {self.apisPath}
                {self.__class__.__name__}.extension =                   {self.extension}\n''')

                self.printTree(self.settingTree,f'{self.__class__.__name__} settin tree')

            self.update()

        elif self.mode == Globals.WRONG_WAY_TO_IMPLEMENT_IT :
            self.localGlobalsApiFilePath = f'{Globals.BASE_API_PATH}{Globals.LOCAL_GLOBALS_API_PATH}'
            self.baseApiPath = f'{self.backSlash.join(self.currentPath.split(self.localGlobalsApiFilePath)[-2].split(self.backSlash)[:-1])}{self.backSlash}'
            self.apisPath = f'{self.backSlash.join(self.currentPath.split(self.localGlobalsApiFilePath)[-2].split(self.backSlash)[:-2])}{self.backSlash}'

            self.apisTree = self.getPathTreeFromPath(self.apisPath)
            self.makePathTreeVisible(self.apisPath)

            if self.printStatus :
                print(f'''                {self.__class__.__name__} = {self}
                {self.__class__.__name__}.currentPath =                 {self.currentPath}
                {self.__class__.__name__}.localPath =                   {self.localPath}
                {self.__class__.__name__}.baseApiPath =                 {self.baseApiPath}
                {self.__class__.__name__}.localGlobalsApiFilePath =     {self.localGlobalsApiFilePath}
                {self.__class__.__name__}.apisPath =                    {self.apisPath}
                {self.__class__.__name__}.extension =                   {self.extension}\n''')
                self.printTree(self.apisTree,'Apis tree')

    def getApiPath(self,apiName):
        return f'{self.localPath}{self.apisRoot}{apiName}{self.backSlash}{self.baseApiPath}'

    def update(self) :
        self.updateApplicationDependencies()
        self.updateGlobalsClassFile()
        self.makeApisAvaliable()

    def makeApisAvaliable(self) :
        self.apisTree = {}
        for apiName in self.apiNameList :
            try :
                apiTree = self.makePathTreeVisible(self.getApiPath(apiName))
                self.apisTree[apiName] = apiTree
            except Exception as exception :
                self.debug(f'Not possible to make {apiName} api avaliable{Globals.NEW_LINE}{str(exception)}')
        if self.printStatus :
            self.printTree(apiTree,'Api tree')

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
            if not len(node.split(charactere)) == 1 :
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

    def lineAproved(self,settingLine) :
        approved = True
        if Globals.NEW_LINE == settingLine  :
            approved = False
        if Globals.HASH_TAG in settingLine :
            filteredSettingLine = self.filterString(settingLine)
            if None == filteredSettingLine or Globals.NOTHING == filteredSettingLine or Globals.NEW_LINE == filteredSettingLine :
                approved = False
        return approved

    def getSettingTree(self,settingFilePath=None) :
        if not settingFilePath :
            settingFilePath = f'{self.apiPath}{self.baseApiPath}{Globals.RESOURCE_BACK_SLASH}{self.globalsApiName}.{Globals.EXTENSION}'
        with open(settingFilePath,Globals.READ,encoding=Globals.ENCODING) as settingsFile :
            allSettingLines = settingsFile.readlines()
        longStringCapturing = False
        quoteType = None
        longStringList = None
        depth = 0
        depthPass = None
        nodeRefference = 0
        nodeKey = Globals.NOTHING
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
        if self.apiName not in settingTree.keys() :
            try :
                self.concatenateTree(f'{self.apiPath}{self.baseApiPath}{Globals.RESOURCE_BACK_SLASH}{self.apiName}.{self.accessTree(AttributeKey.getKeyByClassNameAndKey(Globals,AttributeKey.API_EXTENSION),settingTree)}',settingTree)
            except Exception as exception :
                self.debug(f'Not possible to get api properties tree{Globals.NEW_LINE}{str(exception)}')
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
            self.debug(f'Not possible to get {nodeKey}{Globals.NEW_LINE}{str(exception)}')
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
            values.append(self.getValue(value))
        return values

    def getTuple(self,value):
        roughtValues = value[1:-1].split(Globals.COMA)
        values = []
        for value in roughtValues :
            values.append(self.getValue(value))
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

    def printTree(self,tree,name):
        depth = 0
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

    def updateApplicationDependencies(self):
        try :
            if self.getApiSetting(AttributeKey.DEPENDENCY_UPDATE) :
                import subprocess
                moduleList = self.getApiSetting(AttributeKey.DEPENDENCY_LIST)
                if moduleList :
                    subprocess.Popen(Globals.UPDATE_PIP_INSTALL).wait()
                    for module in moduleList :
                        subprocess.Popen(f'{Globals.PIP_INSTALL} {module}').wait()
                resourceModuleList = self.getApiSetting(AttributeKey.DEPENDENCY_RESOURCE_LIST)
                if resourceModuleList :
                    for resourceModule in resourceModuleList :
                        command = f'{Globals.PIP_INSTALL} {resourceModule}'
                        processPath = f'{self.getApiPath(self.apiName)}{Globals.RESOURCE_BACK_SLASH}'
                        subprocess.Popen(command,shell=True,cwd=processPath).wait()
                        ###- subprocess.run(command,shell=True,capture_output=True,cwd=processPath)
        except :
            pass

    def getGlobalsPrintStatus(self):
        return self.getSetting(AttributeKey.getKeyByClassNameAndKey(Globals,AttributeKey.PRINT_STATUS))

    def getGlobalsApiList(self):
        return self.getSetting(AttributeKey.getKeyByClassNameAndKey(Globals,AttributeKey.GLOBALS_API_LIST))

    def getUpdateGlobalsClassFile(self):
        return self.getSetting(AttributeKey.getKeyByClassNameAndKey(Globals,AttributeKey.UPDATE_GLOBALS))

    def updateGlobalsClassFile(self):
        if self.updateGlobals and self.updateGlobals.__class__.__name__ == Globals.BOOLEAN :
            try :
                globalsScript = []
                with open(self.globalsApiPath,Globals.READ,encoding = Globals.ENCODING) as globalsFile :
                    for line in globalsFile :
                        globalsScript.append(line)
                for apiName in self.apiNameList :
                    updatingApiPath =f'{self.getApiPath(apiName)}{self.localGlobalsApiFilePath}'
                    if apiName != self.globalsApiName :
                        with open(updatingApiPath,Globals.OVERRIDE,encoding = Globals.ENCODING) as globalsFile :
                            globalsFile.write(''.join(globalsScript))
            except Exception as exception :
                self.debug(f'Not possible to update Globals {Globals.NEW_LINE}{str(exception)}')
                if self.printStatus :
                    print(f'''Globals api wans't found in your directory. {self.__class__.__name__} may not work properly in some edge cases''')

    def getExtension(self):
        return self.extension

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

    def debug(self,string):
        if self.debugStatus :
            print(f'{Globals.DEBUG}{string}')
