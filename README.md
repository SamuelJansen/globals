# Globals
This library allows global access to different python api classes and functions

# Simplest way to use it

- put all your git projects you wanna exchange classes between them in a single folder
\n-- `C:\Users\my_user\path\path\path\all_my_git_projects`

- on the directory you wanna launch the "main api" (the one that will consume other projects classes and funtions), 
you put the PathMannanger.py file following this path tree:
\n-- `C:\Users\my_user\path\path\path\all_my_git_projects\my_launcher_api\api\src\domain\control\PathMannanger.py`

- put the following code right on top of the __main__ class of your api
\n-- `from api.src.domain.control import PathMannanger
    pathMannanger = PathMannanger.PathMannanger(
        mode = 'WRONG_WAY_TO_MAKE_IT_WORKS',
        printStatus = True
    )`

- be happy
