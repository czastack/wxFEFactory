from abc import ABC, abstractmethod
import json

class Configurable(ABC):
    def __init__(self, config_file, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_file = config_file
        self.config_changed = False
        self.observers = {}
        self.loadConfig()

    def __del__(self):
        self.writeConfig()

    def getConfig(self, name, defval=None):
        return self.config.get(name, defval)

    def setConfig(self, key, value, notify=True):
        if self.getConfig(key) != value:
            self.config[key] = value
            self.config_changed = True
            if notify:
                handler = self.observers.get(key, None)
                if handler:
                    handler(self, key, value)

    def registerObserver(self, key, handler):
        """ 注册变化观察者
        :param handler: fn(config, key, value) 
        """
        self.observers[key] = handler

    def cancel_change(self):
        """放弃之前的所以修改"""
        self.config_changed = False

    def loadConfig(self):
        try:
            with open(self.config_file) as file:
                self.config = json.load(file)
        except FileNotFoundError:
            self.config = {}

    def writeConfig(self):
        if self.config_changed:
            with open(self.config_file, 'w') as file:
                self.config = json.dump(self.config, file)
            self.config_changed = False