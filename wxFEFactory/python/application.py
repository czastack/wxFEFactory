from lib.utils import HistoryList
from lib.config import Configurable
from project import Project
import json
import fefactory_api

CONFIG_FILE = 'config.json'
HISTORY_SIZE = 10

class Application(Configurable):
    """保存一些全局数据"""
    
    def __init__(self):
        Configurable.__init__(self, CONFIG_FILE)
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
        import __main__, application
        del __main__.app
        del __main__.win
        del application.app


app = Application()
fefactory_api.setOnAppExit(app.onExit)