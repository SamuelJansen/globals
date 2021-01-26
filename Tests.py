from python_helper import TestHelper
# TestHelper.run(__file__, inspectGlobals=False)
TestHelper.run(
    __file__,
    times = 2,
    testStatus = False,
    logStatus = True,
    logResult = True,
    inspectGlobals = True
)
# TestHelper.run(
#     __file__,
#     times = 10,
#     runOnly = [
#         'MyApplicationTest.startMyApplicationTest'
#         ],
#     testStatus = False,
#     logStatus = False,
#     logResult = False
# )
