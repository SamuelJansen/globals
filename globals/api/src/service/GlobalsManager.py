import subprocess, site, importlib
from pathlib import Path
from python_helper import Constant as c
from python_helper import log, StringHelper, SettingHelper, EnvironmentHelper, ObjectHelper, ReflectionHelper

global GLOBALS
GLOBALS = None

DEFAULT_LOG_STATUS = False
DEFAULT_INFO_STATUS = False
DEFAULT_STATUS_STATUS = False
DEFAULT_SUCCESS_STATUS = False
DEFAULT_SETTING_STATUS = False
DEFAULT_DEBUG_STATUS = False
DEFAULT_WARNING_STATUS = False
DEFAULT_FAILURE_STATUS = False
DEFAULT_WRAPPER_STATUS = False
DEFAULT_ERROR_STATUS = False
DEFAULT_TEST_STATUS = False

DEFAULT_LOGS_WITH_COLORS = False

APPLICATION = 'application'

DOT_SPACE_CHECK_LOG_LEVEL_LOGS_FOR_MORE_INFORMATION = f'{c.DOT_SPACE}Check {log.LOG} level logs for more information'

IGNORE_MODULES = list()
IGNORE_REOURCES = list()


globals = globals


class Globals:

    OS_SEPARATOR = EnvironmentHelper.OS_SEPARATOR
    ENCODING = c.ENCODING
    OVERRIDE = c.OVERRIDE
    READ = c.READ

    PYTHON_EXTENSION = 'py'
    EXTENSION = 'yml'
    LOCAL_CONFIGURATION_FILE_NAME = f'local-config{c.DOT}{EXTENSION}'

    API_BACK_SLASH = f'api{EnvironmentHelper.OS_SEPARATOR}'
    SRC_BACK_SLASH = f'src{EnvironmentHelper.OS_SEPARATOR}'
    BASE_API_PATH = f'{API_BACK_SLASH}{SRC_BACK_SLASH}'

    RESOURCE_BACK_SLASH = f'resource{EnvironmentHelper.OS_SEPARATOR}'
    REPOSITORY_BACK_SLASH = f'repository{EnvironmentHelper.OS_SEPARATOR}'
    DEPENDENCY_BACK_SLASH = f'dependency{EnvironmentHelper.OS_SEPARATOR}'

    TOKEN_PIP_USER = '__TOKEN_PIP_USER__'
    SPACE_PIP_USER = f'{c.SPACE}--user'
    PIP_INSTALL = f'python -m pip install --upgrade{TOKEN_PIP_USER} --force-reinstall'
    UPDATE_PIP_INSTALL = f'python -m pip install --upgrade{TOKEN_PIP_USER} pip'

    CHARACTER_FILTER = [
        '__'
    ]

    NODE_IGNORE_LIST = [
        '.git',
        'distribution',
        'dist',
        '__pycache__',
        '__init__',
        '__main__',
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

    STATIC_PACKAGE_PATH = f'{EnvironmentHelper.OS_SEPARATOR}api{EnvironmentHelper.OS_SEPARATOR}resource'

    def __init__(self, filePath,
        loadLocalConfig = True,
        settingsFileName = APPLICATION,
        logStatus = DEFAULT_LOG_STATUS,
        infoStatus = DEFAULT_INFO_STATUS,
        statusStatus = DEFAULT_STATUS_STATUS,
        successStatus = DEFAULT_SUCCESS_STATUS,
        settingStatus = DEFAULT_SETTING_STATUS,
        debugStatus = DEFAULT_DEBUG_STATUS,
        warningStatus = DEFAULT_WARNING_STATUS,
        failureStatus = DEFAULT_FAILURE_STATUS,
        wrapperStatus = DEFAULT_WRAPPER_STATUS,
        errorStatus = DEFAULT_ERROR_STATUS,
        testStatus = DEFAULT_TEST_STATUS,
        logsWithColors = DEFAULT_LOGS_WITH_COLORS,
        encoding = c.ENCODING,
        printRootPathStatus = False,
        globalsEverything = False
    ):

        if globalsInstanceIsNone():

            self.logsWithColors = EnvironmentHelper.update(log.ENABLE_LOGS_WITH_COLORS, logsWithColors or log.colorsEnabled(), default=DEFAULT_LOGS_WITH_COLORS)

            self.logStatus = EnvironmentHelper.update(log.LOG, logStatus, default=DEFAULT_LOG_STATUS)
            self.infoStatus = EnvironmentHelper.update(log.INFO, infoStatus, default=DEFAULT_INFO_STATUS)
            self.statusStatus = EnvironmentHelper.update(log.STATUS, statusStatus, default=DEFAULT_STATUS_STATUS)
            self.successStatus = EnvironmentHelper.update(log.SUCCESS, successStatus, default=DEFAULT_SUCCESS_STATUS)
            self.settingStatus = EnvironmentHelper.update(log.SETTING, settingStatus, default=DEFAULT_SETTING_STATUS)
            self.debugStatus = EnvironmentHelper.update(log.DEBUG, debugStatus, default=DEFAULT_DEBUG_STATUS)
            self.warningStatus = EnvironmentHelper.update(log.WARNING, warningStatus, default=DEFAULT_WARNING_STATUS)
            self.failureStatus = EnvironmentHelper.update(log.FAILURE, failureStatus, default=DEFAULT_FAILURE_STATUS)
            self.wrapperStatus = EnvironmentHelper.update(log.WRAPPER, wrapperStatus, default=DEFAULT_WRAPPER_STATUS)
            self.errorStatus = EnvironmentHelper.update(log.ERROR, errorStatus, default=DEFAULT_ERROR_STATUS)
            self.testStatus = EnvironmentHelper.update(log.TEST, testStatus, default=DEFAULT_TEST_STATUS)
            log.loadSettings()

            self.filePath = filePath
            self.characterFilterList = Globals.CHARACTER_FILTER
            self.nodeIgnoreList = Globals.NODE_IGNORE_LIST
            self.encoding = encoding

            self.loadLocalConfiguration(loadLocalConfig, printRootPathStatus, globalsEverything)

            self.setting(f'{self.__class__.__name__}{c.DOT}filePath: {self.filePath}')
            self.setting(f'__file__: {__file__}')

            self.buildApplicationPath()
            self.loadSettings(settingsFileName)
            self.update()

    def loadSettings(self, settingsFileName):
        self.settingsFileName = self.getSettingsFileName(settingsFileName)
        self.defaultSettingTree = self.getDefaultSettingTree()
        self.settingTree = self.getEnvironmentSettingTree(defaultSettingFilePath=self.defaultSettingFilePath)

        self.staticPackage = self.getStaticPackagePath()
        self.apiName = self.getApiName()
        self.apiNameList = self.getSetting(AttributeKey.GLOBALS_API_LIST)

        self.extension = self.getExtension()
        self.printStatus = self.getSetting(AttributeKey.PRINT_STATUS)
        self.printStatusOnScreen()

        self.updateDependencyStatus = self.getSetting(AttributeKey.DEPENDENCY_UPDATE)
        self.rootPathTree = {}

    def loadLocalConfiguration(self, loadLocalConfig, printRootPathStatus, globalsEverything):
        self.loadLocalConfig = loadLocalConfig
        self.localConfiguration = {}
        if self.loadLocalConfig :
            try :
                self.localConfiguration = self.getSettingTree(settingFilePath=Globals.LOCAL_CONFIGURATION_FILE_NAME,settingTree=None)
            except Exception as exception :
                self.log(f'Failed to load {Globals.LOCAL_CONFIGURATION_FILE_NAME} settings', exception=exception)
            keyQuery = SettingHelper.querySetting(AttributeKey.KW_KEY,self.localConfiguration)
            keyValueQuery = {}
            for key,value in keyQuery.items():
                KW_DOT_KEY = f'{c.DOT}{AttributeKey.KW_KEY}'
                if key.endswith(KW_DOT_KEY):
                    environmentInjection = SettingHelper.getSetting(key[:-len(KW_DOT_KEY)], self.localConfiguration)
                    if (
                        ObjectHelper.isDictionary(environmentInjection) and
                        AttributeKey.KW_KEY in environmentInjection and
                        AttributeKey.KW_VALUE in environmentInjection and
                        2 == len(environmentInjection)
                    ):
                        EnvironmentHelper.update(environmentInjection[AttributeKey.KW_KEY], environmentInjection[AttributeKey.KW_VALUE])
        log.loadSettings()
        self.printRootPathStatus = printRootPathStatus
        self.globalsEverything = globalsEverything
        self.ignoreModules = IGNORE_MODULES
        self.ignoreResources = IGNORE_REOURCES
        self.activeEnvironment = SettingHelper.getActiveEnvironment()
        if ObjectHelper.isNotEmpty(self.localConfiguration) and SettingHelper.getSetting('print-status', self.localConfiguration):
            SettingHelper.printSettings(self.localConfiguration,"Local Configuration")
            basicSettingsAsDictionary = {
                'activeEnvironment' : self.activeEnvironment,
                'successStatus' : self.successStatus,
                'settingStatus' : self.settingStatus,
                'debugStatus' : self.debugStatus,
                'warningStatus' : self.warningStatus,
                'failureStatus' : self.failureStatus,
                'errorStatus' : self.errorStatus,
                'wrapperStatus': self.wrapperStatus,
                'infoStatus' : self.infoStatus,
                'statusStatus' : self.statusStatus,
                'logStatus' : self.logStatus,
                'globalsEverything' : self.globalsEverything,
                'printRootPathStatus' : self.printRootPathStatus
            }
            log.prettyPython(self.__class__, f'Basic settings', basicSettingsAsDictionary, logLevel=log.SETTING)

    def getSettingsFileName(self, settingsFileName):
        self.defaultSettingFileName = settingsFileName
        if SettingHelper.DEFAULT_ENVIRONMENT == self.activeEnvironment :
            return settingsFileName
        else :
            return f'{settingsFileName}{c.DASH}{self.activeEnvironment}'

    def buildApplicationPath(self):
        if ObjectHelper.isNotEmpty(self.filePath):
            self.currentPath = f'{str(Path(self.filePath).parent.absolute())}{EnvironmentHelper.OS_SEPARATOR}'
        else :
            self.currentPath = f'{str(Path(__file__).parent.absolute())}{EnvironmentHelper.OS_SEPARATOR}'
        self.log(f'{self.__class__.__name__}{c.DOT}filePath: {self.filePath}')
        self.log(f'{self.__class__.__name__}{c.DOT}currentPath: {self.currentPath}')

        self.localPath = str(Path.home())
        if not self.localPath[-1] == str(EnvironmentHelper.OS_SEPARATOR):
            self.localPath = f'{self.localPath}{EnvironmentHelper.OS_SEPARATOR}'
        self.log(f'{self.__class__.__name__}{c.DOT}localPath: {self.localPath}')

        self.baseApiPath = Globals.BASE_API_PATH
        self.apiPath = self.currentPath.split(self.baseApiPath)[0]
        self.log(f'{self.__class__.__name__}{c.DOT}apiPath: {self.apiPath}')

        lastLocalPathPackage = self.localPath.split(EnvironmentHelper.OS_SEPARATOR)[-2]
        firstBaseApiPath = self.baseApiPath.split(EnvironmentHelper.OS_SEPARATOR)[0]
        lastLocalPathPackageNotFound = True
        self.apiPackage = c.NOTHING
        for currentPackage in self.currentPath.split(EnvironmentHelper.OS_SEPARATOR):
            if lastLocalPathPackageNotFound :
                if currentPackage == lastLocalPathPackage :
                    lastLocalPathPackageNotFound = False
            elif not currentPackage or currentPackage == firstBaseApiPath :
                break
            else :
                self.apiPackage = currentPackage
        self.log(f'{self.__class__.__name__}{c.DOT}apiPackage: {self.apiPackage}')

        if StringHelper.isNotBlank(self.apiPackage):
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
             return f'{self.localPath}{self.apisRoot}{apiPackageName}{EnvironmentHelper.OS_SEPARATOR}'###-'{self.baseApiPath}'
        if self.apisPath :
            return self.apisPath
        if self.localPath :
            return self.localPath
        return f'{EnvironmentHelper.OS_SEPARATOR}'

    def update(self):
        self.updateDependencies()
        self.makeApiAvaliable(self.apiPackage)
        self.makeApisAvaliable(self.apisPath)
        self.spotRootPath(self.localPath)

    def makeApiAvaliable(self,apiPackageName):
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
                    if not apiPackage in list(self.apiTree.keys()):
                        self.apiTree[apiPackage] = self.makePathTreeVisible(f'{apisPath}{apiPackage}')
                if self.printStatus :
                    self.printTree(self.apiTree,f'{c.DEBUG}Api tree (globalsEverithing is active)')
            except Exception as exception :
                self.error(f'Not possible to run makeApisAvaliable({apisPath}) rotine',exception)

    def spotRootPath(self,rootPath):
        if self.printRootPathStatus :
            try :
                apiPackageList = EnvironmentHelper.listDirectoryContent(rootPath)
                for apiPackage in apiPackageList :
                    self.rootPathTree[apiPackage] = self.addNode(f'{rootPath}{apiPackage}')
                if self.printStatus :
                    self.printTree(self.rootPathTree,f'{c.DEBUG}Root tree (printRootPathStatus is active)')
            except Exception as exception :
                self.failure(f'Not possible to run spotRootPath({rootPath}) rotine', exception)

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
            if self.nodeIsValid(nodeSon):
                nodeSonPath = f'{path}{EnvironmentHelper.OS_SEPARATOR}{nodeSon}'
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
                nodeSonPath = f'{nodePath}{EnvironmentHelper.OS_SEPARATOR}{nodeSon}'
                try :
                    node[nodeSon] = self.addNode(nodeSonPath)
                except :
                    node[nodeSon] = c.NOTHING
        except Exception as exception :
            self.failure(f'Not possible to run addNode({nodePath}) rotine', exception, muteStackTrace=True)
        return node

    def nodeIsValid(self,node):
        return self.nodeIsValidByFilter(node) and (node not in self.nodeIgnoreList)

    def nodeIsValidByFilter(self,node):
        for character in self.characterFilterList :
            if not len(node.split(character)) == 1 :
                return False
        return True

    def getPathTreeFromPath(self,path):
        node = {}
        nodeSons = EnvironmentHelper.listDirectoryContent(path)
        for nodeSon in nodeSons :
            if self.nodeIsValid(nodeSon):
                nodeSonPath = f'{path}{EnvironmentHelper.OS_SEPARATOR}{nodeSon}'
                try :
                    node[nodeSon] = self.getPathTreeFromPath(nodeSonPath)
                except : pass
        return node

    def overrideApiTree(self,apiName,package=None):
        if package :
            actualPackage = package + EnvironmentHelper.OS_SEPARATOR
        else :
            actualPackage = apiName + EnvironmentHelper.OS_SEPARATOR
        self.apiName = apiName
        self.apiPackage = package
        self.apiPath = f'{self.apisPath}{actualPackage}'
        self.defaultSettingTree = self.getDefaultSettingTree()
        self.settingTree = self.getEnvironmentSettingTree(defaultSettingFilePath=self.defaultSettingFilePath, settingTree=self.getSettings())

    def getDefaultSettingTree(self):
        self.defaultSettingFilePath = f'{self.apiPath}{Globals.API_BACK_SLASH}{Globals.RESOURCE_BACK_SLASH}{self.defaultSettingFileName}{c.DOT}{Globals.EXTENSION}'
        return self.getSettingTree(settingFilePath=self.defaultSettingFilePath)

    def getEnvironmentSettingTree(self, defaultSettingFilePath=None, settingTree=None):
        self.settingFilePath = f'{self.apiPath}{Globals.API_BACK_SLASH}{Globals.RESOURCE_BACK_SLASH}{self.settingsFileName}{c.DOT}{Globals.EXTENSION}'
        return self.getSettingTree(settingFilePath=self.settingFilePath, defaultSettingFilePath=defaultSettingFilePath, settingTree=settingTree)

    def getSettingTree(self, settingFilePath=None, defaultSettingFilePath=None, settingTree=None):
        if ObjectHelper.isEmpty(settingTree):
            settingTree = {}
        fallbackSettingFilePath = defaultSettingFilePath if not settingFilePath == defaultSettingFilePath else None
        if (
            ObjectHelper.isNeitherNoneNorBlank(fallbackSettingFilePath) and (
                ObjectHelper.isNoneOrBlank(settingFilePath) or
                not EnvironmentHelper.OS.path.isfile(settingFilePath)
            )
        ):
            self.log(f'The "{settingFilePath}" setting file path was not found. Trying to get it from fallback setting tree', exception=None)
            return self.getSettingTree(settingFilePath=fallbackSettingFilePath, settingTree=settingTree)
        try :
            settingTree = SettingHelper.getSettingTree(settingFilePath, fallbackSettingFilePath=fallbackSettingFilePath, fallbackSettingTree=settingTree, keepDepthInLongString=True)
        except Exception as exception :
            if ObjectHelper.isNone(fallbackSettingFilePath):
                ###- self.error(f'Failed to load setting tree from "{settingFilePath}" setting file path. Returning {settingTree} by default', exception)
                self.log(f'Failed to load setting tree from "{settingFilePath}" setting file path. Returning current setting tree by default', exception=exception)
            else :
                self.log(f'Failed to load setting tree from "{settingFilePath}" setting file path and "{fallbackSettingFilePath}" default setting file path. Only setting file path will be loadded now', exception=exception)
                try :
                    settingTree = SettingHelper.getSettingTree(settingFilePath, keepDepthInLongString=True)
                except Exception as innerException :
                    # self.failure(f'Failed to load setting tree from "{settingFilePath}" setting file path as well. Returning {settingTree} by default', exception)
                    self.failure(f'Failed to load setting tree from "{settingFilePath}" setting file path as well. Returning current setting tree by default', exception=exception)
        return settingTree

    def addTree(self,settingFilePath):
        newSetting = self.getSettingTree(settingFilePath=settingFilePath)
        for settingKey,settingValue in newSetting.items():
            self.getSettings()[settingKey] = settingValue

    def getApiSetting(self,nodeKey):
        return self.getSetting(nodeKey)

    def getSetting(self,nodeKey,settingTree=None):
        resolvedSettingTree = self.getSettingsOrDefault(settingTree)
        settingValue = SettingHelper.getSetting(nodeKey, resolvedSettingTree)
        if ObjectHelper.isEmpty(settingValue):
            return SettingHelper.getSetting(nodeKey, self.defaultSettingTree)
        return settingValue

    def getSettings(self):
        return self.settingTree

    def getSettingsOrDefault(self, settingTree):
        return settingTree if ObjectHelper.isNotNone(settingTree) else self.getSettings()

    def accessTree(self,nodeKey,tree):
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
        apiName = None
        try :
            apiName = self.getSetting(AttributeKey.API_NAME)
        except Exception as exception :
            self.warning(f'Not possible to get api name. Returning {apiName} by default', exception=exception)
        return apiName

    def getExtension(self):
        extension = Globals.EXTENSION
        try :
            extension = self.getSetting(AttributeKey.API_EXTENSION)
        except Exception as exception :
            self.warning(f'Not possible to get api extenion. Returning {extension} by default', exception=exception)
        return extension

    def getStaticPackagePath(self):
        staticPackage = self.getSetting(AttributeKey.PYTHON_STATIC_PACKAGE)
        self.log(f'User static package: "{site.getusersitepackages()}"')
        self.log(f'Static package list: {StringHelper.prettyJson(site.getsitepackages())}')
        self.log(f'Static package (taken from application.yml): "{staticPackage}"')
        if ObjectHelper.isNone(staticPackage):
            staticPackage = str(self.STATIC_PACKAGE_PATH)
        self.setting(f'Static package: "{staticPackage}"')
        return staticPackage

    def log(self,message,exception=None):
        if c.TRUE == self.logStatus :
            log.log(self.__class__,message,exception=exception)

    def info(self,message,exception=None):
        if c.TRUE == self.infoStatus :
            log.info(self.__class__,message,exception=exception)

    def status(self,message,exception=None):
        if c.TRUE == self.statusStatus :
            log.status(self.__class__,message,exception=exception)

    def debug(self,message):
        if c.TRUE == self.debugStatus :
            log.debug(self.__class__,message)

    def warning(self, message, exception=None):
        if c.TRUE == self.warningStatus :
            log.warning(self.__class__, message, exception=exception)

    def error(self,message,exception):
        if c.TRUE == self.errorStatus :
            log.error(self.__class__,message,exception)

    def success(self,message):
        if c.TRUE == self.successStatus :
            log.success(self.__class__,message)

    def failure(self,message,exception, muteStackTrace=False):
        if c.TRUE == self.failureStatus :
            log.failure(self.__class__, message, exception, muteStackTrace=muteStackTrace)

    def setting(self,message):
        if c.TRUE == self.settingStatus :
            log.setting(self.__class__,message)

    def printStatusOnScreen(self):
        if self.printStatus :
            print(f'''            {self.__class__.__name__}: {self}
            {self.__class__.__name__}.staticPackage: ---------- {self.staticPackage}
            {self.__class__.__name__}.currentPath: ------------ {self.currentPath}
            {self.__class__.__name__}.localPath: -------------- {self.localPath}
            {self.__class__.__name__}.baseApiPath: ------------ {self.baseApiPath}
            {self.__class__.__name__}.apiPath: ---------------- {self.apiPath}
            {self.__class__.__name__}.apisRoot: --------------- {self.apisRoot}
            {self.__class__.__name__}.apisPath: --------------- {self.apisPath}
            {self.__class__.__name__}.apiPackage: ------------- {self.apiPackage}
            {self.__class__.__name__}.apiName: ---------------- {self.apiName}
            {self.__class__.__name__}.extension: -------------- {self.extension}
            {self.__class__.__name__}.settingFilePath: -------- {self.settingFilePath}
            {self.__class__.__name__}.defaultSettingFilePath: - {self.defaultSettingFilePath}\n''')
            self.printTree(self.getSettings(),f'{self.__class__.__name__} settings tree')

def newGlobalsInstance(*args, muteLogs=False, **kwargs):
    global GLOBALS
    if globalsInstanceIsNone(muteLogs=muteLogs):
        GLOBALS = Globals(*args, **kwargs)
        if not muteLogs :
            log.setting(newGlobalsInstance, f'Returning new {GLOBALS} globals instance')
    else :
        if not muteLogs :
            log.setting(newGlobalsInstance, f'Returning existing {GLOBALS} globals instance')
    return GLOBALS

def getGlobalsInstance(muteLogs=False):
    global GLOBALS
    return GLOBALS

def updateGlobalsInstance(globalsInstance, muteLogs=False):
    global GLOBALS
    if globalsInstanceIsNone(muteLogs=muteLogs):
        oldGlobals = str(GLOBALS)
        GLOBALS = globalsInstance
        if not muteLogs :
            log.setting(updateGlobalsInstance, f'Replacing {oldGlobals} globals instance by {GLOBALS} globals instance')
    else :
        if not muteLogs :
            log.setting(updateGlobalsInstance, f'Returning existing {GLOBALS} globals instance')
    return GLOBALS

def hardUpdateGlobalsInstance(globalsInstance, muteLogs=False):
    global GLOBALS
    oldGlobals = str(GLOBALS)
    GLOBALS = globalsInstance
    if not muteLogs :
        log.setting(hardUpdateGlobalsInstance, f'Hard replacing {oldGlobals} globals instance by {GLOBALS} globals instance')
    return GLOBALS

def eraseGlobalsInstance(muteLogs=False):
    global GLOBALS
    oldGlobals = str(GLOBALS)
    GLOBALS = None
    if not muteLogs :
        log.setting(eraseGlobalsInstance, f'Erasing {oldGlobals} globals instance. It is now {GLOBALS}')

def globalsInstanceIsNone(muteLogs=False):
    return ObjectHelper.isNone(getGlobalsInstance(muteLogs=muteLogs))

def globalsInstanceIsNotNone(muteLogs=False):
    return not globalsInstanceIsNone(muteLogs=muteLogs)

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

    GLOBALS_API_LIST = f'{KW_API}{c.DOT}{KW_LIST}'

    API_NAME = f'{KW_API}{c.DOT}{KW_NAME}'
    API_EXTENSION = f'{KW_API}{c.DOT}{KW_EXTENSION}'
    UPDATE_GLOBALS = f'{KW_UPDATE}-globals'
    PRINT_STATUS = 'print-status'
    DEPENDENCY_UPDATE = f'{KW_API}{c.DOT}{KW_DEPENDENCY}{c.DOT}{KW_UPDATE}'
    DEPENDENCY_LIST_WEB = f'{KW_API}{c.DOT}{KW_DEPENDENCY}{c.DOT}{KW_LIST}{c.DOT}{KW_WEB}'
    DEPENDENCY_LIST_LOCAL = f'{KW_API}{c.DOT}{KW_DEPENDENCY}{c.DOT}{KW_LIST}{c.DOT}{KW_LOCAL}'
    DEPENDENCY_RESOURCE_LIST = f'{KW_API}{c.DOT}{KW_DEPENDENCY}{c.DOT}{KW_LIST}{c.DOT}{KW_LOCAL}'
    PYTHON = 'python'
    PYTHON_VERSION = f'{PYTHON}{c.DOT}version'
    PYTHON_STATIC_PACKAGE = f'{PYTHON}{c.DOT}static-package'

    def getKey(api,key):
        return f'{Globals.__name__}{c.DOT}{key}'

    def getKeyByClassNameAndKey(cls,key):
        return f'{cls.__name__}{c.DOT}{key}'

def getResourceNameList(resourceNameList):
    return resourceNameList if ObjectHelper.isList(resourceNameList) else [resourceNameList]

def getResourceName(resourceName):
    return resourceName if not c.DOT in resourceName else getResourceNameList(resourceName.split(c.DOT))[0]

def getInnerResourceNameList(resourceName, resourceModuleName):
    if not resourceName == resourceModuleName :
        resourceNameList = getResourceNameList(resourceName.split(c.DOT))
        return [resourceNameList[0]] if 1 == len(resourceNameList) or resourceNameList[1] is None else resourceNameList
    return [resourceName]


IMPORT_CACHE = {}


def getCachedImports():
    return {*IMPORT_CACHE}


def clearCachedImports():
    IMPORT_CACHE = {}


def importModule(resourceModuleName, muteLogs=False, reload=False, ignoreList=IGNORE_MODULES, required=False):
    if resourceModuleName not in ignoreList :
        importException = None
        try :
            if reload :
                IMPORT_CACHE[resourceModuleName] = importlib.reload(resourceModuleName)
            elif (
                resourceModuleName not in IMPORT_CACHE or
                required and ObjectHelper.isNone(IMPORT_CACHE.get(resourceModuleName))
            ):
                IMPORT_CACHE[resourceModuleName] = importlib.import_module(resourceModuleName)
        except Exception as exception:
            importException = exception
            if not muteLogs :
                log.log(importModule, f'Not possible to import "{resourceModuleName}" module. Going for a second attempt', exception=exception)
            try :
                IMPORT_CACHE[resourceModuleName] = __import__(resourceModuleName)
            except Exception as innerException:
                importException = innerException
                IMPORT_CACHE[resourceModuleName] = None
                if not muteLogs :
                    log.log(importModule, f'Not possible to import "{resourceModuleName}" module in the second attempt either. Original cause: {str(exception)}. Returning "{IMPORT_CACHE.get(resourceModuleName)}" by default', exception=innerException)
        if required and ObjectHelper.isNone(IMPORT_CACHE.get(resourceModuleName)):
            if not importException:
                try:
                    IMPORT_CACHE[resourceModuleName] = __import__(resourceModuleName)
                    return IMPORT_CACHE.get(resourceModuleName)
                except Exception as exception:
                    importException = exception
            dotSpaceCause = f'{c.DOT_SPACE_CAUSE}{getExceptionTextWithoutDotAtTheEnd(importException)}'
            raise Exception(f'Not possible to import module "{resourceModuleName}"{dotSpaceCause}{c.BLANK if dotSpaceCause.endswith(DOT_SPACE_CHECK_LOG_LEVEL_LOGS_FOR_MORE_INFORMATION) else DOT_SPACE_CHECK_LOG_LEVEL_LOGS_FOR_MORE_INFORMATION}')
        return IMPORT_CACHE.get(resourceModuleName)


def importResource(resourceName, resourceModuleName=None, muteLogs=False, reload=False, ignoreList=IGNORE_REOURCES, required=False):
    innerResourceName = getResourceName(resourceName)
    if innerResourceName not in ignoreList :
        resource = None
        importException = None
        if ObjectHelper.isNone(resourceModuleName):
            resourceModuleName = innerResourceName
        if (
            reload or
            resourceModuleName not in IMPORT_CACHE or
            required and ObjectHelper.isNone(IMPORT_CACHE.get(resourceModuleName))
        ):
            IMPORT_CACHE[resourceModuleName] = importModule(resourceModuleName, muteLogs=muteLogs, reload=reload, required=required)
        if ObjectHelper.isNone(IMPORT_CACHE.get(resourceModuleName)):
            if required:
                raise Exception(f'Could not import module "{resourceModuleName}"')
            return
        nameList = []
        try :
            accumulatedResourceModule = IMPORT_CACHE.get(resourceModuleName)
            for name in getInnerResourceNameList(resourceName, resourceModuleName):
                nameList.append(name)
                if reload:
                    accumulatedResourceModule = ReflectionHelper.getAttributeOrMethod(accumulatedResourceModule, name)
                    IMPORT_CACHE[getCompositeModuleName(resourceModuleName, nameList)] = accumulatedResourceModule
                elif getCompositeModuleName(resourceModuleName, nameList) in IMPORT_CACHE:
                    accumulatedResourceModule = IMPORT_CACHE.get(getCompositeModuleName(resourceModuleName, nameList))
                elif ReflectionHelper.hasAttributeOrMethod(accumulatedResourceModule, name):
                    accumulatedResourceModule = ReflectionHelper.getAttributeOrMethod(accumulatedResourceModule, name)
                    IMPORT_CACHE[getCompositeModuleName(resourceModuleName, nameList)] = accumulatedResourceModule
        except Exception as exception:
            importException = exception
            IMPORT_CACHE[getCompositeModuleName(resourceModuleName, nameList)] = None
            if not muteLogs :
                log.log(importResource, f'Not possible to import "{resourceName}" resource from "{resourceModuleName}" module', exception=exception)
        if required and ObjectHelper.isNone(accumulatedResourceModule):
            dotSpaceCause = f'{c.DOT_SPACE_CAUSE}{getExceptionTextWithoutDotAtTheEnd(importException)}'
            raise Exception(f'Error while importing {innerResourceName} resource from {resourceModuleName} module{dotSpaceCause}{c.BLANK if dotSpaceCause.endswith(DOT_SPACE_CHECK_LOG_LEVEL_LOGS_FOR_MORE_INFORMATION) else DOT_SPACE_CHECK_LOG_LEVEL_LOGS_FOR_MORE_INFORMATION}')
        return IMPORT_CACHE.get(getCompositeModuleName(resourceModuleName, nameList))


def getCompositeModuleName(resourceModuleName, resourceNameList):
    return StringHelper.join([resourceModuleName, *resourceNameList], character=c.DOT)


def getExceptionTextWithoutDotAtTheEnd(exception):
    if ObjectHelper.isNone(exception):
        return "Unknown"
    exceptionText = str(exception)
    while ObjectHelper.isNeitherNoneNorBlank(exceptionText) and c.DOT == exceptionText[-1]:
        exceptionText = exceptionText[:-1]
    return exceptionText


def runBeforeTest(instanceList, logLevel=log.LOG, muteLogs=True):
    log.prettyPython(runBeforeTest, f'{getGlobalsInstance(muteLogs=muteLogs)} in comparrison to globals instance list', instanceList, condition=not muteLogs, logLevel=logLevel)
    instanceList.append(getGlobalsInstance(muteLogs=muteLogs))
    log.prettyPython(runBeforeTest, f'{getGlobalsInstance(muteLogs=muteLogs)} in comparrison to globals instance list', instanceList, condition=not muteLogs, logLevel=logLevel)
    eraseGlobalsInstance(muteLogs=muteLogs)
    log.prettyPython(runBeforeTest, f'{getGlobalsInstance(muteLogs=muteLogs)} in comparrison to globals instance list', instanceList, condition=not muteLogs, logLevel=logLevel)

def runAfterTest(instanceList, logLevel=log.LOG, muteLogs=True):
    log.prettyPython(runAfterTest, f'{getGlobalsInstance(muteLogs=muteLogs)} in comparrison to globals instance list', instanceList, condition=not muteLogs, logLevel=logLevel)
    previousGlobalsInstance = instanceList.pop()
    log.prettyPython(runAfterTest, f'{previousGlobalsInstance} previous globals instance in comparrison to globals instance list', instanceList, condition=not muteLogs, logLevel=logLevel)
    eraseGlobalsInstance(muteLogs=muteLogs)
    log.prettyPython(runAfterTest, f'{getGlobalsInstance(muteLogs=muteLogs)} in comparrison to globals instance list', instanceList, condition=not muteLogs, logLevel=logLevel)
    hardUpdateGlobalsInstance(previousGlobalsInstance, muteLogs=muteLogs)
    log.prettyPython(runAfterTest, f'{getGlobalsInstance(muteLogs=muteLogs)} in comparrison to globals instance list', instanceList, condition=not muteLogs, logLevel=logLevel)
