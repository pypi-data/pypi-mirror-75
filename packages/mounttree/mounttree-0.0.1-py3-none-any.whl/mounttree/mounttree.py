import numpy as np


def deg2rad(deg):
    return deg/180.0*np.pi


def rad2deg(rad):
    return rad/np.pi*180.0


class FrameNotFoundError(Exception):
    pass


coordinate_lib = {
    'WGS-84': lambda variables={}:
        OblateEllipsoidFrame(6378137.0, 6356752.314245, variables),
    'GRS-80': lambda variables={}:
        OblateEllipsoidFrame(6378137.0,  6356752.314140, variables),
}


class CoordinateUniverse(object):
    def __init__(self, name, root_frame, variables={}):
        self.name = name
        self.root_frame = root_frame
        self.variables = variables

    def find_path_to_frame(self, framename):
        return self.root_frame.find_path_to_frame(framename)

    def get_frame(self, framename):
        return self.root_frame.get_frame(framename)

    def get_transformation(self, start, to, **kwargs):
        transform_variables = self.variables.copy()
        transform_variables.update(kwargs)
        self.root_frame.set_variables(**transform_variables)
        p1 = self.find_path_to_frame(start)
        p2 = self.find_path_to_frame(to)
        prefix = self.root_frame
        while(p1 and p2 and p1[0] is p2[0]):
            prefix = p1[0]
            p1 = p1[1:]
            p2 = p2[1:]
        from_transform = prefix.collect_transform(p1)
        to_transform = prefix.collect_transform(p2)
        return to_transform.invert() * from_transform

    def update(self, **kwargs):
        self.variables.update(kwargs)
        self.root_frame.update(**kwargs)

    def set_variables(self, **kwargs):
        self.variables = kwargs
        self.root_frame.set_variables(**kwargs)


class CoordinateFrame(object):
    def __init__(self, variables={}):
        self.variables = variables
        self.children = []
        self.pos = [0, 0, 0]
        self.euler = [0, 0, 0]
        self.__rotation = None

    def add_child(self, CoordinateFrame):
        self.children.append(CoordinateFrame)

    def toNatural(self, cartesian):
        raise NotImplementedError()

    def toCartesian(self, natural):
        raise NotImplementedError()

    def getLocalFrameRotation(self, natural_location):
        raise NotImplementedError()

    @property
    def pos(self):
        return [self.variables[p] if isinstance(p, str) else p
                for p in self.__pos]

    @pos.setter
    def pos(self, pos):
        self.__pos = pos

    @property
    def euler(self):
        return [self.variables[p] if isinstance(p, str) else p
                for p in self.__euler]

    @euler.setter
    def euler(self, euler):
        self.__euler = euler

    @property
    def rotation(self):
        if self.__rotation is None:
            # Build new from euler angles
            roll = Rotation.fromAngle(deg2rad(self.euler[0]), "x")
            pitch = Rotation.fromAngle(deg2rad(self.euler[1]), "y")
            yaw = Rotation.fromAngle(deg2rad(self.euler[2]), "z")
            return yaw * pitch * roll
        return self.__rotation

    @rotation.setter
    def rotation(self, rotation):
        self.__rotation = rotation

    def __str__(self):
        return "Name: {}\nPosition: {}\nRotation: {}".format(
                self.name, self.pos, self.rotation)

    def get_frame(self, framename):
        if self.name == framename:
            return self
        for child in self.children:
            try:
                return child.get_frame(framename)
            except FrameNotFoundError:
                pass
        raise FrameNotFoundError

    def find_path_to_frame(self, framename):
        if self.name == framename:
            return []
        for child in self.children:
            try:
                path = child.find_path_to_frame(framename)
                path = [child] + path
                return path
            except FrameNotFoundError:
                pass
        raise FrameNotFoundError()

    def get_transform_child(self, child):
        nat_position = child.pos
        position = self.toCartesian(nat_position)
        rotation = child.rotation
        transform = (Translation.fromPoint(position) *
                     self.getLocalFrameRotation(nat_position) *
                     rotation)
        return transform

    def collect_transform(self, path):
        if not path:
            return Rotation.Identity()
        child_to_self = self.get_transform_child(path[0])
        final_to_child = path[0].collect_transform(path[1:])
        return child_to_self * final_to_child

    def update(self, **kwargs):
        self.variables.update(kwargs)
        for child in self.children:
            child.update(**kwargs)

    def set_variables(self, **kwargs):
        self.variables = kwargs
        for child in self.children:
            child.set_variables(**kwargs)


class CartesianCoordinateFrame(CoordinateFrame):
    def toNatural(self, cartesian):
        return cartesian

    def toCartesian(self, natural):
        return natural

    def getLocalFrameRotation(self, natural_location):
        return Rotation.Identity()


