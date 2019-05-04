from tools.base.native import NativeContext, NativeContext64


class SafeScriptEnv:
    def __init__(self, owner, names=None):
        """
        :param names: 确保调用script_call执行的方法名集合
        """
        self.owner = owner
        self.names = names

    def __enter__(self):
        self._script_call = self.owner.script_call
        self.owner.script_call = self.hook if self.names else self.owner.script_hook_call
        return self

    def __exit__(self, *args):
        self.owner.script_call = self._script_call
        del self._script_call

    def hook(self, name, *args, **kwargs):
        return (self.owner.script_hook_call if name in self.names else self._script_call)(name, *args, **kwargs)
