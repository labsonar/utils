"""
This module defines enums for various physical units along with methods to convert them. Each enum
represents a category of units (Distance, Time, Speed, etc.). Additionally, the classes provide a
string representation of the unit in symbol-formatted output.
"""
import enum
import abc
import math


class Prefix(enum.Enum):
    """ Enum to represent prefix of units. """
    BASE = 0
    y = 1
    YOCTO = 1
    z = 2
    ZEPTO = 2
    a = 3
    ATTO = 3
    f = 4
    FEMTO = 4
    p = 5
    PICO = 5
    n = 6
    NANO = 6
    u = 7
    MICRO = 7
    m = 8
    MILLI = 8
    k = 9
    KILO = 9
    M = 10
    MEGA = 10
    G = 11
    GIGA = 11
    T = 12
    TERA = 12
    P = 13
    PETA = 13
    E = 14
    EXA = 14
    Z = 15
    ZETTA = 15
    Y = 16
    YOTTA = 16
    Ki = 17
    KIBI = 17
    Mi = 18
    MEBI = 18
    Gi = 19
    GIBI = 19
    Ti = 20
    TEBI = 20
    Pi = 21
    PEBI = 21
    Ei = 22
    EXBI = 22
    Zi = 23
    ZEBI = 23
    Yi = 24
    YOBI = 24

    def as_float(self) -> float:
        """
        return the prefix as float value.

        Returns:
            float: Float equivalent to the prefix, i.e., 1e3 for k, 1ed-3 for m.
        """
        convert_list = [1,
                        1E-24,
                        1E-21,
                        1E-18,
                        1E-15,
                        1E-12,
                        1E-9,
                        1E-6,
                        1E-3,
                        1E3,
                        1E6,
                        1E9,
                        1E12,
                        1E15,
                        1E18,
                        1E21,
                        1E24,
                        2**10,
                        2**20,
                        2**30,
                        2**40,
                        2**50,
                        2**60,
                        2**70,
                        2**80]
        return convert_list[self.value]

    def __str__(self) -> str:
        """ Returns the prefix as str """
        if self == Prefix.BASE:
            return ''
        return self.name.lower()

class Unity():
    """ Class to represent a basic unity. """

    @abc.abstractmethod
    def convert_to_base(self) -> float:
        """ Converts some unity to its default format. """

    @abc.abstractmethod
    def __str__(self) -> str:
        """ Returns the unit as symbol """

class Distance(Unity, enum.Enum):
    """ Enum to represent distance units. """
    M = 0
    METER = 0
    YD = 1
    YARD = 1
    NM = 2
    NAUTICAL_MILE = 2
    FT = 3
    FOOT = 3

    def convert_to_base(self) -> float:
        """
        Converts the distance unit to meters.

        Returns:
            float: The conversion value to the base unit (meters).
        """
        convert_list = [1,
                        0.9144,
                        1852,
                        0.3048]
        return convert_list[self.value]

    def __str__(self) -> str:
        """ Returns the unit as str """
        return self.name.lower()

class Time(Unity, enum.Enum):
    """ Enum to represent time units. """
    S = 0
    SECOND = 0
    M = 1
    MINUTE = 1
    H = 2
    HOUR = 2

    def convert_to_base(self) -> float:
        """
        Converts the time unit to seconds.

        Returns:
            float: The conversion value to the base unit (seconds).
        """
        convert_list = [1,
                        60,
                        3600]
        return convert_list[self.value]

    def __str__(self) -> str:
        """ Returns the unit as str """
        return self.name.lower()

class Frequency(Unity, enum.Enum):
    """ Enum to represent frequency units. """
    HZ = 0
    HERTZ = 0
    RPM = 1
    ROTATIONS_PER_MINUTE = 1

    def convert_to_base(self) -> float:
        """
        Converts the frequency unit to hertz.

        Returns:
            float: The conversion value to the base unit (hertz).
        """
        convert_list = [1,
                        1/60]
        return convert_list[self.value]

    def __str__(self) -> str:
        """ Returns the unit as str """
        convert_list = ["Hz",
                        "RPM"]
        return convert_list[self.value]

