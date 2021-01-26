from python_helper import TestHelper
# TestHelper.run(__file__)
TestHelper.run(
    __file__,
    times = 10,
    # runOnly = [
    #     'LogHelperTest.mustLogPretyPythonWithColors',
    #     'LogHelperTest.mustLogPretyJsonWithColors'
    #     ],
    testStatus = False,
    logStatus = True,
    logResult = True
)
