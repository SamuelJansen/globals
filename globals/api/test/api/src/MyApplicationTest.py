from globals import Globals
import globals
from python_helper import EnvironmentVariable, SettingHelper, log, ObjectHelper
from python_helper import Constant as c

# LOG_HELPER_SETTINGS = {
#     log.LOG : False,
#     log.SUCCESS : False,
#     log.SETTING : False,
#     log.DEBUG : False,
#     log.WARNING : False,
#     log.WRAPPER : False,
#     log.FAILURE : False,
#     log.ERROR : False
# }

LOG_HELPER_SETTINGS = {
    log.LOG : True,
    log.SUCCESS : True,
    log.SETTING : True,
    log.DEBUG : True,
    log.WARNING : True,
    log.WRAPPER : True,
    log.FAILURE : True,
    log.ERROR : True
}

@EnvironmentVariable(environmentVariables={
        SettingHelper.ACTIVE_ENVIRONMENT : SettingHelper.LOCAL_ENVIRONMENT,
        **LOG_HELPER_SETTINGS
})
def startMyApplicationTest() :
    # Act
    Globals(__file__
        , loadLocalConfig = False
        , logStatus = True
        , debugStatus = True
        , warningStatus = True
        , errorStatus = True
        , successStatus = True
        , failureStatus = True
        , settingStatus = True
        , encoding = 'utf-8'
        , printRootPathStatus = False
        , globalsEverything = False
        )

