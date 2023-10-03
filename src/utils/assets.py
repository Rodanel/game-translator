from os import getcwd, path


class MyAssets(object):

    @classmethod
    def get_asset_path(cls, asset:str) -> str:
        _exeDir = path.join(getcwd())
        _internaldir = path.join(_exeDir, "_internal")
        if path.exists(_internaldir):
            return path.join(_internaldir, asset)
        else:
            return path.join(_exeDir, asset)

    @classmethod    
    @property
    def favicon(cls):
        return "assets/favicon.ico"

    @classmethod    
    @property
    def icon(cls):
        return "assets/icon.jpg"

