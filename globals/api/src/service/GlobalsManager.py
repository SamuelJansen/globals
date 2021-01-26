import subprocess, site, importlib
from pathlib import Path
from python_helper import Constant as c
from python_helper import log, StringHelper, SettingHelper, EnvironmentHelper, ObjectHelper

global GLOBALS
GLOBALS = None

DEFAULT_LOG_STATUS = False
DEFAULT_SUCCESS_STATUS = False
DEFAULT_SETTING_STATUS = False
DEFAULT_DEBUG_STATUS = False
DEFAULT_WARNING_STATUS = False
DEFAULT_FAILURE_STATUS = False
DEFAULT_WRAPPER_STATUS = False
DEFAULT_ERROR_STATUS = False
DEFAULT_TEST_STATUS = False

APPLICATION = 'application'

IGNORE_MODULE_LIST = []
IGNORE_REOURCE_LIST = []

class Globals:

    OS_SEPARATOR = EnvironmentHelper.OS_SEPARATOR
    ENCODING = c.ENCODING
    OVERRIDE = c.OVERRIDE
    READ = c.READ

    PYTHON_EXTENSION = 'py'
    EXTENSION = 'yml'
    LOCAL_CONFIGURATION_FILE_NAME = f'local-config{c.DOT}{EXTENSION}'

    API_BACK_SLASH = f'api{OS_SEPARATOR}'
    SRC_BACK_SLASH = f'src{OS_SEPARATOR}'
    BASE_API_PATH = f'{API_BACK_SLASH}{SRC_BACK_SLASH}'

    RESOURCE_BACK_SLASH = f'resource{OS_SEPARATOR}'
    REPOSITORY_BACK_SLASH = f'repository{OS_SEPARATOR}'
    DEPENDENCY_BACK_SLASH = f'dependency{OS_SEPARATOR}'

    TOKEN_PIP_USER = '__TOKEN_PIP_USER__'
    SPACE_PIP_USER = f'{c.SPACE}--user'
    PIP_INSTALL = f'python -m pip install --upgrade{TOKEN_PIP_USER} --force-reinstall'
    UPDATE_PIP_INSTALL = f'python -m pip install --upgrade{TOKEN_PIP_USER} pip'

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
    OPEN_SET = '{'
    OPEN_DICTIONARY = '{'

    SAFE_AMOUNT_OF_TRIPLE_SINGLE_OR_DOUBLE_QUOTES_PLUS_ONE = 4

    LIB = 'lib'
    STATIC_PACKAGE_PATH = f'{OS_SEPARATOR}statics'
    TOKEN_PYTHON_VERSION = '__TOKEN_PYTHON_VERSION__'
    HEROKU_PYTHON = f'{OS_SEPARATOR}lib{OS_SEPARATOR}python{TOKEN_PYTHON_VERSION}{OS_SEPARATOR}site-packages'

    def __init__(self, filePath,
        loadLocalConfig = True,
        settingsFileName = APPLICATION,
        logStatus = DEFAULT_LOG_STATUS,
        successStatus = DEFAULT_SUCCESS_STATUS,
        settingStatus = DEFAULT_SETTING_STATUS,
        debugStatus = DEFAULT_DEBUG_STATUS,
        warningStatus = DEFAULT_WARNING_STATUS,
        failureStatus = DEFAULT_FAILURE_STATUS,
        wrapperStatus = DEFAULT_WRAPPER_STATUS,
        errorStatus = DEFAULT_ERROR_STATUS,
        testStatus = DEFAULT_TEST_STATUS,
        encoding = c.ENCODING,
        printRootPathStatus = False,
        globalsEverything = False
    ):

        if globalsInstanceIsNone() :

            self.filePath = filePath
            self.charactereFilterList = Globals.CHARACTERE_FILTER
            self.nodeIgnoreList = Globals.NODE_IGNORE_LIST
            self.encoding = encoding

            self.loadLocalConfiguration(
                loadLocalConfig,
                settingsFileName,
                logStatus,
                successStatus,
                settingStatus,
                debugStatus,
                warningStatus,
                failureStatus,
                wrapperStatus,
                errorStatus,
                testStatus,
                printRootPathStatus,
                globalsEverything
            )

            self.setting(f'{self.__class__.__name__}{c.DOT}filePath: {self.filePath}')
            self.setting(f'__file__: {__file__}')

            self.buildApplicationPath()

            self.defaultSettingTree = self.getDefaultSettingTree()
            self.settingTree = self.getSettingTree()
            self.staticPackage = self.getStaticPackagePath()
            self.apiName = self.getApiName()
            self.extension = self.getExtension()

            self.printStatus = self.getSetting(AttributeKey.PRINT_STATUS)
            self.apiNameList = self.getSetting(AttributeKey.GLOBALS_API_LIST)

            if self.printStatus :
                print(f'''            {self.__class__.__name__}: {self}
                {self.__class__.__name__}.staticPackage:    {self.staticPackage}
                {self.__class__.__name__}.currentPath:      {self.currentPath}
                {self.__class__.__name__}.localPath:        {self.localPath}
                {self.__class__.__name__}.baseApiPath:      {self.baseApiPath}
                {self.__class__.__name__}.apiPath:          {self.apiPath}
                {self.__class__.__name__}.apisRoot:         {self.apisRoot}
                {self.__class__.__name__}.apisPath:         {self.apisPath}
                {self.__class__.__name__}.apiPackage:       {self.apiPackage}
                {self.__class__.__name__}.apiName:          {self.apiName}
                {self.__class__.__name__}.extension:        {self.extension}\n''')

                self.printTree(self.settingTree,f'{self.__class__.__name__} settings tree')

            self.updateDependencyStatus = self.getSetting(AttributeKey.DEPENDENCY_UPDATE)
            self.rootPathTree = {}
            self.update()

    def loadLocalConfiguration(
        self,
        loadLocalConfig,
        settingsFileName,
        logStatus,
        successStatus,
        settingStatus,
        debugStatus,
        warningStatus,
        failureStatus,
        wrapperStatus,
        errorStatus,
        testStatus,
        printRootPathStatus,
        globalsEverything
    ) :
        self.logStatus = EnvironmentHelper.update(log.LOG, logStatus, default=DEFAULT_LOG_STATUS)
        self.successStatus = EnvironmentHelper.update(log.SUCCESS, successStatus, default=DEFAULT_SUCCESS_STATUS)
        self.settingStatus = EnvironmentHelper.update(log.SETTING, settingStatus, default=DEFAULT_SETTING_STATUS)
        self.debugStatus = EnvironmentHelper.update(log.DEBUG, debugStatus, default=DEFAULT_DEBUG_STATUS)
        self.warningStatus = EnvironmentHelper.update(log.WARNING, warningStatus, default=DEFAULT_WARNING_STATUS)
        self.failureStatus = EnvironmentHelper.update(log.FAILURE, failureStatus, default=DEFAULT_FAILURE_STATUS)
        self.wrapperStatus = EnvironmentHelper.update(log.WRAPPER, wrapperStatus, default=DEFAULT_WRAPPER_STATUS)
        self.errorStatus = EnvironmentHelper.update(log.ERROR, errorStatus, default=DEFAULT_ERROR_STATUS)
        self.testStatus = EnvironmentHelper.update(log.TEST, testStatus, default=DEFAULT_TEST_STATUS)
        self.loadLocalConfig = loadLocalConfig
        self.localConfiguration = {}
        if self.loadLocalConfig :
            try :
                self.localConfiguration = self.getSettingTree(settingFilePath=Globals.LOCAL_CONFIGURATION_FILE_NAME,settingTree=None)
            except Exception as exception :
                log.log(self.__class__,f'Failed to load {Globals.LOCAL_CONFIGURATION_FILE_NAME} settings', exception=exception)
            keyQuery = SettingHelper.querySetting(AttributeKey.KW_KEY,self.localConfiguration)
            keyValueQuery = {}
            for key,value in keyQuery.items() :
                KW_DOT_KEY = f'{c.DOT}{AttributeKey.KW_KEY}'
                if key.endswith(KW_DOT_KEY) :
                    environmentInjection = SettingHelper.getSetting(key[:-len(KW_DOT_KEY)], self.localConfiguration)
                    if (
                        ObjectHelper.isDictionary(environmentInjection) and
                        AttributeKey.KW_KEY in environmentInjection and
                        AttributeKey.KW_VALUE in environmentInjection and
                        2 == len(environmentInjection)
                    ):
                        EnvironmentHelper.update(environmentInjection[AttributeKey.KW_KEY], environmentInjection[AttributeKey.KW_VALUE])
        log.loadSettings()
        self.settingsFileName = self.getSettingsFileName(settingsFileName)
        self.printRootPathStatus = printRootPathStatus
        self.globalsEverything = globalsEverything
        self.ignoreModuleList = IGNORE_MODULE_LIST
        self.ignoreResourceList = IGNORE_REOURCE_LIST
        if ObjectHelper.isNotEmpty(self.localConfiguration) and SettingHelper.getSetting('print-status', self.localConfiguration) :
            SettingHelper.printSettings(self.localConfiguration,"Local Configuration")
            basicSettingsAsDictionary = {
                'activeEnvironment' : self.activeEnvironment,
                'settingsFileName' : self.settingsFileName,
                'defaultSettingFileName' : self.defaultSettingFileName,
                'successStatus' : self.successStatus,
                'settingStatus' : self.settingStatus,
                'debugStatus' : self.debugStatus,
                'warningStatus' : self.warningStatus,
                'failureStatus' : self.failureStatus,
                'errorStatus' : self.errorStatus,
                'logStatus' : self.logStatus,
                'globalsEverything' : self.globalsEverything,
                'printRootPathStatus' : self.printRootPathStatus
            }
            log.prettyPython(self.__class__, f'Basic settings', basicSettingsAsDictionary, logLevel=log.SETTING)

    def getSettingsFileName(self, settingsFileName) :
        self.defaultSettingFileName = settingsFileName
        self.activeEnvironment = SettingHelper.getActiveEnvironment()
        if SettingHelper.DEFAULT_ENVIRONMENT == self.activeEnvironment :
            return settingsFileName
        else :
            return f'{settingsFileName}{c.DASH}{self.activeEnvironment}'

    def buildApplicationPath(self):
        if ObjectHelper.isNotEmpty(self.filePath) :
            self.currentPath = f'{str(Path(self.filePath).parent.absolute())}{self.OS_SEPARATOR}'
        else :
            self.currentPath = f'{str(Path(__file__).parent.absolute())}{self.OS_SEPARATOR}'
        self.log(f'{self.__class__.__name__}{c.DOT}filePath: {self.filePath}')
        self.log(f'{self.__class__.__name__}{c.DOT}currentPath: {self.currentPath}')

        self.localPath = str(Path.home())
        if not self.localPath[-1] == str(self.OS_SEPARATOR) :
            self.localPath = f'{self.localPath}{self.OS_SEPARATOR}'
        self.log(f'{self.__class__.__name__}{c.DOT}localPath: {self.localPath}')

        self.baseApiPath = Globals.BASE_API_PATH
        self.apiPath = self.currentPath.split(self.baseApiPath)[0]
        self.log(f'{self.__class__.__name__}{c.DOT}apiPath: {self.apiPath}')

        lastLocalPathPackage = self.localPath.split(self.OS_SEPARATOR)[-2]
        firstBaseApiPath = self.baseApiPath.split(self.OS_SEPARATOR)[0]
        lastLocalPathPackageNotFound = True
        self.apiPackage = c.NOTHING
        for currentPackage in self.currentPath.split(self.OS_SEPARATOR) :
            if lastLocalPathPackageNotFound :
                if currentPackage == lastLocalPathPackage :
                    lastLocalPathPackageNotFound = False
            elif not currentPackage or currentPackage == firstBaseApiPath :
                break
            else :
                self.apiPackage = currentPackage
        self.log(f'{self.__class__.__name__}{c.DOT}apiPackage: {self.apiPackage}')

        if StringHelper.isNotBlank(self.apiPackage) :
            if len(self.currentPath.split(self.localPath)[1].split(self.apiPackage)) > 1:
                self.apisRoot = self.currentPath.split(self.localPath)[1].split(self.apiPackage)[0]
            self.apisPath = f'{self.currentPath.split(self.apiPackage)[0]}'
        else :
            self.apisRoot = c.NOTHING
            self.apisPath = c.NOTHING
        self.log(f'{self.__class__.__name__}{c.DOT}apisRoot: {self.apisRoot}')
        self.log(f'{self.__class__.__name__}{c.DOT}apisPath: {self.apisPath}')


    def getApiPath(self,apiPackageName):
        if not apiPackageName == c.NOTHING :
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
        self.spotRootPath(self.localPath)

    def makeApiAvaliable(self,apiPackageName) :
        self.apiTree = {}
        try :
            apiPath = self.getApiPath(apiPackageName)
            self.apiTree[apiPackageName] = self.makePathTreeVisible(self.getApiPath(apiPackageName))
        except Exception as exception :
            self.error(f'Not possible to make {apiPackageName} api avaliable',exception)
        if self.printStatus :
            self.printTree(self.apiTree,'Api tree')

    def makeApisAvaliable(self,apisPath):
        if self.globalsEverything :
            try :
                apiPackageList = EnvironmentHelper.listDirectoryContent(apisPath)
                for apiPackage in apiPackageList :
                    if not apiPackage in list(self.apiTree.keys()) :
                        self.apiTree[apiPackage] = self.makePathTreeVisible(f'{apisPath}{apiPackage}')
                if self.printStatus :
                    self.printTree(self.apiTree,f'{c.DEBUG}Api tree (globalsEverithing is active)')
            except Exception as exception :
                self.error(f'Not possible to run makeApisAvaliable({apisPath}) rotine',exception)

    def spotRootPath(self,rootPath) :
        if self.printRootPathStatus :
            try :
                apiPackageList = EnvironmentHelper.listDirectoryContent(rootPath)
                for apiPackage in apiPackageList :
                    self.rootPathTree[apiPackage] = self.addNode(f'{rootPath}{apiPackage}')
                if self.printStatus :
                    self.printTree(self.rootPathTree,f'{c.DEBUG}Root tree (printRootPathStatus is active)')
            except Exception as exception :
                self.error(f'Not possible to run spotRootPath({rootPath}) rotine',exception)

    def giveLocalVisibilityToFrameworkApis(self,apiPackageNameList):
        if apiPackageNameList :
            localPackageNameList = EnvironmentHelper.listDirectoryContent(self.apisPath)
            for packageName in localPackageNameList :
                if packageName not in self.apiTree.keys() and packageName in apiPackageNameList :
                    packagePath = f'{self.apisPath}{packageName}'
                    try :
                        self.apiTree[packageName] = self.makePathTreeVisible(packagePath)
                    except :
                        self.apiTree[packageName] = c.NOTHING
            if self.printStatus :
                self.printTree(self.apiTree,f'{c.DEBUG}Api tree')

    def makePathTreeVisible(self,path):
        node = {}
        nodeSons = EnvironmentHelper.listDirectoryContent(path)
        for nodeSon in nodeSons :
            if self.nodeIsValid(nodeSon) :
                nodeSonPath = f'{path}{self.OS_SEPARATOR}{nodeSon}'
                try :
                    node[nodeSon] = self.makePathTreeVisible(nodeSonPath)
                except :
                    node[nodeSon] = c.NOTHING
        EnvironmentHelper.appendPath(path)
        return node

    def addNode(self,nodePath):
        node = {}
        try :
            nodeSons = EnvironmentHelper.listDirectoryContent(nodePath)
            for nodeSon in nodeSons :
                nodeSonPath = f'{nodePath}{self.OS_SEPARATOR}{nodeSon}'
                try :
                    node[nodeSon] = self.addNode(nodeSonPath)
                except :
                    node[nodeSon] = c.NOTHING
        except Exception as exception :
            self.error(f'Not possible to run addNode({nodePath}) rotine',exception)
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
        nodeSons = EnvironmentHelper.listDirectoryContent(path)
        for nodeSon in nodeSons :
            if self.nodeIsValid(nodeSon) :
                nodeSonPath = f'{path}{self.OS_SEPARATOR}{nodeSon}'
                try :
                    node[nodeSon] = self.getPathTreeFromPath(nodeSonPath)
                except : pass
        return node

    def overrideApiTree(self,apiName,package=None):
        if package :
            actualPackage = package + self.OS_SEPARATOR
        else :
            actualPackage = apiName + self.OS_SEPARATOR
        self.apiName = apiName
        self.apiPackage = package
        self.apiPath = f'{self.apisPath}{actualPackage}'
        self.defaultSettingTree = self.getDefaultSettingTree()
        settingFilePath = f'{self.apiPath}{Globals.API_BACK_SLASH}{Globals.RESOURCE_BACK_SLASH}{self.settingsFileName}.{Globals.EXTENSION}'
        self.settingTree = self.getSettingTree(settingFilePath=settingFilePath,settingTree=self.settingTree)

    def getDefaultSettingTree(self) :
        defaultSettingFilePath = f'{self.apiPath}{Globals.API_BACK_SLASH}{Globals.RESOURCE_BACK_SLASH}{self.defaultSettingFileName}.{Globals.EXTENSION}'
        return self.getSettingTree(settingFilePath=defaultSettingFilePath)

    def getSettingTree(self,settingFilePath=None,settingTree=None) :
        if not settingFilePath :
            settingFilePath = f'{self.apiPath}{Globals.API_BACK_SLASH}{Globals.RESOURCE_BACK_SLASH}{self.settingsFileName}.{Globals.EXTENSION}'
        settingTree = None
        try :
            settingTree = SettingHelper.getSettingTree(settingFilePath, keepDepthInLongString=True, fallbackSettingTree=self.defaultSettingTree)
        except :
            settingTree = SettingHelper.getSettingTree(settingFilePath, keepDepthInLongString=True)
        return settingTree

    def addTree(self,settingFilePath):
        newSetting = self.getSettingTree(settingFilePath=settingFilePath)
        for settingKey,settingValue in newSetting.items() :
            self.settingTree[settingKey] = settingValue

    def getApiSetting(self,nodeKey):
        return self.getSetting(nodeKey)

    def getSetting(self,nodeKey,settingTree=None) :
        if not settingTree :
            settingTree = self.settingTree
        settingValue = SettingHelper.getSetting(nodeKey,self.settingTree)
        if ObjectHelper.isEmpty(settingValue) or {} == settingValue :
            return SettingHelper.getSetting(nodeKey,self.defaultSettingTree)
        return settingValue

    def accessTree(self,nodeKey,tree) :
        return SettingHelper.getSetting(nodeKey,tree)

    def printTree(self,tree,name,depth=1):
        SettingHelper.printSettings(tree, name, depth=depth)

    def updateDependencies(self):
        try :
            if self.updateDependencyStatus :
                moduleList = self.getSetting(AttributeKey.DEPENDENCY_LIST_WEB)
                localPackageNameList = self.getSetting(AttributeKey.DEPENDENCY_LIST_LOCAL)
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
            return f'{tryOrder}{c.SPACE}{LOG_COMMAND}{c.COLON_SPACE}{command}'
        def getResponseLog(tryOrder,command,response):
            logResponse = f'{tryOrder}{c.SPACE}{LOG_COMMAND}{c.COLON_SPACE}{command}'
            logResponse = f'{logResponse}{c.SPACE_DASH_SPACE}{LOG_RESPONSE}{c.COLON_SPACE}'
            if 1 == response :
                return f'{logResponse}{LOG_FAIL}'
            elif 0 == response :
                return f'{logResponse}{LOG_SUCCESS}'
            else :
                return f'{logResponse}{response}'
        commandFirstTry = command.replace(self.TOKEN_PIP_USER,self.SPACE_PIP_USER)
        self.debug(getCommandLog(LOG_FIRST_TRY,commandFirstTry))
        responseFirstTry = KW_DIDNT_RUN
        try :
            responseFirstTry = subprocess.Popen(commandFirstTry).wait()
            self.debug(getResponseLog(LOG_FIRST_TRY,commandFirstTry,responseFirstTry))
        except Exception as exceptionFirstTry :
            self.error(f'{commonExceptionMessage}',exceptionFirstTry)
        if KW_DIDNT_RUN == responseFirstTry or 1 == responseFirstTry :
            commandSecondTry = command.replace(self.TOKEN_PIP_USER,c.NOTHING)
            self.debug(getCommandLog(LOG_SECOND_TRY,commandSecondTry))
            responseSecondTry = KW_DIDNT_RUN
            try :
                responseSecondTry = subprocess.Popen(commandSecondTry).wait()
                self.debug(getResponseLog(LOG_SECOND_TRY,commandSecondTry,responseSecondTry))
            except Exception as exceptionSecondTry :
                self.error(f'{commonExceptionMessage}',exceptionSecondTry)
            if KW_DIDNT_RUN == responseFirstTry and KW_DIDNT_RUN == responseSecondTry :
                log.error(self.__class__,f'Not possible to run {commandFirstTry}',Exception(f'Both attempt failed'))

    def getApiName(self):
        try :
            return self.getSetting(AttributeKey.API_NAME)
        except Exception as exception :
            self.failure('Not possible to get api name', exception)

    def getExtension(self):
        extension = Globals.EXTENSION
        try :
            extension = self.getSetting(AttributeKey.API_EXTENSION)
        except Exception as exception :
            self.failure('Not possible to get api extenion. Returning default estension', exception)
        return extension

    def getStaticPackagePath(self) :
        staticPackageList = site.getsitepackages()
        self.log(f'Static packages list: {StringHelper.prettyJson(staticPackageList)}. Picking the first one')
        staticPackage = str(staticPackageList[0])
        staticPackage = staticPackage.replace(f'{c.BACK_SLASH}{c.BACK_SLASH}',Globals.OS_SEPARATOR)
        staticPackage = staticPackage.replace(c.BACK_SLASH,Globals.OS_SEPARATOR)
        staticPackage = staticPackage.replace(f'{c.SLASH}{c.SLASH}',Globals.OS_SEPARATOR)
        staticPackage = staticPackage.replace(c.SLASH,Globals.OS_SEPARATOR)
        if staticPackage[-1] == str(Globals.OS_SEPARATOR) :
            staticPackage = staticPackage[:-1]
        herokuPythonLibPath = Globals.HEROKU_PYTHON.replace(Globals.TOKEN_PYTHON_VERSION, str(self.getSetting(AttributeKey.PYTHON_VERSION)))
        if staticPackage.endswith(herokuPythonLibPath) :
            staticPackage = staticPackage.replace(herokuPythonLibPath,c.NOTHING)
        staticPackage = f'{staticPackage}{Globals.STATIC_PACKAGE_PATH}'
        self.setting(f'Static package: "{staticPackage}"')
        return staticPackage

    def log(self,message,exception=None):
        if c.TRUE == self.logStatus :
            log.log(self.__class__,message,exception=exception)

    def debug(self,message):
        if c.TRUE == self.debugStatus :
            log.debug(self.__class__,message)

    def warning(self,message):
        if c.TRUE == self.warningStatus :
            log.warning(self.__class__,message)

    def error(self,message,exception):
        if c.TRUE == self.errorStatus :
            log.error(self.__class__,message,exception)

    def success(self,message):
        if c.TRUE == self.successStatus :
            log.success(self.__class__,message)

    def failure(self,message,exception):
        if c.TRUE == self.failureStatus :
            log.failure(self.__class__,message,exception)

    def setting(self,message):
        if c.TRUE == self.settingStatus :
            log.setting(self.__class__,message)

