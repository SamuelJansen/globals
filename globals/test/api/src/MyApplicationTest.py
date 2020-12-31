from globals.api.src.service.globals import Globals
from python_helper import EnvironmentVariable, SettingHelper, StringHelper, log
from python_helper import Constant as c

LOG_HELPER_SETTINGS = {
    log.LOG : False,
    log.SUCCESS : False,
    log.SETTING : False,
    log.DEBUG : False,
    log.WARNING : False,
    log.WRAPPER : False,
    log.FAILURE : False,
    log.ERROR : False
}

@EnvironmentVariable(environmentVariables={
        SettingHelper.ACTIVE_ENVIRONMENT : SettingHelper.LOCAL_ENVIRONMENT,
        **LOG_HELPER_SETTINGS
})
def startMyApplicationTest() :
    # Act
    Globals(__file__
        , logStatus = False
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

@EnvironmentVariable(environmentVariables={
    SettingHelper.ACTIVE_ENVIRONMENT : None,
    **LOG_HELPER_SETTINGS
})
def myConfigurationTests_whenEnvironmentVariableIsPresent() :
    # Arrange
    enveironmentKey = 'MY_CONFIGURATION_KEY'
    enveironmentValue = 'my configuration value injected through environmnet variable'
    environmentVariables = {enveironmentKey : enveironmentValue}
    @EnvironmentVariable(environmentVariables=environmentVariables)
    def initialiseGlobals() :
        return Globals(__file__)
    globalsInstance = initialiseGlobals()
    expected = enveironmentValue

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
    globalsInstance = Globals(__file__)
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
    expected = 'Globals - no circular reference'

    # Act
    toAssert = globalsInstance.getSetting('api.name')

    # Assert
    assert expected == toAssert
