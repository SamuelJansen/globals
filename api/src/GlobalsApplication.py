if __name__ == '__main__' :
    from domain.control import PathMannanger
    # PathMannanger.PathMannanger(mode = 'WRONG_WAY_TO_MAKE_IT_WORKS')
    PathMannanger.PathMannanger(globalsApis='Globals.api.list',printStatus = True)
