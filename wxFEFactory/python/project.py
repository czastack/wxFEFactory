import os
Path = os.path

class Project:
    # __slots__ = ()

    def __init__(self, path, title=None):
        self.path = path
        self.title = title or Path.basename(path)
        self.check()

    def getConfigFile(self):
        return Path.join(self.path, 'project.json')

    def check(self):
        if not Path.exists(self.path):
            os.mkdir(self.path)

    def exists(self):
        return Path.exists(self.getConfigFile())

    def save(self):
        pass
