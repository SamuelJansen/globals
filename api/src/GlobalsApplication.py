from domain.control import PathMannanger
pathMannanger = PathMannanger.PathMannanger()

print('Glopals api')

print(
f'''pathMannanger = {pathMannanger}
pathMannanger.currentPath =                 {pathMannanger.currentPath}
pathMannanger.localPath =                   {pathMannanger.localPath}
pathMannanger.baseApiPath =                 {pathMannanger.baseApiPath}
pathMannanger.apiPath =                     {pathMannanger.apiPath}
pathMannanger.apiName =                     {pathMannanger.apiName}
pathMannanger.apisRoot =                    {pathMannanger.apisRoot}
pathMannanger.apiNames =                    {pathMannanger.apiNames}
pathMannanger.localGlobalsApiPath =         {pathMannanger.localGlobalsApiPath}
pathMannanger.globalsApiName =              {pathMannanger.globalsApiName}
pathMannanger.globalsApiPath =              {pathMannanger.globalsApiPath}''')

import Application
