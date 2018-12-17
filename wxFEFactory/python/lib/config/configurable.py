from abc import ABC, abstractmethod
import json


class Configurable(ABC):
    __slots__ = ('config_file', 'config_changed', 'observers')

    def __init__(self, config_file, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_file = config_file
        self.config_changed = False
        self.observers = {}
        self.loadconfig()

    def __del__(self):
        self.writeconfig()

    def __str__(self):
        return '{}("{}")'.format(self.__class__.__name__, self.config_file)

    def getconfig(self, name, defval=None):
        return self.config.get(name, defval)

    def setconfig(self, name, value, notify=True):
        if self.getconfig(name) != value:
            self.config[name] = value
            self.config_changed = True
            if notify:
                handler = self.observers.get(name, None)
                if handler:
                    handler(self, name, value)

    def setdefault(self, name, default):
        if name not in self.config:
            self.setconfig(name, default)

    def register_observer(self, name, handler):
        """ 注册变化观察者
        :param handler: fn(config, name, value)
        """
        self.observers[name] = handler

    def cancel_change(self):
        """放弃之前的所以修改"""
        self.config_changed = False

    def loadconfig(self):
        try:
            with open(self.config_file) as file:
                self.config = json.load(file)
        except Exception:
            self.config = {}

    def writeconfig(self):
        if self.config_changed:
            with open(self.config_file, 'w') as file:
                self.config = json.dump(self.config, file)
            self.config_changed = False


class Config(Configurable):
    load = Configurable.loadconfig
    write = Configurable.writeconfig

    def __getattr__(self, name):
        if name in self.observers:
            return self.getconfig(name)

    def __setattr__(self, name, value):
        if name not in self.__slots__ and name in self.observers:
            self.setconfig(name, value)
        else:
            object.__setattr__(self, name, value)
