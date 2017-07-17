
class A:
    __slots__ = ()

    def __del__(self):
        print("del")

print("123")

a=A()