@EnvironmentVariable(environmentVariables={
    SettingHelper.ACTIVE_ENVIRONMENT : SettingHelper.LOCAL_ENVIRONMENT,
    'MY_COMPLEX_ENV' : ' -- my complex value -- ',
    'LATE_VALUE' : '-- late environment value --',
    'ONLY_ENVIRONMENT_VARIABLE' : 'only environment variable value',
    **LOG_HELPER_SETTINGS
})
def myConfigurationTests_basicVariableDefinitions() :
    # Arrange and Act
    globalsInstance = Globals(__file__
        , loadLocalConfig = False
        , debugStatus = True
        , warningStatus = True
        , errorStatus = True
        , successStatus = True
        , failureStatus = False
        , settingStatus = True
        , logStatus = False
        , encoding = 'utf-8'
        , printRootPathStatus = False
        , globalsEverything = False
        )

    # Assert
    assert 'self reference value' == globalsInstance.getSetting('my.self-reference-key')
    assert 'other self reference value as well' == globalsInstance.getSetting('my.other.self-reference-key.as-well')
    assert 'other repeated self reference value as well' == globalsInstance.getSetting('my.other.repeated.self-reference-key.as-well')
    assert 'my default value' == globalsInstance.getSetting('my.configuration-without-environment-variable-key')
    assert "my default value" == globalsInstance.getSetting('my.configuration-without-environment-variable-key-with-value-surrounded-by-single-quotes')
    assert 'my default value' == globalsInstance.getSetting('my.configuration-without-environment-variable-key-and-space-after-colon')
    assert 'self reference value' == globalsInstance.getSetting('my.configuration')
    assert 'self reference value' == globalsInstance.getSetting('my.own.configuration')
    assert 'other root value' == globalsInstance.getSetting('other.root.key')
    assert 'other root value' == globalsInstance.getSetting('my.own.very.deep.configuration')
    assert 'other self reference value as well' == globalsInstance.getSetting('my.other-with-other-name.self-reference-key.as-well')
    assert 'self reference value' == globalsInstance.getSetting('my.other-with-other-name.configuration')
    assert 'other self reference value as well' == globalsInstance.getSetting('my.other-with-other-name.configuration-as-well')
    assert 'other repeated self reference value as well' == globalsInstance.getSetting('my.other-with-other-name.configuration-repeated-as-well')
    assert globalsInstance.getSetting('my.override-case.overridden') is None
    assert 'overrider configuration' == globalsInstance.getSetting('my.override-case.overrider')

    assert 'delayed assignment value' == globalsInstance.getSetting('some-reference.before-its-assignment')
    assert 'delayed assignment value' == globalsInstance.getSetting('some-reference.much.before-its-assignment')
    assert "'''  value  ''' with spaces" == globalsInstance.getSetting('some-key.with-an-enter-in-between-the-previous-one')
    assert f"""Hi
        every
    one""".replace('\t',c.TAB) == globalsInstance.getSetting('long.string')
    assert f"""Hi
    every
    one
    this
    is
    the
    deepest
    long
                string
    here""".replace('\t',c.TAB) == globalsInstance.getSetting('deepest.long.string.ever.long.string')
    assert f"""me
    being
    fshds""".replace('\t',c.TAB) == globalsInstance.getSetting('not.idented.long.string')
    assert 'abcdefg' == globalsInstance.getSetting('it.contains.one-setting-injection')
    assert 'abcdefghijklm' == globalsInstance.getSetting('it.contains.two-consecutive-setting-injection')
    assert 'abcdefghijklm' == globalsInstance.getSetting('it.contains.one-inside-of-the-other-setting-injection')
    assert 'ABCD-- my complex value --EFG' == globalsInstance.getSetting('it.contains.one-setting-injection-with-environment-variable')
    assert 'ABCDEFGEFG-- my complex value --HIJKLMNOP' == globalsInstance.getSetting('it.contains.one-inside-of-the-other-setting-injection-with-environment-variable')
    assert 'abcdefghijklm' == globalsInstance.getSetting('it.contains.two-consecutive-setting-injection-with-missing-environment-variable')
    assert 'abcd-- late value ----abcd---- late value ----abcd--efg' == globalsInstance.getSetting('it.contains.some-composed-key.pointing-to.a-late-value')
    assert 'abcd-- late environment value ----abcd--it.contains.late-value--abcd--efg' == globalsInstance.getSetting('it.contains.some-composed-key.pointing-to.a-late-value-with-an-environment-variable-in-between')
    assert '-- late value --' == globalsInstance.getSetting('it.contains.late-value')
    assert 'only environment variable value' == globalsInstance.getSetting('it.contains.environment-variable.only')
    assert 'ABCD -- only environment variable value -- EFGH' == globalsInstance.getSetting('it.contains.environment-variable.surrounded-by-default-values')
    assert 'ABCD -- "some value followed by: "only environment variable value\' and some following default value\' -- EFGH' == globalsInstance.getSetting('it.contains.environment-variable.in-between-default-values')
    assert 'ABCD -- very late definiton value -- EFGH' == globalsInstance.getSetting('it.contains.refference.to-a-late-definition')
    assert 222233444 == globalsInstance.getSetting('handle.integer')
    assert 2.3 == globalsInstance.getSetting('handle.float')
    assert True == globalsInstance.getSetting('handle.boolean')
    assert 222233444 == globalsInstance.getSetting('handle.late.integer')
    assert 2.3 == globalsInstance.getSetting('handle.late.float')
    assert True == globalsInstance.getSetting('handle.late.boolean')
    assert [] == globalsInstance.getSetting('handle.empty.list')
    assert {} == globalsInstance.getSetting('handle.empty.dictionary-or-set')
    assert (()) == globalsInstance.getSetting('handle.empty.tuple')
    assert 'local' == globalsInstance.getSetting('environment.test')
    assert 'not at all' == globalsInstance.getSetting('environment.missing')
    assert 'ABCD -- 222233444 -- EFGH' == globalsInstance.getSetting('some-not-string-selfreference.integer')
    assert 'ABCD -- 2.3 -- EFGH' == globalsInstance.getSetting('some-not-string-selfreference.float')
    assert 'ABCD -- True -- EFGH' == globalsInstance.getSetting('some-not-string-selfreference.boolean')


@EnvironmentVariable(environmentVariables={
    'MY_CONFIGURATION_KEY' : 'my configuration value injected through environmnet variable',
    SettingHelper.ACTIVE_ENVIRONMENT : None,
    **LOG_HELPER_SETTINGS
})
def myConfigurationTests_whenEnvironmentVariableIsPresent() :
    # Arrange
    globalsInstance = Globals(__file__, loadLocalConfig = False)
    expected = 'my configuration value injected through environmnet variable'

    # Act
    toAssert = globalsInstance.getSetting('my.configuration')

    # Assert
    assert expected == toAssert