def newGlobalsInstance(*args, **kwargs) :
    global GLOBALS
    if globalsInstanceIsNone() :
        GLOBALS = Globals(*args, **kwargs)
        log.setting(newGlobalsInstance, f'Returning new {GLOBALS} globals instance')
    else :
        log.setting(updateGlobalsInstance, f'Returning existing {GLOBALS} globals instance')
    return GLOBALS

def getGlobalsInstance() :
    global GLOBALS
    return GLOBALS

def updateGlobalsInstance(globalsInstance) :
    global GLOBALS
    if globalsInstanceIsNone() :
        GLOBALS = globalsInstance
        log.setting(updateGlobalsInstance, f'Updatting {GLOBALS} globals instance')
    else :
        log.setting(updateGlobalsInstance, f'Returning existing {GLOBALS} globals instance')
    return GLOBALS

def hardUpdateGlobalsInstance(globalsInstance) :
    global GLOBALS
    GLOBALS = globalsInstance
    log.setting(updateGlobalsInstance, f'Updatting {GLOBALS} globals instance')
    return GLOBALS

def eraseGlobalsInstance() :
    global GLOBALS
    GLOBALS = None

def globalsInstanceIsNone():
    return ObjectHelper.isNone(getGlobalsInstance())

def globalsInstanceIsNotNone():
    return not globalsInstanceIsNone()

