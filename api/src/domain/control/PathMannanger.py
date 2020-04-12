import os, sys
from pathlib import Path
clear = lambda: os.system('cls')

print('PathMannanger library imported')

class PathMannanger:

    BASE_API_PATH = 'api\\src\\'
    LOCAL_GLOBALS_API_PATH = 'domain\\control\\'

    EXTENSION = 'gbl'
    PYTHON_EXTENSION = 'py'

    ENCODING = 'utf-8'
    OVERRIDE = 'w+'
    READ = 'r'

    GLOBALS_NAME = 'Globals'

    DEFAULT_SETTINGS = 'Globals.api.list'

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

    ### There are 'places' where backslash is not much wellcome
    ### Having it stored into a variable helps a lot
    BACK_SLASH = '\\'
    HASH_TAG = '#'
    COLON = ':'
    COMA = ','
    SPACE = ' '
    DOT = '.'
    NEW_LINE = '\n'
    NOTHING = ''

    WRONG_WAY_TO_MAKE_IT_WORKS = 'WRONG_WAY_TO_MAKE_IT_WORKS'
    PROPER_WAY_TO_MAKE_IT_WORKS = 'PROPER_WAY_TO_MAKE_IT_WORKS'

    def __init__(self,
        mode = PROPER_WAY_TO_MAKE_IT_WORKS,
        globalsApis = DEFAULT_SETTINGS,
        encoding = ENCODING,
        printStatus = False
    ):

        clear() # or simply os.system('cls')

        self.mode = mode
        self.backSlash = PathMannanger.BACK_SLASH

        self.charactereFilterList = PathMannanger.CHARACTERE_FILTER
        self.nodeIgnoreList = PathMannanger.NODE_IGNORE_LIST
        self.extension = PathMannanger.EXTENSION

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
            self.settingTree = self.getSettingTree()
            self.apiNames = self.accessTree(globalsApis,self.settingTree)

            self.globalsApiName = PathMannanger.GLOBALS_NAME
            self.localGlobalsApiFilePath = f'{PathMannanger.LOCAL_GLOBALS_API_PATH}{PathMannanger.__name__}.{PathMannanger.PYTHON_EXTENSION}'
            self.globalsApiPath = f'{self.getApiPath(self.globalsApiName)}{self.localGlobalsApiFilePath}'
            self.apisPath = f'{self.backSlash.join(self.currentPath.split(self.localGlobalsApiFilePath)[-1].split(self.backSlash)[:-2])}{self.backSlash}'


            try : extension = self.accessTree(settings,self.settingTree)
            except : extension = PathMannanger.NOTHING
            if self.printStatus :
                print(f'{self.apiName}.extension = {extension}')


            if not PathMannanger.NOTHING == extension :
                self.extension = extension

            if self.printStatus :
                print(f'''                {self.__class__.__name__} = {self}
                {self.__class__.__name__}.currentPath =                 {self.currentPath}
                {self.__class__.__name__}.localPath =                   {self.localPath}
                {self.__class__.__name__}.baseApiPath =                 {self.baseApiPath}
                {self.__class__.__name__}.apiPath =                     {self.apiPath}
                {self.__class__.__name__}.apiName =                     {self.apiName}
                {self.__class__.__name__}.apisRoot =                    {self.apisRoot}
                {self.__class__.__name__}.apiNames =                    {self.apiNames}
                {self.__class__.__name__}.localGlobalsApiFilePath =     {self.localGlobalsApiFilePath}
                {self.__class__.__name__}.globalsApiName =              {self.globalsApiName}
                {self.__class__.__name__}.globalsApiPath =              {self.globalsApiPath}
                {self.__class__.__name__}.apisPath =                    {self.apisPath}
                {self.__class__.__name__}.extension =                   {self.extension}\n''')


            self.update()

        elif self.mode == PathMannanger.WRONG_WAY_TO_MAKE_IT_WORKS :
            self.localGlobalsApiFilePath = f'{PathMannanger.BASE_API_PATH}{PathMannanger.LOCAL_GLOBALS_API_PATH}'
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
                self.printTree(self.apisTree)

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
        self.apisTree = []
        for apiName in self.apiNames :
            apiTree = self.makePathTreeVisible(self.getApiPath(apiName))
            apiTree = {apiName:apiTree}
            self.apisTree.append(apiTree)
        if self.printStatus :
            print(f'{self.__class__.__name__}.apisTree:')
            for apiTree in self.apisTree :
                print()
                self.printTree(apiTree)
            print()

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

    def getExtension(self):
        return self.extension

    def getSettings(self,path,settingKey) :
        with open(path,'r',encoding='utf-8') as settingsFile :
            allSettingLines = settingsFile.readlines()
        for line, settingLine in enumerate(allSettingLines) :
            depth = getDepth(settingLine)
            setingKeyLine = getAttributeKey(settingLine)
            if settingKey == setingKeyLine :
                settingValue = getAttibuteValue(settingLine)
                if self.printStatus :
                    print(f'''key : value --> {settingKey} : {settingValue}''')
                return settingValue

    def getSettingTree(self) :

        settingFilePath = f'{self.apiPath}{self.baseApiPath}resource\\{self.apiName}.{PathMannanger.EXTENSION}'
        with open(settingFilePath,'r',encoding='utf-8') as settingsFile :
            allSettingLines = settingsFile.readlines()

        depth = 0
        depthPass = None
        nodeRefference = 0
        nodeKey = ''
        settingTree = {}
        for line, settingLine in enumerate(allSettingLines) :
            # print(f'\nbegin of line {line}')
            currentDepth = getDepth(settingLine)
            # print(f'currentDepth = {currentDepth}')

            if not settingLine == PathMannanger.NEW_LINE :
                if currentDepth == depth :
                    # print(f'    getSettingTree(): {currentDepth} == {depth} --> {currentDepth == depth}')
                    settinKey,settingValue = self.getAttributeKeyValue(settingLine)
                    nodeKey = self.updateSettingTreeAndReturnNodeKey(nodeKey,settingTree,settinKey,settingValue)

                elif currentDepth > depth :
                    if not depthPass :
                        depthPass = currentDepth - depth
                    # print(f'    getSettingTree(): {currentDepth} > {depth} --> {currentDepth > depth}')
                    currentNodeRefference = currentDepth // (currentDepth - depth)
                    # print(f'    getSettingTree(): {currentNodeRefference} = {currentDepth} // ({currentDepth} - {depth})')

                    # print(f'    getSettingTree(): {currentNodeRefference} - {nodeRefference} == 1 = {currentNodeRefference - nodeRefference == 1}')
                    if currentNodeRefference - nodeRefference == 1 :
                        settinKey,settingValue = self.getAttributeKeyValue(settingLine)
                        nodeKey = self.updateSettingTreeAndReturnNodeKey(nodeKey,settingTree,settinKey,settingValue)
                        nodeRefference = currentNodeRefference
                        depth = currentDepth


                elif currentDepth < depth :
                    # print('======================================================================================')
                    # print(f'    getSettingTree(): {currentDepth} < {depth} --> {currentDepth < depth}')

                    nodeRefference = currentDepth // depthPass
                    # print(f'    getSettingTree(): {nodeRefference} = {currentDepth} // {depthPass}')

                    # print(f'    getSettingTree(): nodeRefference = {nodeRefference}, depthPass = {depthPass}')

                    depth = currentDepth
                    # print(f'depth = {depth}')

                    splitedNodeKey = nodeKey.split(PathMannanger.DOT)[:nodeRefference]
                    # print(f'    getSettingTree(): splitedNodeKey = {splitedNodeKey}')

                    # print(f'    getSettingTree(): len(splitedNodeKey) = {len(splitedNodeKey)}, len({splitedNodeKey}) == 0 = {len(splitedNodeKey) == 0}')
                    splitedNodeKeyLength = len(splitedNodeKey)

                    # print(f'    getSettingTree(): {splitedNodeKeyLength} == 0 --> {splitedNodeKeyLength == 0}')
                    if splitedNodeKeyLength == 0 :
                        nodeKey = PathMannanger.NOTHING
                    elif splitedNodeKeyLength == 1 :
                        nodeKey = splitedNodeKey[0]
                    else :
                        nodeKey = PathMannanger.DOT.join(splitedNodeKey)

                    # print(f'    getSettingTree(): nodeKey = {nodeKey}')

                    settinKey,settingValue = self.getAttributeKeyValue(settingLine)
                    nodeKey = self.updateSettingTreeAndReturnNodeKey(nodeKey,settingTree,settinKey,settingValue)
                    depth = currentDepth

                    # print('======================================================================================')

            # print(f'    getSettingTree(): settingTree = {settingTree}')
            # print(f'end of line {line}\n')

        if self.printStatus :
            print(f'{self.__class__.__name__}.settingTree: = {settingTree}')
            self.printTree(settingTree)
        return settingTree

    def printTree(self,tree):
        depth = 0
        self.printNodeTree(tree,depth)

    def printNodeTree(self,tree,depth):
        depthSpace = ''
        for nodeDeep in range(depth) :
            depthSpace += f'{PathMannanger.SPACE}{PathMannanger.SPACE}{PathMannanger.SPACE}'
        depth += 1
        for node in list(tree) :
            # print(f'tree[node] = {tree[node]}')
            # print(f'''{tree[node].__class__.__name__} == 'dict' = {tree[node].__class__.__name__ == 'dict'}''')
            if tree[node].__class__.__name__ == 'dict' :
                print(f'{depthSpace}{node}{PathMannanger.SPACE}{PathMannanger.COLON}')
                self.printNodeTree(tree[node],depth)
            else :
                print(f'{depthSpace}{node}{PathMannanger.SPACE}{PathMannanger.COLON}{PathMannanger.SPACE}{tree[node]}')

    def accessTree(self,nodeKey,tree) :
        # print(f'        accessTree(): nodeKey = {nodeKey}, tree = {tree}')
        if nodeKey == PathMannanger.NOTHING :
            return tree
        else :
            nodeKeyList = nodeKey.split(PathMannanger.DOT)
            lenNodeKeyList = len(nodeKeyList)
            if lenNodeKeyList > 0 and lenNodeKeyList == 1 :
                 nextNodeKey = PathMannanger.NOTHING
            else :
                nextNodeKey = PathMannanger.DOT.join(nodeKeyList[1:])
            # print(f'        accessTree(): nextNodeKey = {nextNodeKey}')
            # print(f'        accessTree(): nodeKeyList = {nodeKeyList}')
            # print(f'        accessTree(): tree[{nodeKeyList[0]}] = {tree[nodeKeyList[0]]}')
            return self.accessTree(nextNodeKey,tree[nodeKeyList[0]])

    def getAttributeKeyValue(self,settingLine):
        settinKey = getAttributeKey(settingLine)
        # print(f'    getAttributeKeyValue(): settinKey = {settinKey}')
        settingValue = getAttibuteValue(settingLine)
        # print(f'    getAttributeKeyValue(): settingValue = {settingValue}')
        return settinKey,settingValue

    def updateSettingTreeAndReturnNodeKey(self,nodeKey,settingTree,settinKey,settingValue):
        if settingValue :
            self.accessTree(nodeKey,settingTree)[settinKey] = settingValue
            # print(f'    updateSettingTreeAndReturnNodeKey: accessTree({nodeKey},{settingTree})[{settinKey}] = {self.accessTree(nodeKey,settingTree)[settinKey]}')
        else :
            self.accessTree(nodeKey,settingTree)[settinKey] = {}
            if PathMannanger.NOTHING == nodeKey :
                nodeKey += f'{settinKey}'
            else :
                nodeKey += f'{PathMannanger.DOT}{settinKey}'
        # print(f'    updateSettingTreeAndReturnNodeKey(): nodeKey = {nodeKey}')
        return nodeKey

