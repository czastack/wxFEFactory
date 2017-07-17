from lib.utils import Configurable
import json
import os
Path = os.path

class Project(Configurable):
    # __slots__ = ()

    def __init__(self, path, title=None):
        super().__init__()
        self.path = path
        self.title = title
        self.check()

    def getConfigFile(self):
        return Path.join(self.path, 'project.json')

    def check(self):
        if not Path.exists(self.path):
            os.mkdir(self.path)
        else:
            self.loadConfig()

    def exists(self):
        return Path.exists(self.getConfigFile())

    @property
    def title(self):
        return self.config.get('title', None)

    @title.setter
    def title(self, title):
        if title:
            self.setConfig('title', title)