class AttributeKey:

    KW_KEY = 'key'
    KW_VALUE = 'value'

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
    PYTHON_VERSION = 'python.version'

    def getKey(api,key):
        return f'{Globals.__name__}.{key}'

    def getKeyByClassNameAndKey(cls,key):
        return f'{cls.__name__}.{key}'

def importModule(resourceModuleName, muteLogs=False, ignoreList=IGNORE_MODULE_LIST) :
    if resourceModuleName not in ignoreList :
        module = None
        try :
            module = importlib.import_module(resourceModuleName)
        except Exception as exception:
            if not muteLogs :
                log.warning(importResource, f'Not possible to import "{resourceModuleName}" module. Going for a second attempt', exception=exception)
            try :
                module = __import__(resourceModuleName)
            except :
                if not muteLogs :
                    log.error(importResource, f'Not possible to import "{resourceModuleName}" module in the second attempt either. Returning "{module}" by default', exception)
        return module

def importResource(resourceName, resourceModuleName=None, muteLogs=False, ignoreList=IGNORE_REOURCE_LIST) :
    if resourceName not in ignoreList :
        if ObjectHelper.isEmpty(resourceModuleName) :
            resourceModuleName = resourceName
        module = importModule(resourceModuleName, muteLogs=False)
        if module :
            resource = None
            try :
                resource = getattr(module, resourceName)
            except Exception as exception :
                if not muteLogs :
                    log.error(importResource, f'Not possible to import "{resourceName}" resource from "{resourceModuleName}" module', exception=exception)
            return resource

