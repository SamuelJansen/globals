import globals
from python_helper import Test, SettingHelper, log, ObjectHelper, EnvironmentHelper
from python_helper import Constant as c

LOG_HELPER_SETTINGS = {
    log.LOG : False,
    log.SUCCESS : False,
    log.SETTING : False,
    log.DEBUG : False,
    log.WARNING : False,
    log.WRAPPER : False,
    log.FAILURE : False,
    log.ERROR : False,
    log.TEST : False
}

# LOG_HELPER_SETTINGS = {
#     log.LOG : False,
#     log.SUCCESS : True,
#     log.SETTING : True,
#     log.DEBUG : True,
#     log.WARNING : True,
#     log.WRAPPER : True,
#     log.FAILURE : True,
#     log.ERROR : True,
#     log.TEST : True
# }

@Test(environmentVariables={
        SettingHelper.ACTIVE_ENVIRONMENT : SettingHelper.LOCAL_ENVIRONMENT,
        **LOG_HELPER_SETTINGS
    }
)
def startMyApplicationTest() :
    # Act
    globals.newGlobalsInstance(__file__
        , loadLocalConfig = False
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

@Test(environmentVariables={
        SettingHelper.ACTIVE_ENVIRONMENT : SettingHelper.LOCAL_ENVIRONMENT,
        'MY_COMPLEX_ENV' : ' -- my complex value -- ',
        'LATE_VALUE' : '-- late environment value --',
        'ONLY_ENVIRONMENT_VARIABLE' : 'only environment variable value',
        **LOG_HELPER_SETTINGS
    }
)
def myConfigurationTests_basicVariableDefinitions() :
    # Arrange and Act
    globalsInstance = globals.newGlobalsInstance(__file__
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
        not
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
    assert ObjectHelper.equals('/my/static/folder', globalsInstance.settingTree['python']['static-package'])
    print(globalsInstance.getSetting(globals.AttributeKey.PYTHON_STATIC_PACKAGE))
    assert ObjectHelper.equals('/my/static/folder', globalsInstance.getSetting(globals.AttributeKey.PYTHON_STATIC_PACKAGE))
    assert ObjectHelper.equals('/my/static/folder', globalsInstance.getStaticPackagePath())

@Test(environmentVariables={
        'MY_CONFIGURATION_KEY' : 'my configuration value injected through environmnet variable',
        SettingHelper.ACTIVE_ENVIRONMENT : None,
        **LOG_HELPER_SETTINGS
    }
)
def myConfigurationTests_whenEnvironmentVariableIsPresent() :
    # Arrange
    globalsInstance = globals.newGlobalsInstance(__file__, loadLocalConfig = False)
    expected = 'my configuration value injected through environmnet variable'

    # Act
    toAssert = globalsInstance.getSetting('my.configuration')

    # Assert
    assert expected == toAssert

@Test(environmentVariables={
        SettingHelper.ACTIVE_ENVIRONMENT : None,
        **LOG_HELPER_SETTINGS
    }
)
def myConfigurationTests_whenEnvironmentVariableIsNotPresentAndIsSettingKeyReferencedAndSettingKeyAlreadyIsDefined() :
    # Arrange
    globalsInstance = globals.newGlobalsInstance(__file__, loadLocalConfig = False)
    expected = globalsInstance.getSetting('my.self-reference-key')

    # Act
    toAssert = globalsInstance.getSetting('my.configuration')

    # Assert
    assert expected == toAssert

@Test(environmentVariables={
        SettingHelper.ACTIVE_ENVIRONMENT : 'no-circular-reference',
        **LOG_HELPER_SETTINGS
    }
)
def myConfigurationTests_musHandleSettingsWithNoSelfOrCircularReference() :
    # Arrange
    globalsInstance = globals.newGlobalsInstance(__file__
        , loadLocalConfig = False
        , debugStatus = False
        , warningStatus = False
        , errorStatus = False
        , successStatus = False
        , failureStatus = False
        , settingStatus = False
        , logStatus = False
        , encoding = 'utf-8'
        , printRootPathStatus = False
        , globalsEverything = False
    )
    expected = 'Globals - no self reference'

    # Act
    toAssert = globalsInstance.getSetting('api.name')

    # Assert
    assert expected == toAssert

@Test(environmentVariables={
        SettingHelper.ACTIVE_ENVIRONMENT : SettingHelper.LOCAL_ENVIRONMENT,
        **LOG_HELPER_SETTINGS
    }
)
def importResourceAndModule_withSuccess() :
    # Arrange
    SOME_VALUE = 'some value'
    globalsInstance = globals.newGlobalsInstance(__file__
        , debugStatus = True
        , warningStatus = True
        , errorStatus = True
        , successStatus = True
        , wrapperStatus = False
        , failureStatus = False
        , settingStatus = True
        , logStatus = False

        # , debugStatus = True
        # , warningStatus = True
        # , errorStatus = True
        # , successStatus = True
        # , failureStatus = True
        # , settingStatus = True
        # , wrapperStatus = True
        # , logStatus = True

        , loadLocalConfig = False
        , encoding = 'utf-8'
        , printRootPathStatus = False
        , globalsEverything = False
    )

    # Act
    myServiceClass = globals.importResource('MyService', muteLogs=False)
    myOtherServiceClass = globals.importResource('MyOtherService', resourceModuleName='MyService', muteLogs=False)
    myServiceModule = globals.importModule('MyService', muteLogs=False)
    globalsInstance.ignoreResourceList += ['MyIgnorableService']
    myIgnorableServiceClass = globals.importResource('MyIgnorableService', muteLogs=False)
    myOtherIgnorableServiceClass = globals.importResource('MyOtherIgnorableService', resourceModuleName='MyIgnorableService', muteLogs=False)
    myOtherServiceModule = globals.importModule('MyIgnorableService', muteLogs=False)
    pythonHelperLogModule = globals.importResource('log', resourceModuleName='python_helper', muteLogs=False)
    pythonHelperLogModuleLOGValue = globals.importResource('log.LOG', resourceModuleName='python_helper', muteLogs=False)
    myDomainValue = globals.importResource('MyDomain.myDomainValue', muteLogs=False)

    # Assert
    assert f'service value: {SOME_VALUE}' == myServiceClass().getServiceValue(SOME_VALUE)
    assert f'other service value: {SOME_VALUE}' == myOtherServiceClass().getServiceValue(SOME_VALUE)
    assert ObjectHelper.isNotNone(myServiceModule)
    assert ObjectHelper.isNone(myIgnorableServiceClass)
    assert ObjectHelper.isNone(myOtherIgnorableServiceClass)
    assert ObjectHelper.isNotNone(myOtherServiceModule)
    assert log == pythonHelperLogModule
    assert ObjectHelper.equals(log.LOG, pythonHelperLogModuleLOGValue)
    assert ObjectHelper.equals('my value', myDomainValue)


@Test(environmentVariables={
        SettingHelper.ACTIVE_ENVIRONMENT : 'missing_setting_file',
        **LOG_HELPER_SETTINGS
    }
)
def shouldNotHandleMissingEnvironmentSettings() :
    # Arrange
    exception = None
    globalsInstance = None

    # Act
    try :
        globalsInstance = globals.newGlobalsInstance(__file__, loadLocalConfig = False)
    except Exception as ext :
        exception = ext

    # Assert
    assert ObjectHelper.isNone(globalsInstance)
    assert ObjectHelper.isNotNone(exception)
    assert 'missing_setting_file' == EnvironmentHelper.get(SettingHelper.ACTIVE_ENVIRONMENT)
    assert 'missing_setting_file' == SettingHelper.getActiveEnvironment()
    assert str(exception).startswith('The "')
    assert str(exception).endswith('globals\\globals\\api\\test\\api\\resource\\application-missing_setting_file.yml" setting file path was not found')

@Test(environmentVariables={
        'MY_COMPLEX_ENV' : ' -- my complex value -- ',
        'LATE_VALUE' : '-- late environment value --',
        'ONLY_ENVIRONMENT_VARIABLE' : 'only environment variable value',
        **LOG_HELPER_SETTINGS
    }
)
def mustLoadLocalConfiguration() :
    # Arrange
    LOCAL_CONFIG_VALUE = 'local config setting value'
    FIRST_LONG_STRING = '''"""Hi
                every
            one
            """'''
    SECOND_LONG_STRING = '''"""Hi
                            every
                            one
                            this
                            is
                            the
                            deepest
                            long
                                        string
                            here
                            """'''
    THIRD_LONG_STRING = '''"""
                    me
                    being
        not
                    fshds
                    """'''
    expected = {
        'print-status': True,
        'local': {
            'config': {
                'setting-key': 'local config setting value'
            }
        },
        'database': {
            'dialect': 'a:b$c:d',
            'username': 'e:f?g:h',
            'password': 'i:j!k:l',
            'host': 'm:n*o:p',
            'port': '[q:r:s:t]',
            'schema': '(u:v:w:x)'
        },
        'environment': {
            'database': {
                'key': 'DATABASE_URL',
                'value': 'a:b$c:d://e:f?g:h:i:j!k:l@m:n*o:p:[q:r:s:t]/(u:v:w:x)'
            },
            'test': 'production',
            'missing': 'not at all'
        },
        'server': {
            'scheme': 'https',
            'host': 'host',
            'servlet': {
                'context-path': '/test-api'
            },
            'port': 5050
        },
        'api': {
            'host-0': 'https://host',
            'host-1': 'https://host/test-api',
            'host-2': 'https://host:5050/test-api',
            'name': 'Globals',
            'extension': 'yml',
            'dependency': {
                'update': False,
                'list': {
                    'web': [
                        'Popen',
                        'Path'
                    ],
                    'local': []
                }
            },
            'list': [
                'Globals'
            ],
            'language': 'EN-US',
            'git': {
                'url': 'https://github.com/SamuelJansen/',
                'extension': 'git'
            }
        },
        'swagger': {
            'host': 'host',
            'info': {
                'title': 'TestApi',
                'version': '0.0.1',
                'description': 'description',
                'terms-of-service': 'http://swagger.io/terms/',
                'contact': {
                    'name': 'Samuel Jansen',
                    'email': 'samuel.jansenn@gmail.com'
                },
                'license': {
                    'name': 'Apache 2.0 / MIT License',
                    'url': 'http://www.apache.org/licenses/LICENSE-2.0.html'
                }
            },
            'schemes': [
                'https'
            ]
        },
        'python': {
            'version': 3.9
        },
        'some-reference': {
            'much': {
                'before-its-assignment': 'delayed assignment value'
            },
            'before-its-assignment': 'delayed assignment value'
        },
        'other': {
            'root': {
                'key': 'other root value'
            }
        },
        'my': {
            'self-reference-key': 'self reference value',
            'other': {
                'self-reference-key': {
                    'as-well': 'other self reference value as well'
                },
                'repeated': {
                    'self-reference-key': {
                        'as-well': 'other repeated self reference value as well'
                    }
                }
            },
            'configuration-without-environment-variable-key': 'my default value',
            'configuration-without-environment-variable-key-with-value-surrounded-by-single-quotes': 'my default value',
            'configuration-without-environment-variable-key-and-space-after-colon': 'my default value',
            'own': {
                'very': {
                    'deep': {
                        'configuration': 'other root value'
                    }
                },
                'configuration': 'self reference value'
            },
            'other-with-other-name': {
                'self-reference-key': {
                    'as-well': 'other self reference value as well'
                },
                'configuration': 'self reference value',
                'configuration-as-well': 'other self reference value as well',
                'configuration-repeated-as-well': 'other repeated self reference value as well'
            },
            'override-case': {
                'overrider': 'overrider configuration'
            },
            'configuration': 'self reference value'
        },
        'long': {
            'string': FIRST_LONG_STRING
        },
        'deepest': {
            'long': {
                'string': {
                    'ever': {
                        'long': {
                            'string': SECOND_LONG_STRING
                        }
                    }
                }
            }
        },
        'not': {
            'idented': {
                'long': {
                    'string': THIRD_LONG_STRING
                }
            }
        },
        'new-key': 'new value',
        'my-list': {
            'numbers': [
                1,
                2,
                3,
                4
            ],
            'simple-strings': [
                'a',
                'b',
                'c',
                'd'
            ],
            'complex': [
                2,
                'b',
                'c',
                'd',
                1,
                2,
                True,
                True
            ],
            'with-elemets-surrounded-by-all-sorts-of-quotes': [
                'a',
                'b',
                'c',
                'd',
                'e',
                'f'
            ]
        },
        'specific-for': {
            'previous-assignment': 'delayed assignment value'
        },
        'some-key': {
            'with-an-enter-in-between-the-previous-one': "'''  value  ''' with spaces"
        },
        'it': {
            'contains': {
                'some-composed-key': {
                    'pointing-to': {
                        'a-late-value': 'abcd-- late value ----abcd---- late value ----abcd--efg',
                        'a-late-value-with-an-environment-variable-in-between': 'abcd-- late environment value ----abcd--it.contains.late-value--abcd--efg'
                    }
                },
                'late-value': '-- late value --',
                'environment-variable': {
                    'only': 'only environment variable value',
                    'surrounded-by-default-values': 'ABCD -- only environment variable value -- EFGH',
                    'in-between-default-values': """ABCD -- "some value followed by: "only environment variable value' and some following default value' -- EFGH"""
                },
                'refference': {
                    'to-a-late-definition': 'ABCD -- very late definiton value -- EFGH'
                },
                'one-setting-injection': 'abcdefg',
                'two-consecutive-setting-injection': 'abcdefghijklm',
                'one-inside-of-the-other-setting-injection': 'abcdefghijklm',
                'one-setting-injection-with-environment-variable': 'ABCD-- my complex value --EFG',
                'one-inside-of-the-other-setting-injection-with-environment-variable': 'ABCDEFGEFG-- my complex value --HIJKLMNOP',
                'two-consecutive-setting-injection-with-missing-environment-variable': 'abcdefghijklm'
            }
        },
        'very-late': {
            'definition': 'very late definiton value'
        },
        'handle': {
            'late': {
                'integer': 222233444,
                'float': 2.3,
                'boolean': True
            },
            'integer': 222233444,
            'float': 2.3,
            'boolean': True,
            'empty': {
                'list': [],
                'dictionary-or-set': {},
                'tuple': ()
            }
        },
        'some': {
            'dictionary': {
                'yolo': 'yes',
                'another-yolo': 'no',
                'another-yolo-again': '',
                f'''{'{'}{" 'again?'"}''': f'''{"'yes' "}{'}'}'''
            }
        },
        'some-not-string-selfreference': {
            'integer': 'ABCD -- 222233444 -- EFGH',
            'float': 'ABCD -- 2.3 -- EFGH',
            'boolean': 'ABCD -- True -- EFGH'
        }
    }



    # Act
    globalsInstance = globals.newGlobalsInstance(__file__, settingStatus=True, settingsFileName='other-application')
    # globalsInstance.printTree(globalsInstance.settingTree, 'settingTree')
    # globalsInstance.printTree(globalsInstance.defaultSettingTree, 'defaultSettingTree')

    # Assert
    assert LOCAL_CONFIG_VALUE == globalsInstance.getSetting('local.config.setting-key')
    assert True == globalsInstance.getSetting('print-status')
    assert 'Globals' == globalsInstance.getSetting('api.name')
    assert "a:b$c:d://e:f?g:h:i:j!k:l@m:n*o:p:[q:r:s:t]/(u:v:w:x)" == globalsInstance.getSetting('environment.database.value')
    assert expected['long']['string'] == globalsInstance.settingTree['long']['string']
    assert expected['deepest']['long']['string']['ever']['long']['string'] == globalsInstance.settingTree['deepest']['long']['string']['ever']['long']['string']
    assert expected['not']['idented']['long']['string'] == globalsInstance.settingTree['not']['idented']['long']['string']
    assert ObjectHelper.equals(expected['some']['dictionary'], globalsInstance.settingTree['some']['dictionary'])
    assert ObjectHelper.equals(expected, globalsInstance.settingTree, ignoreKeyList = [])

@Test(environmentVariables={
        **LOG_HELPER_SETTINGS
    }
)
def mustLoadLocalConfiguration_correctly() :
    # Arrange
    expected = {
        'print-status': False,
        'server': {
            'scheme': 'http',
            'host': 'localhost',
            'host-and-port': 'localhost:5050',
            'port': 5050,
            'servlet': {
                'context-path': '/test-api'
            }
        },
        'has-it': {
            'or-not': '?',
            'here': '?'
        },
        'flask-specific-port': 'flask run --host=0.0.0.0 --port=5001',
        'api': {
            'name': 'TestApi',
            'extension': 'yml',
            'dependency': {
                'update': False,
                'list': {
                    'web': [
                        'globals',
                        'python_helper',
                        'Popen',
                        'Path',
                        'numpy',
                        'pywin32',
                        'sqlalchemy'
                    ]
                }
            },
            'git': {
                'force-upgrade-command': 'pip install --upgrade --force python_framework'
            },
            'static-package': 'AppData\Local\Programs\Python\Python38-32\statics',
            'list': []
        },
        'swagger': {
            'info': {
                'title': 'TestApi',
                'version': '0.0.1',
                'description': 'description',
                'terms-of-service': 'http://swagger.io/terms/',
                'contact': {
                    'name': 'Samuel Jansen',
                    'email': 'samuel.jansenn@gmail.com'
                },
                'license': {
                    'name': 'Apache 2.0 / MIT License',
                    'url': 'http://www.apache.org/licenses/LICENSE-2.0.html'
                }
            },
            'host': 'localhost:5050',
            'schemes': [
                'http'
            ]
        },
        'python': {
            'version': 3.9
        }
    }

    # Act
    globalsInstance = globals.newGlobalsInstance(__file__, debugStatus=True, settingsFileName='fallback-priority')
    # log.prettyJson(mustLoadLocalConfiguration_correctly, 'Must Load Local Configuration setting tree', globalsInstance.settingTree, logLevel=log.DEBUG)

    # Assert
    assert ObjectHelper.equals(expected, globalsInstance.settingTree)