class Speed(Unity, enum.Enum):
    """ Enum to represent speed units. """
    M_S = 0
    METER_PER_SECOND = 0
    KM_H = 1
    KILOMETER_PER_HOUR = 1
    KT = 2
    KNOT = 2

    def convert_to_base(self) -> float:
        """
        Converts the speed unit to meters per second.

        Returns:
            float: The conversion value to the base unit (meters per second).
        """
        convert_list = [1,
                        1000.0/3600,
                        1852.0/3600]
        return convert_list[self.value]

    def __str__(self) -> str:
        """ Returns the unit as str """
        return self.name.lower().replace('_', '/')

class Acceleration(Unity, enum.Enum):
    """ Enum to represent acceleration units. """
    M_S2 = 0
    METER_PER_SECOND_SQUARE = 0
    KM_H2 = 1
    KILOMETER_PER_HOUR_SQUARE = 1
    KT_H = 2
    KNOT_PER_HOUR = 2

    def convert_to_base(self) -> float:
        """
        Converts the acceleration unit to meters per second squared.

        Returns:
            float: The conversion value to the base unit (meters per second squared).
        """
        convert_list = [1,
                        1000.0/(3600*3600),
                        1852.0/(3600*3600)]
        return convert_list[self.value]

    def __str__(self) -> str:
        """ Returns the unit as str """
        convert_list = ["m/s^2",
                        "km/h^2",
                        "kt/h"]
        return convert_list[self.value]

class Angle(Unity, enum.Enum):
    """ Enum to represent angle units. """
    RAD = 0
    RADIAN = 0
    DEG = 1
    DEGREE = 1

    def convert_to_base(self) -> float:
        """
        Converts the angle unit to radians.

        Returns:
            float: The conversion value to the base unit (radians).
        """
        convert_list = [1,
                        math.pi/180]
        return convert_list[self.value]

    def __str__(self) -> str:
        """ Returns the unit as str """
        convert_list = ["rad",
                        "°"]
        return convert_list[self.value]

class AngularVelocity(Unity, enum.Enum):
    """ Enum to represent angular velocity units. """
    RAD_S = 0
    RADIAN_PER_SECOND = 0
    DEG_S = 1
    DEGREE_PER_SECOND = 1

    def convert_to_base(self) -> float:
        """
        Converts the angular velocity unit to radians per second.

        Returns:
            float: The conversion value to the base unit (radians per second).
        """
        convert_list = [1,
                        math.pi/180]
        return convert_list[self.value]

    def __str__(self) -> str:
        """ Returns the unit as str """
        convert_list = ["rad/s",
                        "°/s"]
        return convert_list[self.value]

class Density(Unity, enum.Enum):
    """ Enum to represent density units. """
    G_CM3 = 0
    KG_M3 = 1

    def convert_to_base(self) -> float:
        """
        Converts the density unit to grams per cubic centimeter (g/cm³).

        Returns:
            float: The conversion factor to the base unit (g/cm³).
        """
        convert_list = [1,
                        1e-3]
        return convert_list[self.value]

    def __str__(self) -> str:
        """ Returns the unit as string """
        unit_list = ["g/cm^3", "kg/m^3"]
        return unit_list[self.value]

class Sensitivity(Unity, enum.Enum):
    """ Enum to represent sensitivity units (dB re 1 V/μPa). """
    DB_RE_1_VOLT_PER_MICROPAL = 0
    DB_V_P_UPA = 0

    def convert_to_base(self) -> float:
        """ Converts the sensitivity unit to (dB re 1 V/μPa). """
        convert_list = [1]
        return convert_list[self.value]

    def __str__(self) -> str:
        return self.name.replace('_', ' (re 1 V/μPa)')