class OblateEllipsoidFrame(CoordinateFrame):
    def __init__(self, a, b, *args):
        super().__init__(*args)
        self.axes = (a, b)

    @property
    def axes(self):
        """
        length of axes (unit: meters)

        :returns: (longer, shorter) axes == (xy axes, z axis)
        """
        return self.a, self.b

    @axes.setter
    def axes(self, ab):
        a, b = ab
        self.a, self.b = (a, b)
        self.excentricity2 = (a**2 - b**2) / a**2
        self.excentricityt2 = (a**2 - b**2) / b**2

    def _Nlat(self, slat):
        return self.a / (1 - self.excentricity2*slat**2)**.5

    def toCartesian(self, natural):
        # follows http://www.navipedia.net/index.php/Ellipsoidal_and_Cartesian_Coordinates_Conversion # noqa: E501
        lat, lon, height = natural
        rlat = lat * np.pi / 180
        rlon = lon * np.pi / 180
        slat = np.sin(rlat)
        clat = np.cos(rlat)
        slon = np.sin(rlon)
        clon = np.cos(rlon)
        Nlat = self._Nlat(slat)
        xbase = (Nlat + height) * clat
        x = xbase * clon
        y = xbase * slon
        z = (Nlat * (1 - self.excentricity2) + height) * slat
        return [x, y, z]

    def toNatural(self, cartesian, iterations=10):
        # follows http://www.navipedia.net/index.php/Ellipsoidal_and_Cartesian_Coordinates_Conversion # noqa: E501
        x, y, z = cartesian
        rlon = np.arctan2(y, x)
        xbase = (x**2 + y**2)**.5
        eps2 = self.excentricity2
        rlat = np.arctan2(z, (1 + eps2) * xbase)
        for i in range(iterations):
            Nlat = self._Nlat(np.sin(rlat))
            height = xbase / np.cos(rlat) - Nlat
            rlat = np.arctan2(z, (1 - eps2 * (Nlat / (Nlat + height))) * xbase)
        return [180*rlat/np.pi, 180*rlon/np.pi, height]

    def getLocalFrameRotation(self, natural_location):
        return (Rotation.fromAngle(-np.pi/2, 'y') *
                Rotation.fromAngle(deg2rad(natural_location[1]), 'x') *
                Rotation.fromAngle(-deg2rad(natural_location[0]), 'y'))
        # !!! Why is cpp and py version different in order?
        # return reduce(M.mmul, (Ry(-M.deg2rad(position.natural[0])),
        #                        Rx(M.deg2rad(position.natural[1])),
        #                        Ry(-M.pi/2)))


class Transform(object):
    def __init__(self, M):
        assert(isinstance(M, np.ndarray))
        self.M = M

    def apply_point(self, x, y, z):
        p = np.stack([x, y, z, np.ones_like(x)])
        result = np.tensordot(self.M, p, (1, 0))
        return result[0], result[1], result[2]

    def apply_direction(self, x, y, z):
        p = np.stack([x, y, z, np.zeros_like(x)])
        result = np.tensordot(self.M, p, (1, 0))
        return result[0], result[1], result[2]

    def __mul__(self, o):
        assert(isinstance(o, Transform))
        if self.__class__ == o.__class__:
            return self.__class__(self.M @ o.M)
        return Transform(self.M @ o.M)

    def __str__(self):
        return repr(self.M)

    def __eq__(self, o):
        return self.M == self.o

    def invert(self):
        return self.__class__(np.linalg.inv(self.M))


class Rotation(Transform):
    @classmethod
    def fromAngle(cls, ang, axis):
        M = np.eye(4)
        if axis == 'x':
            M[1, 1] = np.cos(ang)
            M[2, 1] = np.sin(ang)
            M[1, 2] = -np.sin(ang)
            M[2, 2] = np.cos(ang)
        if axis == 'y':
            M[0, 0] = np.cos(ang)
            M[0, 2] = np.sin(ang)
            M[2, 0] = -np.sin(ang)
            M[2, 2] = np.cos(ang)
        if axis == 'z':
            M[0, 0] = np.cos(ang)
            M[1, 0] = np.sin(ang)
            M[0, 1] = -np.sin(ang)
            M[1, 1] = np.cos(ang)
        return cls(M)

    @classmethod
    def Identity(cls):
        M = np.eye(4)
        return cls(M)

    def invert(self):
        newM = self.M.copy()
        newM = newM.T
        return self.__class__(newM)


class Translation(Transform):
    @classmethod
    def fromPoint(cls, p):
        M = np.eye(4)
        M[0, 3] = p[0]
        M[1, 3] = p[1]
        M[2, 3] = p[2]
        return cls(M)

    def invert(self):
        newM = self.M.copy()
        newM[0, 3] = -newM[0, 3]
        newM[1, 3] = -newM[1, 3]
        newM[2, 3] = -newM[2, 3]
        return self.__class__(newM)
