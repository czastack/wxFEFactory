import json
import os
from lib.config import Configurable
Path = os.path


class Project(Configurable):

    def __init__(self, path, title=None):
        self.path = path
        self.title = title
        if not Path.exists(self.path):
            os.mkdir(self.path)
        super().__init__(Path.join(self.path, 'project.json'))

    def exists(self):
        return Path.exists(self.config_file)

    @property
    def title(self):
        return self.config.get('title', None)

    @title.setter
    def title(self, title):
        if title:
            self.setconfig('title', title)