def getDepth(settingLine):
    depthNotFount = True
    depth = 0
    while not settingLine[depth] == PathMannanger.NEW_LINE and depthNotFount:
        if settingLine[depth] == PathMannanger.SPACE:
            depth += 1
        else :
            depthNotFount = False
    return depth

def getAttributeKey(settingLine):
    possibleKey = filterString(settingLine)
    # print(f'      getAttributeKey({possibleKey}) = {possibleKey.strip().split(PathMannanger.HASH_TAG)[0].split(PathMannanger.COLON)[0].strip()}')
    return settingLine.strip().split(PathMannanger.HASH_TAG)[0].split(PathMannanger.COLON)[0].strip()

def getAttibuteValue(settingLine):
    possibleValue = filterString(settingLine)
    # print(f'''      getAttibuteValue({possibleValue}) = {getValue(':'.join(possibleValue.strip().split(PathMannanger.HASH_TAG)[0].split(PathMannanger.COLON)[1:]).strip())}''')
    return getValue(PathMannanger.COLON.join(possibleValue.strip().split(PathMannanger.HASH_TAG)[0].split(PathMannanger.COLON)[1:]).strip())

def filterString(string) :
    # print(f'''filterString({string}) = string[-1] = -->{string[-1]}<--, string[-1] == {PathMannanger.NEW_LINE} = {string[-1] == PathMannanger.NEW_LINE}''')
    if string[-1] == PathMannanger.NEW_LINE :
        string = string[:-1]
    string = string.strip()
    # print(f'filteredString = -->{string}<--')
    return string

