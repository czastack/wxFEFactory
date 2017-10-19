from lib.utils import Configurable, HistoryList
from project import Project
import json
import fefactory_api

CONFIG_FILE = 'config.json'
HISTORY_SIZE = 10

class Application((Configurable)):
    """保存一些全局数据"""
    
    def __init__(self):
        super().__init__()
        self.loadConfig()
        config = self.config
        if 'recent_project' in config:
            config['recent_project'] = HistoryList(config['recent_project'], HISTORY_SIZE)
            self.project = Project(config['recent_project'][-1])
        else:
            config['recent_project'] = HistoryList(maxsize=HISTORY_SIZE)
            self.project = None

    def project_confirm(self):
        if not self.project:
            fefactory_api.alert('未打开工程')
            return False
        return True

    def getConfigFile(self):
        return CONFIG_FILE

    def getConfig(self, name, defval=None):
        return self.config.get(name, defval)

    def setConfig(self, name, value):
        self.config[name] = value

    def onChangeProject(self, project):
        self.config['recent_project'].append(project.path)
        self.config_changed = True
        self.project = project

    def onExit(self):
        self.writeConfig()
        if self.project:
            self.project.writeConfig()


app = Application()
fefactory_api.setOnAppExit(app.onExit)