@EnvironmentVariable(environmentVariables={
    SettingHelper.ACTIVE_ENVIRONMENT : None,
    **LOG_HELPER_SETTINGS
})
def myConfigurationTests_whenEnvironmentVariableIsNotPresentAndIsSettingKeyReferencedAndSettingKeyAlreadyIsDefined() :
    # Arrange
    globalsInstance = Globals(__file__, loadLocalConfig = False)
    expected = globalsInstance.getSetting('my.self-reference-key')

    # Act
    toAssert = globalsInstance.getSetting('my.configuration')

    # Assert
    assert expected == toAssert

@EnvironmentVariable(environmentVariables={
    SettingHelper.ACTIVE_ENVIRONMENT : 'no-circular-reference',
    **LOG_HELPER_SETTINGS
})
def myConfigurationTests_musHandleSettingsWithNoSelfOrCircularReference() :
    # Arrange
    globalsInstance = Globals(__file__
        , loadLocalConfig = False
        , debugStatus = True
        , warningStatus = True
        , errorStatus = True
        , successStatus = True
        , failureStatus = False
        , settingStatus = True
        , logStatus = False
        , encoding = 'utf-8'
        , printRootPathStatus = False
        , globalsEverything = False
    )
    expected = 'Globals - no self reference'

    # Act
    toAssert = globalsInstance.getSetting('api.name')
    print(toAssert)

    # Assert
    assert expected == toAssert

@EnvironmentVariable(environmentVariables={
    SettingHelper.ACTIVE_ENVIRONMENT : SettingHelper.LOCAL_ENVIRONMENT,
    **LOG_HELPER_SETTINGS
})
def importResourceAndModule_withSuccess() :
    # Arrange
    SOME_VALUE = 'some value'
    globalsInstance = Globals(__file__
        , loadLocalConfig = False
        , debugStatus = True
        , warningStatus = True
        , errorStatus = True
        , successStatus = True
        , failureStatus = False
        , settingStatus = True
        , logStatus = False
        , encoding = 'utf-8'
        , printRootPathStatus = False
        , globalsEverything = False
    )

    # Act
    myServiceClass = globals.importResource('MyService', muteLogs=True)
    myOtherServiceClass = globals.importResource('MyOtherService', resourceModuleName='MyService', muteLogs=True)
    myServiceModule = globals.importModule('MyService', muteLogs=True)
    globalsInstance.ignoreResourceList += ['MyIgnorableService']
    myIgnorableServiceClass = globals.importResource('MyIgnorableService', muteLogs=True)
    myOtherIgnorableServiceClass = globals.importResource('MyOtherIgnorableService', resourceModuleName='MyIgnorableService', muteLogs=True)
    myOtherServiceModule = globals.importModule('MyIgnorableService', muteLogs=True)

    # Assert
    assert f'service value: {SOME_VALUE}' == myServiceClass().getServiceValue(SOME_VALUE)
    assert f'other service value: {SOME_VALUE}' == myOtherServiceClass().getServiceValue(SOME_VALUE)
    assert ObjectHelper.isNotNone(myServiceModule)
    assert ObjectHelper.isNone(myIgnorableServiceClass)
    assert ObjectHelper.isNone(myOtherIgnorableServiceClass)
    assert ObjectHelper.isNotNone(myOtherServiceModule)


@EnvironmentVariable(environmentVariables={
    SettingHelper.ACTIVE_ENVIRONMENT : 'missing_setting_file',
    **LOG_HELPER_SETTINGS
})
def shouldNotHandleMissingApplicationEnvironment() :
    # Arrange
    exception = None
    globalsInstance = None

    # Act
    try :
        globalsInstance = Globals(__file__, loadLocalConfig = False)
    except Exception as ext :
        exception = ext
        exceptionMessage = str(exception)

    # Assert
    assert ObjectHelper.isNone(globalsInstance)
    assert ObjectHelper.isNotNone(exception)
    assert 'No such file or directory:' in exceptionMessage
    assert 'application-missing_setting_file' in exceptionMessage

@EnvironmentVariable(environmentVariables={
    # SettingHelper.ACTIVE_ENVIRONMENT : SettingHelper.LOCAL_ENVIRONMENT,
    **LOG_HELPER_SETTINGS
})
def mustLoadLocalConfiguration() :
    # Arrange
    LOCAL_CONFIG_VALUE = 'local config setting value'

    # Act
    globalsInstance = Globals(__file__)

    # Assert
    assert LOCAL_CONFIG_VALUE == globalsInstance.getSetting('local.config.setting-key')
    assert True == globalsInstance.getSetting('print-status')