def runBeforeTest(instanceList) :
    log.prettyPython(runBeforeTest, f'{getGlobalsInstance()} in comparrison to globals instance list', instanceList, logLevel=log.LOG)
    instanceList.append(getGlobalsInstance())
    log.prettyPython(runBeforeTest, f'{getGlobalsInstance()} in comparrison to globals instance list', instanceList, logLevel=log.LOG)
    eraseGlobalsInstance()
    log.prettyPython(runBeforeTest, f'{getGlobalsInstance()} in comparrison to globals instance list', instanceList, logLevel=log.LOG)

def runAfterTest(instanceList) :
    log.prettyPython(runAfterTest, f'{getGlobalsInstance()} in comparrison to globals instance list', instanceList, logLevel=log.LOG)
    previousGlobalsInstance = instanceList.pop()
    log.prettyPython(runAfterTest, f'{getGlobalsInstance()} in comparrison to globals instance list', instanceList, logLevel=log.LOG)
    eraseGlobalsInstance()
    log.prettyPython(runAfterTest, f'{getGlobalsInstance()} in comparrison to globals instance list', instanceList, logLevel=log.LOG)
    hardUpdateGlobalsInstance(previousGlobalsInstance)
    log.prettyPython(runAfterTest, f'{getGlobalsInstance()} in comparrison to globals instance list', instanceList, logLevel=log.LOG)
