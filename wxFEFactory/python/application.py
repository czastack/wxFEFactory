import json
import fefactory_api
import __main__
from lib.utils import HistoryList
from lib.config import Configurable
from project import Project

CONFIG_FILE = 'config/config.json'


class Application(Configurable):
    """保存一些全局数据"""
    def __init__(self):
        Configurable.__init__(self, CONFIG_FILE)
        config = self.config
        recent_project = self.getconfig('recent_project')
        history_size = self.getconfig('history_size', 10)
        if recent_project:
            config['recent_project'] = HistoryList(recent_project, history_size)
            self.project = Project(config['recent_project'][-1])
        else:
            config['recent_project'] = HistoryList(maxsize=history_size)
            self.project = None

        self.start_option = self.getconfig('start_option')

    def project_confirm(self):
        if not self.project:
            fefactory_api.alert('未打开工程')
            return False
        return True

    def on_change_project(self, project):
        self.config['recent_project'].append(project.path)
        self.config_changed = True
        self.project = project

    def on_exit(self):
        self.writeconfig()
        if self.project:
            self.project.writeconfig()
        # globals().pop('app')
        del __main__.app
        del __main__.win


app = Application()
fefactory_api.set_on_exit(app.on_exit)
