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

    def getConfigFile(self):
        return CONFIG_FILE

    def onChangeProject(self, project):
        self.config['recent_project'].append(project.path)
        self.config_changed = True
        self.project = project

    def onExit(self):
        self.writeConfig()
        self.project.writeConfig()


app = Application()
fefactory_api.setOnAppExit(app.onExit)