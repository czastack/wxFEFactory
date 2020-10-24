import json
import traceback
import os
import pyapi
import __main__
from lib.utils import HistoryList
from lib.config import Configurable
from project import Project

CONFIG_DIR = 'config'
CONFIG_FILE = os.path.join(CONFIG_DIR, 'config.json')
CONFIG_START_OPTION = os.path.join(CONFIG_DIR, 'start_option.json')


class Application(Configurable):
    """保存一些全局数据"""
    def __init__(self):

        if not os.path.exists(CONFIG_DIR):
            os.makedirs(CONFIG_DIR, exist_ok=True)

        super().__init__(CONFIG_FILE)
        config = self.config
        recent_project = self.getconfig('recent_project')
        history_size = self.getconfig('history_size', 10)
        if recent_project:
            config['recent_project'] = HistoryList(recent_project, history_size)
            self.project = Project(config['recent_project'][-1])
        else:
            config['recent_project'] = HistoryList(maxsize=history_size)
            self.project = None

        self.start_option = self.load_temp_start_option() or self.getconfig('start_option')

    def project_confirm(self):
        if not self.project:
            pyapi.alert('未打开工程')
            return False
        return True

    def on_change_project(self, project):
        """切换工程"""
        self.config['recent_project'].append(project.path)
        self.config_changed = True
        self.project = project

    def on_exit(self):
        """退出处理"""
        for name in dir(__main__):
            if not name.startswith('__'):
                delattr(__main__, name)

    def load_temp_start_option(self):
        """加载临时启动参数"""
        data = None
        try:
            with open(CONFIG_START_OPTION, 'r+') as file:
                data = json.load(file)
                file.seek(0)
                file.truncate()
                file.write('null')
        except FileNotFoundError:
            pass
        except Exception:
            traceback.print_exc()
        return data

    def save_temp_start_option(self, start_option):
        """保存临时启动参数"""
        with open(CONFIG_START_OPTION, 'w') as file:
            json.dump(start_option, file)
