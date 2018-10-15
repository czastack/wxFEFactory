from functools import reduce
import math
PI = math.pi


def degreeToRadian(degrees):
    return degrees * (PI / 180.0)


def radianToDegree(radian):
    return radian / PI * 180.0


def headingToDirection(heading):
    heading = degreeToRadian(heading)
    return -math.sin(heading), math.cos(heading)


def get_vertical_vector(v):
    """获取一个垂直的向量"""
    length = len(v)
    for i in range(length):
        if v[i]:
            break
    else:
        # 0向量
        pass

    a = v[i]
    result = [1] * length
    result[i] = -(sum(v) - a) / a
    return result


class Vector:
    def __init__(self, values):
        self._values = list(values)

    def values(self):
        return list(self._values)

    def clone(self):
        return self.__class__(self._values)

    def __getitem__(self, i):
        return self._values[i]

    def __setitem__(self, i, value):
        self._values[i] = value

    def __iter__(self):
        return iter(self._values)

    def __add__(self, value):
        if hasattr(value, '__iter__'):
            return self.__class__(self[i] + it for i, it in enumerate(value))
        else:
            return self.__class__(it + value for it in self)

    def __iadd__(self, value):
        if hasattr(value, '__iter__'):
            for i, it in enumerate(value):
                self[i] += it
        else:
            for i in range(self.len):
                self[i] += value
        return self

    def __mul__(self, value):
        if hasattr(value, '__iter__'):
            return self.__class__(self[i] * it for i, it in enumerate(value))
        else:
            return self.__class__(it * value for it in self)

    def __imul__(self, value):
        if hasattr(value, '__iter__'):
            for i, it in enumerate(value):
                self[i] *= it
        else:
            for i in range(self.len):
                self[i] *= value
        return self

    def __len__(self):
        """向量维度"""
        return len(self._values)

    def __str__(self):
        return str(self._values)

    def __repr__(self):
        return self.__class__.__name__ + str(tuple(self._values))

    @property
    def len(self):
        """向量维度"""
        return self.__len__()

    @property
    def length(self):
        return math.sqrt(reduce(lambda a, b: a + b * b, self, 0))

    def normalize(self):
        length = self.length

        if length == 0 or length == 1:
            return

        for i in range(self.len):
            self[i] /= length

    def distance(self, v):
        if v.length != self.length:
            raise ValueError('维度不一致')
        return math.sqrt(sum(
            (abs(self[i] - v[i]) ** 2) for i in range(self.length)
        ))

    class Item:
        def __init__(self, i):
            self.i = i

        def __get__(self, instance, ownner=None):
            return instance[self.i]

        def __set__(self, instance, value):
            instance[self.i] = value


class Vector2(Vector):
    x = Vector.Item(0)
    y = Vector.Item(1)

    def __init__(self, values=(0.0, 0.0)):
        Vector.__init__(self, values)

    def get_vetical_xy(self):
        """获取xy面上垂直的向量"""
        v1 = Vector2(get_vertical_vector((self.x, self.y)))
        v2 = Vector2(v1)
        v2 *= -1
        return v1, v2


class Vector3(Vector):
    x = Vector.Item(0)
    y = Vector.Item(1)
    z = Vector.Item(2)

    def __init__(self, values=(0.0, 0.0, 0.0)):
        Vector.__init__(self, values)
        if self.len is not 3:
            raise ValueError('Vector3 need 3 element values')

    get_vetical_xy = Vector2.get_vetical_xy


class Quaternion(Vector3):
    w = Vector.Item(3)

    def __init__(self, values=(0.0, 0.0, 0.0, 0.0)):
        if len(values) is not 4:
            raise ValueError('Quaternion need 4 element values')
        Vector.__init__(self, values)

    def to_rotation(self):
        x, y, z, w = self
        pitch = math.atan2(2.0 * (y * z + w * x), w * w - x * x - y * y + z * z)
        yaw = math.atan2(2.0 * (x * y + w * z), w * w + x * x - y * y - z * z)
        roll = math.asin(-2.0 * (x * z - w * y))
        return Vector3((pitch, roll, yaw))

    @classmethod
    def from_rotation(cls, rotation):
        """
        :param rotation: Vector3 object
        """
        WorldUp = Vector3((0.0, 0.0, 1.0))
        WorldEast = Vector3((1.0, 0.0, 0.0))
        WorldNorth = Vector3((0.0, 1.0, 0.0))

        qyaw = cls.rotation_axis(WorldUp, rotation.x)
        qyaw.normalize()
        qpitch = cls.rotation_axis(WorldEast, rotation.y)
        qpitch.normalize()
        qroll = cls.rotation_axis(WorldNorth, rotation.z)
        qroll.normalize()
        yawpitch = qyaw * qpitch * qroll
        yawpitch.normalize()
        return yawpitch

    @classmethod
    def rotation_axis(cls, axis, angle):
        """
        :param axis: Vector3 object
        """
        # axis.normalize()
        half = angle * 0.5
        sin = math.sin(half)
        cos = math.cos(half)

        return Quaternion((
            axis.x * sin,
            axis.y * sin,
            axis.z * sin,
            cos
        ))

        return result

    def __mul__(self, right):

        lx, ly, lz, lw = self
        rx, ry, rz, rw = right

        return Quaternion((
            (lx * rw + rx * lw) + (ly * rz) - (lz * ry),
            (ly * rw + ry * lw) + (lz * rx) - (lx * rz),
            (lz * rw + rz * lw) + (lx * ry) - (ly * rx),
            (lw * rw) - (lx * rx + ly * ry + lz * rz)
        ))


class VectorField(Vector):
    x = Vector.Item(0)
    y = Vector.Item(1)
    z = Vector.Item(2)

    def __init__(self, obj, values, name):
        super().__init__(values)
        self.obj = obj
        self.name = name

    def __setitem__(self, i, value):
        super().__setitem__(i, value)
        setattr(self.obj, self.name, self._values)


class CoordData(VectorField):
    """坐标数据"""
    def __init__(self, obj, values, name="coord"):
        super().__init__(obj, values, name)
