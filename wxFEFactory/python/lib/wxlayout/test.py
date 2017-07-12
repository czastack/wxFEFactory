import inspect

class View:
    __slots__ = ()
    LAYOUTS = []

    def __init__(self, key=None):
        layout = self.activeLayout()
        if layout:
            layout.add(self, key)

    @classmethod
    def activeLayout(class_):
        return class_.LAYOUTS[-1] if len(class_.LAYOUTS) else None


class Control(View):
    __slots__ = ()


class Parent(View):
    __slots__ = ()


class Layout(View):
    __slots__ = ('children', 'named_children')

    def __init__(self):
        super().__init__()
        self.children = []
        self.named_children = {}

    def add(self, child, key=None):
        self.children.append(child)
        if key:
            self.add_named(child, key)

    def add_named(self, child, key):
        self.named_children[key] = child

    def __iter__(self):
        return iter(self.children)

    def __enter__(self):
        self.LAYOUTS.append(self)
        return self

    def __exit__(self, typ, value, tb):
        # scope = inspect.currentframe().f_back
        # for key, value in scope.f_locals.items():
        #     if value is not self and isinstance(value, View) and value in self:
        #         self.add_named(value, key)
        pass

    def __setattr__(self, key, value):
        if isinstance(value, View) and not key.startswith("_"):
            self.add(value, key=key)
        else:
            super().__setattr__(key, value)

    def __getattr__(self, key):
        return self.named_children.get(key, None) or super().__getattr__(key)


if __name__ == 'builtins':
    def fn():
        with Layout() as p:
            View()
            View(key='a')
        print(p.children, p.named_children)

    fn()