def getValue(value) :
    # print(f'        getValue(): value = {value}')
    if value :
        if '[' == value[0] :
            # print(f'      getValue({value}) = {getList(value)}')
            return getList(value)
        elif '(' == value[0] :
            # print(f'      getValue({value}) = {getTuple(value)}')
            return getTuple(value)
        elif '{' == value[0] :
            # print(f'      getValue({value}) = {getDictionary(value)}')
            return getDictionary(value)
        try :
            # print(f'      getValue({value}) = {int(value)}')
            return int(value)
        except :
            try :
                # print(f'      getValue({value}) = {float(value)}')
                return float(value)
            except :
                # print(f'      getValue({value}) = {value}')
                return value

def getList(value):
    roughtValues = value[1:-1].split(PathMannanger.COMA)
    values = []
    for value in roughtValues :
        values.append(getValue(value))
    # print(f'      getList({value}) = {values}')
    return values

def getTuple(value):
    roughtValues = value[1:-1].split(PathMannanger.COMA)
    values = []
    for value in roughtValues :
        values.append(getValue(value))
    # print(f'        tupleValues = {values}')
    return tuple(values)

def getDictionary(value) :
    # print(f'         value = {value}')
    splitedValue = value[1:-1].split(PathMannanger.COLON)
    # print(f'         splitedValue = {splitedValue}')

    keyList = []
    for index in range(len(splitedValue) -1) :
        keyList.append(splitedValue[index].split(PathMannanger.COMA)[-1].strip())
    # print(f'         keyList = {keyList}')

    valueList = []
    valueListSize = len(splitedValue) -1
    for index in range(valueListSize) :
        if index == valueListSize -1 :
            correctValue = splitedValue[index+1].strip()
        else :
            correctValue = PathMannanger.COMA.join(splitedValue[index+1].split(PathMannanger.COMA)[:-1]).strip()
        # print(f'        correctValue = {correctValue}')
        valueList.append(getValue(correctValue))
    # print(f'         valueList = {valueList}')

    resultantDictionary = {}
    for index in range(len(keyList)) :
        resultantDictionary[keyList[index]] = valueList[index]

    return resultantDictionary
