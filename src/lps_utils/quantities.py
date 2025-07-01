"""
Module for representing quantities with units, prefixes, and powers.

This module provides classes for defining physical quantities with units and prefixes,
along with methods to convert between units and prefixes.
"""
import time
import datetime
import re
import math
import enum
import lps_utils.unity as lps_unity

class Quantity():
    """ Base class to represent a physical quantity with a magnitude, unit, prefix, and power. """

    def __init__(self, magnitude: float,
                 unity: lps_unity.Unity,
                 prefix: lps_unity.Prefix = lps_unity.Prefix.BASE,
                 power: int = 1) -> None:
        """
        Initializes a Quantity instance.

        Args:
            magnitude (float): The magnitude of the unity.
            unity (lps_unity.Unity): The unity
            prefix (lps_unity.Prefix, optional): The prefix for the unit.
                Defaults to lps_unity.Prefix.base.
            power (int, optional): The power of the unit. Defaults to 1.
        """
        self.magnitude = magnitude
        self.unity = unity
        self.prefix = prefix
        self.power = power

    def __abs__(self):
        """
        Return a copy of the object with positive magnitude.
        Supports subclassing by using self.__class__.
        """
        return self.__class__(
            magnitude=abs(self.magnitude),
            unity=self.unity,
            prefix=self.prefix,
            power=self.power
        )

    def __str__(self) -> str:
        if self.power == 1:
            return f'{self.magnitude} {self.prefix}{self.unity}'
        return f'{self.magnitude} {self.prefix}({self.unity})^{self.power}'

    def __repr__(self):
        return self.__str__()

    def get(self,
            unity: lps_unity.Unity,
            prefix: lps_unity.Prefix = lps_unity.Prefix.BASE) -> float:
        """ Returns the magnitude of the unity converted to the specified unity and prefix. """
        return self.magnitude * \
            Quantity.convert_unity(self.unity, unity, self.power) * \
            Quantity.convert_prefix(self.prefix, prefix, self.power)

    @staticmethod
    def convert_prefix(prefix_in: lps_unity.Prefix, prefix_out: lps_unity.Prefix, power: int):
        """ Convert a prefix in another. """
        return prefix_in.as_float()/prefix_out.as_float() ** power

    @staticmethod
    def convert_unity(unity_in: lps_unity.Unity, unity_out: lps_unity.Unity, power: int):
        """ Convert a unity in another. """
        if isinstance(unity_in, type(unity_out)) or isinstance(unity_out, type(unity_in)):
            return (unity_in.convert_to_base()/unity_out.convert_to_base()) ** power
        raise UnboundLocalError(f'Convertion from {type(unity_in)} to {type(unity_out)}')

    def _check_compatibility(self, other: 'Quantity') -> bool:
        if isinstance(self.unity, type(other)):
            raise UnboundLocalError(f'Unity {self.unity} not compatible with {other.unity}')
        if self.power != other.power:
            raise UnboundLocalError(f'Incompatible power {self.power} with {other.power}')
        return True

    def __hash__(self):
        return hash((self.magnitude, self.unity.value, self.prefix.value, self.power))

    def __eq__(self, other: 'Quantity') -> bool:
        self._check_compatibility(other)
        return self.get(self.unity, self.prefix) == other.get(self.unity, self.prefix)

    def __ne__(self, other: 'Quantity') -> bool:
        self._check_compatibility(other)
        return not self.__eq__(other)

    def __gt__(self, other: 'Quantity') -> bool:
        self._check_compatibility(other)
        return self.get(self.unity, self.prefix) > other.get(self.unity, self.prefix)

    def __lt__(self, other: 'Quantity') -> bool:
        self._check_compatibility(other)
        return self.get(self.unity, self.prefix) < other.get(self.unity, self.prefix)

    def __ge__(self, other: 'Quantity') -> bool:
        self._check_compatibility(other)
        return self.get(self.unity, self.prefix) >= other.get(self.unity, self.prefix)

    def __le__(self, other: 'Quantity') -> bool:
        self._check_compatibility(other)
        return self.get(self.unity, self.prefix) <= other.get(self.unity, self.prefix)

    def __add__(self, other: 'Quantity') -> 'Quantity':
        self._check_compatibility(other)
        return self.__class__(self.get(self.unity, self.prefix) + other.get(self.unity, self.prefix),
                        self.unity,
                        self.prefix,
                        self.power)

    def __sub__(self, other: 'Quantity') -> 'Quantity':
        self._check_compatibility(other)
        return self.__class__(self.get(self.unity, self.prefix) - other.get(self.unity, self.prefix),
                        self.unity,
                        self.prefix,
                        self.power)

    def __mul__(self, other) -> 'Quantity':

        if isinstance(other, type(self)):
            self._check_compatibility(other)
            return self.__class__(self.get(self.unity, self.prefix) * other.get(self.unity, self.prefix),
                        self.unity,
                        self.prefix,
                        self.power + other.power)

        if isinstance(other, (int, float)):
            return self.__class__(self.magnitude * other,
                        self.unity,
                        self.prefix,
                        self.power)

        raise NotImplementedError(f'__mul__ for {type(self)} and {type(other)}')

    def __rmul__(self, other: float) -> 'Quantity':
        return self.__mul__(other)

    def __truediv__(self, other) -> 'Quantity':

        if isinstance(other, type(self)):

            self._check_compatibility(other)
            if self.power == other.power:
                return self.get(self.unity, self.prefix) / other.get(self.unity, self.prefix)

            return self.__class__(self.get(self.unity, self.prefix) / other.get(self.unity, self.prefix),
                        self.unity,
                        self.prefix,
                        self.power - other.power)

        if isinstance(other, (int, float)):
            return self.__class__(self.magnitude / other,
                        self.unity,
                        self.prefix,
                        self.power)

        raise NotImplementedError(f'__truediv__ for {type(self)} and {type(other)}')

    def __rtruediv__(self, scale: float) -> 'Quantity':
        return self.__class__(scale / self.magnitude,
                        self.unity,
                        self.prefix,
                        self.power * -1)

    def __pow__(self, exponent: float) -> 'Quantity':
        aux = self.get(self.unity, lps_unity.Prefix.BASE)
        return self.__class__(
            aux ** exponent,
            self.unity,
            lps_unity.Prefix.BASE,
            self.power * exponent
        )


class Distance(Quantity):
    """ Class to represent Distance with predefined units. """

    def __init__(self,
                 magnitude: float,
                 unity: lps_unity.Distance,
                 prefix: lps_unity.Prefix = lps_unity.Prefix.BASE,
                 power: int = 1):
        super().__init__(magnitude, unity, prefix, power)

    def get_m(self) -> float:
        """ Returns the magnitude in meters. """
        return self.get(lps_unity.Distance.M)

    def get_km(self) -> float:
        """ Returns the magnitude in kilometers. """
        return self.get(lps_unity.Distance.M, lps_unity.Prefix.k)

    def get_nm(self) -> float:
        """ Returns the magnitude in nautical miles. """
        return self.get(lps_unity.Distance.NM)

    def get_yd(self) -> float:
        """ Returns the magnitude in yards. """
        return self.get(lps_unity.Distance.YD)

    def get_ft(self) -> float:
        """ Returns the magnitude in foots. """
        return self.get(lps_unity.Distance.FT)

    @classmethod
    def m(cls, m: float) -> 'Distance':
        """ Creates a Distance instance with the magnitude in meters. """
        return cls(m, lps_unity.Distance.M)

    @classmethod
    def km(cls, km: float) -> 'Distance':
        """ Creates a Distance instance with the magnitude in kilometers. """
        return cls(km, lps_unity.Distance.M, lps_unity.Prefix.k)

    @classmethod
    def nm(cls, nm: float) -> 'Distance':
        """ Creates a Distance instance with the magnitude in nautical miles. """
        return cls(nm, lps_unity.Distance.NM)

    @classmethod
    def yd(cls, yd: float) -> 'Distance':
        """ Creates a Distance instance with the magnitude in yards. """
        return cls(yd, lps_unity.Distance.YD)

    @classmethod
    def kyd(cls, kyd: float) -> 'Distance':
        """ Creates a Distance instance with the magnitude in kilometers of yards. """
        return cls(kyd, lps_unity.Distance.YD, lps_unity.Prefix.k)

    @classmethod
    def ft(cls, ft: float) -> 'Distance':
        """ Creates a Distance instance with the magnitude in foots. """
        return cls(ft, lps_unity.Distance.FT)

    def __mul__(self, other) -> 'Quantity':
        if isinstance(other, Frequency):
            return self / (1/other)

        return super().__mul__(other)

    def __truediv__(self, other) -> 'Quantity':
        if isinstance(other, Time):
            if self.power == other.power:
                return Speed.m_s(self.get_m() / other.get_s())

            if 2 * self.power == other.power:
                return Acceleration.m_s2(self.get_m() / other.get_s())

        if isinstance(other, Speed):
            if self.power == other.power:
                return Time.s(self.get_m() / other.get_m_s())

        return super().__truediv__(other)

class Time(Quantity):
    """ Class to represent time with predefined units. """

    def __init__(self,
                 magnitude: float,
                 unity: lps_unity.Time,
                 prefix: lps_unity.Prefix = lps_unity.Prefix.BASE,
                 power: int = 1) -> None:
        super().__init__(magnitude, unity, prefix, power)

    def get_s(self) -> float:
        """ Returns the magnitude in seconds. """
        return self.get(lps_unity.Time.S)

    def get_ms(self) -> float:
        """ Returns the magnitude in milliseconds. """
        return self.get(lps_unity.Time.S, lps_unity.Prefix.m)

    def get_us(self) -> float:
        """ Returns the magnitude in microseconds. """
        return self.get(lps_unity.Time.S, lps_unity.Prefix.u)

    def get_ns(self) -> float:
        """ Returns the magnitude in nanoseconds. """
        return self.get(lps_unity.Time.S, lps_unity.Prefix.n)

    def get_minutes(self) -> float:
        """ Returns the magnitude in minutes. """
        return self.get(lps_unity.Time.M)

    def get_hours(self) -> float:
        """ Returns the magnitude in hours. """
        return self.get(lps_unity.Time.H)

    @classmethod
    def s(cls, seconds: float) -> 'Time':
        """ Creates a Time instance with the magnitude in seconds. """
        return cls(seconds, lps_unity.Time.S)

    @classmethod
    def ms(cls, ms: float) -> 'Time':
        """ Creates a Time instance with the magnitude in milliseconds. """
        return cls(ms, lps_unity.Time.S, lps_unity.Prefix.m)

    @classmethod
    def us(cls, us: float) -> 'Time':
        """ Creates a Time instance with the magnitude in microseconds. """
        return cls(us, lps_unity.Time.S, lps_unity.Prefix.u)

    @classmethod
    def ns(cls, ns: float) -> 'Time':
        """ Creates a Time instance with the magnitude in nanoseconds. """
        return cls(ns, lps_unity.Time.S, lps_unity.Prefix.n)

    @classmethod
    def m(cls, minutes: float) -> 'Time':
        """ Creates a Time instance with the magnitude in minutes. """
        return cls(minutes, lps_unity.Time.M)

    @classmethod
    def h(cls, hours: float) -> 'Time':
        """ Creates a Time instance with the magnitude in hours. """
        return cls(hours, lps_unity.Time.H)

    def __rtruediv__(self, scale: float) -> 'Quantity':
        return Frequency(scale / self.get_s(),
                        lps_unity.Frequency.HZ,
                        lps_unity.Prefix.BASE,
                        self.power)

    def __truediv__(self, other) -> 'Quantity':
        if isinstance(other, Frequency):
            return self * (1/other)
        return super().__truediv__(other)

    def __mul__(self, other) -> 'Quantity':

        if isinstance(other, Speed):
            if self.power == other.power:
                return Distance.m(self.get_s() * other.get_m_s())

        if isinstance(other, Frequency):
            return self / (1/other)

        if isinstance(other, Acceleration):
            return other * self

        return super().__mul__(other)

    def __add__(self, other):
        if isinstance(other, Timestamp):
            return Timestamp.ns(self.get_ns() + other.get_ns())

        return super().__add__(other)

class Frequency(Quantity):
    """ Class to represent frequency with predefined units. """

    def __init__(self,
                 magnitude: float,
                 unity: lps_unity.Frequency,
                 prefix: lps_unity.Prefix = lps_unity.Prefix.BASE,
                 power: int = 1) -> None:
        super().__init__(magnitude, unity, prefix, power)

    def get_hz(self) -> float:
        """ Returns the magnitude in hertz. """
        return self.get(lps_unity.Frequency.HZ)

    def get_khz(self) -> float:
        """ Returns the magnitude in kilo hertz. """
        return self.get(lps_unity.Frequency.HZ, lps_unity.Prefix.k)

    def get_rpm(self) -> float:
        """ Returns the magnitude in rotations per minute. """
        return self.get(lps_unity.Frequency.RPM)

    @classmethod
    def hz(cls, hz: float) -> 'Frequency':
        """ Creates a Frequency instance with the magnitude in hertz. """
        return cls(hz, lps_unity.Frequency.HZ)

    @classmethod
    def khz(cls, hz: float) -> 'Frequency':
        """ Creates a Frequency instance with the magnitude in kilo hertz. """
        return cls(hz, lps_unity.Frequency.HZ, lps_unity.Prefix.k)

    @classmethod
    def rpm(cls, rpm: float) -> 'Frequency':
        """ Creates a Frequency instance with the magnitude in rotations per minute. """
        return cls(rpm, lps_unity.Frequency.RPM)

    def __rtruediv__(self, scale: float) -> 'Quantity':
        return Time(scale / self.get_hz(),
                        lps_unity.Time.S,
                        lps_unity.Prefix.BASE,
                        self.power)

    def __truediv__(self, other) -> 'Quantity':
        if isinstance(other, Time):
            return self * (1/other)
        return super().__truediv__(other)

class Speed(Quantity):
    """ Class to represent speed with predefined units. """

    def __init__(self,
                 magnitude: float,
                 unity: lps_unity.Speed,
                 prefix: lps_unity.Prefix = lps_unity.Prefix.BASE,
                 power: int = 1) -> None:
        super().__init__(magnitude, unity, prefix, power)

    def get_m_s(self) -> float:
        """ Returns the magnitude in meters per second. """
        return self.get(lps_unity.Speed.M_S)

    def get_km_h(self) -> float:
        """ Returns the magnitude in kilometers per hour. """
        return self.get(lps_unity.Speed.KM_H)

    def get_kt(self) -> float:
        """ Returns the magnitude in knots. """
        return self.get(lps_unity.Speed.KT)

    @classmethod
    def m_s(cls, m_s: float) -> 'Speed':
        """ Creates a Speed instance with the magnitude in meters per second. """
        return cls(m_s, lps_unity.Speed.M_S)

    @classmethod
    def km_h(cls, km_h: float) -> 'Speed':
        """ Creates a Speed instance with the magnitude in kilometers per hour. """
        return cls(km_h, lps_unity.Speed.KM_H)

    @classmethod
    def kt(cls, kt: float) -> 'Speed':
        """ Creates a Speed instance with the magnitude in knots. """
        return cls(kt, lps_unity.Speed.KT)

    def __mul__(self, other) -> 'Quantity':

        if isinstance(other, Time):
            return other * self

        return super().__mul__(other)

    def __truediv__(self, other) -> 'Quantity':
        if isinstance(other, Distance):
            return Frequency.hz(self.get_m_s()/ other.get_m())

        if isinstance(other, Frequency):
            return self*(1/other)

        if isinstance(other, Time):
            if self.power == other.power:
                return Acceleration.m_s2(self.get_m_s() / other.get_s())

        return super().__truediv__(other)

class Acceleration(Quantity):
    """ Class to represent Acceleration with predefined units. """

    def __init__(self,
                 magnitude: float,
                 unity: lps_unity.Acceleration,
                 prefix: lps_unity.Prefix = lps_unity.Prefix.BASE,
                 power: int = 1):
        super().__init__(magnitude, unity, prefix, power)

    def get_m_s2(self) -> float:
        """ Returns the magnitude in meters per second squared. """
        return self.get(lps_unity.Acceleration.M_S2)

    def get_km_h2(self) -> float:
        """ Returns the magnitude in kilometers per hour squared. """
        return self.get(lps_unity.Acceleration.KM_H2)

    def get_kt_h(self) -> float:
        """ Returns the magnitude in knots per hour. """
        return self.get(lps_unity.Acceleration.KT_H)

    @classmethod
    def m_s2(cls, m_s2: float) -> 'Acceleration':
        """ Creates an Acceleration instance with the magnitude in meters per second squared. """
        return cls(m_s2, lps_unity.Acceleration.M_S2)

    @classmethod
    def km_h2(cls, km_h2: float) -> 'Acceleration':
        """ Creates an Acceleration instance with the magnitude in kilometers per hour squared. """
        return cls(km_h2, lps_unity.Acceleration.KM_H2)

    @classmethod
    def kt_h(cls, kt_h: float) -> 'Acceleration':
        """ Creates an Acceleration instance with the magnitude in knots per hour. """
        return cls(kt_h, lps_unity.Acceleration.KT_H)

    def __mul__(self, other) -> 'Quantity':
        if isinstance(other, Time):
            if self.power == other.power:
                return Speed.m_s(self.get_m_s2() * other.get_s())

            if 2 * self.power == other.power:
                return Distance.m(self.get_m_s2() * other.get_s())

        return super().__mul__(other)

    # def __truediv__(self, other) -> 'Quantity':
    #     return super().__truediv__(other)

class DMS():
    """ Class to represent Degree-Minute-Second (DMS) angle representation. """

    def __init__(self, degree: float = 0, minute: float = 0, second: float = 0) -> None:
        self.degree = degree
        self.minute = minute
        self.second = second

    def __str__(self) -> str:
        return self.to_string()

    def to_string(self, precision: int = 0, show_signal: bool = False) -> str:
        """ return current angle in DMS representation with the given second precision

        Args:
            precision (int, optional): Number of decimal places for seconds. Defaults to 0.
            show_signal (bool, optional): Show negative number. Defaults to False
                (standard behavior for latitude/longitude).

        Returns:
            str: DMS string in format -> 43°38'51.000"
        """
        aux_degree = self.degree if show_signal else abs(self.degree)
        format_spec = "02.0f" if precision == 0 else f"{precision + 3}.{precision}f"
        return f"{aux_degree:02.0f}°{self.minute:02.0f}'{self.second:{format_spec}}\""

    def get_degrees(self) -> float:
        """ Return angle with degrees with decimal precision. """
        return self.degree + math.copysign(self.minute/60.0 + self.second/3600.0, self.degree)

    @classmethod
    def by_degree(cls, degree: float) -> 'DMS':
        """ Class constructor based on degree with decimal precision. """
        deg = math.floor(degree) if (degree > 0) else math.ceil(degree)
        degree = abs(degree) - abs(deg)
        minute = math.floor(degree*60)
        degree = degree * 60 - minute
        sec = degree * 60

        return cls(deg, minute, sec)

    @classmethod
    def by_string(cls, dms: str) -> 'DMS':
        """ Class constructor based on DMS string format. """
        values = [0, 0, 0]

        pieces = re.split("[°'\"]", dms)
        for i in range(min(len(pieces), len(values))):
            try:
                values[i] = float(pieces[i])
            except ValueError:
                pass

        if dms.endswith('S') or dms.endswith('W'):
            values[0] *= -1

        return cls(values[0], values[1], values[2])

class Angle(Quantity):
    """ Class to represent Angle with predefined units. """

    def __init__(self,
                 magnitude: float,
                 unity: lps_unity.Angle,
                 prefix: lps_unity.Prefix = lps_unity.Prefix.BASE,
                 power: int = 1):
        super().__init__(magnitude, unity, prefix, power)

    def get_rad(self) -> float:
        """ Returns the magnitude in radians. """
        return self.get(lps_unity.Angle.RAD)

    def get_deg(self) -> float:
        """ Returns the magnitude in degrees. """
        return self.get(lps_unity.Angle.DEG)

    def get_dms(self) -> DMS:
        """ Return string in DMS format. """
        return DMS.by_degree(self.get_deg())

    @classmethod
    def rad(cls, rad: float) -> 'Angle':
        """ Creates an Angle instance with the magnitude in radians. """
        return cls(rad, lps_unity.Angle.RAD)

    @classmethod
    def deg(cls, deg: float) -> 'Angle':
        """ Creates an Angle instance with the magnitude in degrees. """
        return cls(deg, lps_unity.Angle.DEG)

    @classmethod
    def dms(cls, dms: DMS) -> 'Angle':
        """ Creates an Angle instance with the magnitude in dms. """
        return cls(dms.get_degrees(), lps_unity.Angle.DEG)

    def __truediv__(self, other) -> 'Quantity':
        if isinstance(other, Time):
            return AngularVelocity.rad_s(self.get_rad() / other.get_s())
        return super().__truediv__(other)

class BearingReference(enum.Enum):
    """ Class to represent reference of a bearing in
        east counterclockwise (ECCW)
        west clockwise (NCW). """
    ECCW = 0
    EAST_COUNTERCLOCKWISE = 0
    NCW = 1
    WEST_CLOCKWISE = 1

class Bearing(Angle):
    """ Class to represent a Angle between 0-360. """

    def __init__(self,
                 angle: Angle,
                 reference: BearingReference):
        angle = Bearing.coerce(Bearing.set_reference(angle, reference))
        super().__init__(angle.get_rad(), lps_unity.Angle.RAD)

    @staticmethod
    def set_reference(angle: Angle, reference: BearingReference) -> Angle:
        """ Return Angle in ECCW. """
        return Angle.rad(angle.get_rad() if (reference == BearingReference.ECCW) \
                         else (math.pi/2.0 - angle.get_rad()))

    @staticmethod
    def coerce(angle: Angle) -> Angle:
        """ Coerce an angle in range from 0 to 2pi. """
        return Angle.rad(math.fmod(angle.get_rad(), 2*math.pi) + \
                         (0.0 if (angle.get_rad() >= 0) else (2*math.pi) ))

    @classmethod
    def eccw_deg(cls, degree: float) -> 'Bearing':
        """ Class constructor in eccw. """
        return cls(Angle.deg(degree), BearingReference.ECCW)

    @classmethod
    def eccw_rad(cls, radian: float) -> 'Bearing':
        """ Class constructor in eccw. """
        return cls(Angle.rad(radian), BearingReference.ECCW)

    @classmethod
    def ncw_deg(cls, degree: float) -> 'Bearing':
        """ Class constructor in ncw. """
        return cls(Angle.deg(degree), BearingReference.NCW)

    @classmethod
    def ncw_rad(cls, radian: float) -> 'Bearing':
        """ Class constructor in ncw. """
        return cls(Angle.rad(radian), BearingReference.NCW)

    def get_by_reference(self, angle: lps_unity.Angle, reference: BearingReference):
        """ Return bearing in unity and reference desired. """
        return Bearing.coerce(Bearing.set_reference(self,reference)).get(angle)

    def get_eccw_deg(self) -> float:
        """ Return bearing in eccw and degree. """
        return self.get_by_reference(lps_unity.Angle.DEGREE, BearingReference.ECCW)

    def get_eccw_rad(self) -> float:
        """ Return bearing in eccw and radian. """
        return self.get_by_reference(lps_unity.Angle.RADIAN, BearingReference.ECCW)

    def get_ncw_deg(self) -> float:
        """ Return bearing in ncw and degree. """
        return self.get_by_reference(lps_unity.Angle.DEGREE, BearingReference.NCW)

    def get_ncw_rad(self) -> float:
        """ Return bearing in ncw and radian. """
        return self.get_by_reference(lps_unity.Angle.RADIAN, BearingReference.NCW)

    def __str__(self) -> str:
        return f"{self.get_eccw_deg()} deg_eccw"

    def __add__(self, other: 'Quantity') -> 'Quantity':
        self._check_compatibility(other)
        if isinstance(other, RelativeBearing):
            return Bearing.eccw_rad(self.get_eccw_rad() + other.get_ccw_rad())

        if isinstance(other, Bearing):
            return Bearing.eccw_rad(self.get_eccw_rad() + other.get_eccw_rad())

        if isinstance(other, Angle):
            return Bearing.eccw_rad(self.get_eccw_rad() + other.get_rad())

        my_self = Angle.rad(self.get_eccw_rad())
        return my_self + other

    def __sub__(self, other: 'Quantity') -> 'Quantity':
        self._check_compatibility(other)
        if isinstance(other, RelativeBearing):
            return Bearing.eccw_rad(self.get_eccw_rad() - other.get_ccw_rad())

        if isinstance(other, Bearing):
            return RelativeBearing.ccw_rad(self.get_eccw_rad() - other.get_eccw_rad())

        if isinstance(other, Angle):
            return Bearing.eccw_rad(self.get_eccw_rad() - other.get_rad())

        my_self = Angle.rad(self.get_eccw_rad())
        return my_self - other

    def __mul__(self, other) -> 'Quantity':
        my_self = Angle.rad(self.get_eccw_rad())
        aux = my_self * other

        if isinstance(aux, Angle):
            return Bearing.eccw_rad(aux.get_rad())
        return aux

    def __truediv__(self, other) -> 'Quantity':
        my_self = Angle.rad(self.get_eccw_rad())
        aux = my_self / other

        if isinstance(aux, Angle):
            return Bearing.eccw_rad(aux.get_rad())
        return aux

class RelativeBearingReference(enum.Enum):
    """ Class to represent reference of a relative_bearing. """
    CCW = 0
    COUNTERCLOCKWISE = 0
    CW = 1
    CLOCKWISE = 1

class RelativeBearing(Bearing):
    """ Class to represent a Angle between 0-360. """

    def __init__(self,
                 angle: Angle,
                 reference: RelativeBearingReference):
        angle = RelativeBearing.set_reference(angle, reference)
        super().__init__(angle, BearingReference.ECCW)

    @staticmethod
    def set_reference(angle: Angle, reference: RelativeBearingReference) -> Angle:
        """ Return Angle in CCW. """
        return Angle.rad(angle.get_rad() if (reference == RelativeBearingReference.CCW) \
                         else (math.pi/2.0 - angle.get_rad()))

    @staticmethod
    def coerce(angle: Angle) -> Angle:
        """ Coerce an angle in range from 0 to 2pi. """
        return Angle.rad(math.fmod(angle.get_rad(), 2*math.pi) + \
                         (0.0 if (angle.get_rad() >= 0) else (2*math.pi) ))

    @classmethod
    def ccw_deg(cls, degree: float) -> 'RelativeBearing':
        """ Class constructor in ccw. """
        return cls(Angle.deg(degree), RelativeBearingReference.CCW)

    @classmethod
    def ccw_rad(cls, radian: float) -> 'RelativeBearing':
        """ Class constructor in ccw. """
        return cls(Angle.rad(radian), RelativeBearingReference.CCW)

    @classmethod
    def cw_deg(cls, degree: float) -> 'RelativeBearing':
        """ Class constructor in cw. """
        return cls(Angle.deg(degree), RelativeBearingReference.CW)

    @classmethod
    def cw_rad(cls, radian: float) -> 'RelativeBearing':
        """ Class constructor in cw. """
        return cls(Angle.rad(radian), RelativeBearingReference.CW)

    def get_by_reference(self, angle: lps_unity.Angle, reference: RelativeBearingReference):
        """ Return bearing in unity and reference desired. """
        return Bearing.coerce(RelativeBearing.set_reference(self,reference)).get(angle)

    def get_ccw_deg(self) -> float:
        """ Return bearing in ccw and degree. """
        return self.get_by_reference(lps_unity.Angle.DEGREE, RelativeBearingReference.CCW)

    def get_ccw_rad(self) -> float:
        """ Return bearing in ccw and radian. """
        return self.get_by_reference(lps_unity.Angle.RADIAN, RelativeBearingReference.CCW)

    def get_cw_deg(self) -> float:
        """ Return bearing in cw and degree. """
        return self.get_by_reference(lps_unity.Angle.DEGREE, RelativeBearingReference.CW)

    def get_cw_rad(self) -> float:
        """ Return bearing in cw and radian. """
        return self.get_by_reference(lps_unity.Angle.RADIAN, RelativeBearingReference.CW)

    def __add__(self, other: 'Quantity') -> 'Quantity':
        self._check_compatibility(other)
        if isinstance(other, Bearing):
            return Bearing.eccw_rad(self.get_ccw_rad() + other.get_eccw_rad())

        if isinstance(other, (RelativeBearing, Angle)):
            return RelativeBearing.ccw_rad(self.get_ccw_rad() + other.get_rad())

        my_self = Angle.rad(self.get_eccw_rad())
        return my_self - other

    def __sub__(self, other: 'Quantity') -> 'Quantity':
        self._check_compatibility(other)

        if isinstance(other, Bearing):
            return Bearing.eccw_rad(self.get_ccw_rad() - other.get_eccw_rad())

        if isinstance(other, (RelativeBearing, Angle)):
            return RelativeBearing.ccw_rad(self.get_ccw_rad() - other.get_rad())

        my_self = Angle.rad(self.get_eccw_rad())
        return my_self - other

    def __mul__(self, other) -> 'Quantity':
        my_self = Angle.rad(self.get_eccw_rad())
        aux = my_self * other

        if isinstance(aux, Angle):
            return RelativeBearing.ccw_rad(aux.get_rad())
        return aux

    def __truediv__(self, other) -> 'Quantity':
        my_self = Angle.rad(self.get_eccw_rad())
        aux = my_self / other

        if isinstance(aux, Angle):
            return RelativeBearing.ccw_rad(aux.get_rad())
        return aux

    def __str__(self) -> str:
        return f"{self.get_ccw_deg()} deg_ccw"

class Latitude(Angle):
    """ Class to represent Latitude with predefined units. """

    def __init__(self,
                 magnitude: float,
                 unity: lps_unity.Angle,
                 prefix: lps_unity.Prefix = lps_unity.Prefix.BASE,
                 power: int = 1):
        super().__init__(magnitude, unity, prefix, power)

        if (self.get_rad() < -math.pi/2.0) or (self.get_rad() > math.pi/2.0):
            raise ValueError(f"invalid_latitude: {self.get_rad()}")

    def get_hemisphere(self) -> str:
        """ Return N or S given the current angle. """
        return "N" if self.get_deg()>0 else "S"

    def __str__(self) -> str:
        return f"{self.get_dms()} {self.get_hemisphere()}"

class Longitude(Angle):
    """ Class to represent Longitude with predefined units. """

    def __init__(self,
                 magnitude: float,
                 unity: lps_unity.Angle,
                 prefix: lps_unity.Prefix = lps_unity.Prefix.BASE,
                 power: int = 1):
        super().__init__(magnitude, unity, prefix, power)

        if (self.get_rad() < -math.pi) or (self.get_rad() > math.pi):
            raise ValueError(f"invalid_latitude: {self.get_rad()}")

    def get_hemisphere(self) -> str:
        """ Return E or W given the current angle. """
        return "E" if self.get_deg()>0 else "W"

    def __str__(self) -> str:
        return f"{self.get_dms()} {self.get_hemisphere()}"

class AngularVelocity(Quantity):
    """ Class to represent Angular Velocity with predefined units. """

    def __init__(self,
                 magnitude: float,
                 unity: lps_unity.AngularVelocity,
                 prefix: lps_unity.Prefix = lps_unity.Prefix.BASE,
                 power: int = 1):
        super().__init__(magnitude, unity, prefix, power)

    def get_rad_s(self) -> float:
        """ Returns the magnitude in radians per second. """
        return self.get(lps_unity.AngularVelocity.RAD_S)

    def get_deg_s(self) -> float:
        """ Returns the magnitude in degrees per second. """
        return self.get(lps_unity.AngularVelocity.DEG_S)

    @staticmethod
    def rad_s(rad_s: float) -> 'AngularVelocity':
        """ Creates an AngularVelocity instance with the magnitude in radians per second. """
        return AngularVelocity(rad_s, lps_unity.AngularVelocity.RAD_S)

    @staticmethod
    def deg_s(deg_s: float) -> 'AngularVelocity':
        """ Creates an AngularVelocity instance with the magnitude in degrees per second. """
        return AngularVelocity(deg_s, lps_unity.AngularVelocity.DEG_S)

    def __mul__(self, other) -> 'Quantity':
        if isinstance(other, Time):
            return Angle.rad(self.get_rad_s() * other.get_s())

        return super().__mul__(other)

class Density(Quantity):
    """ Class to represent Density with predefined units. """

    def __init__(self,
                 magnitude: float,
                 unity: lps_unity.Density,
                 prefix: lps_unity.Prefix = lps_unity.Prefix.BASE,
                 power: int = 1):
        super().__init__(magnitude, unity, prefix, power)

    def get_kg_m3(self) -> float:
        """ Returns the magnitude in kilograms per cubic meter. """
        return self.get(lps_unity.Density.KG_M3)

    def get_g_cm3(self) -> float:
        """ Returns the magnitude in grams per cubic centimeter. """
        return self.get(lps_unity.Density.G_CM3)

    @staticmethod
    def kg_m3(kg_m3: float) -> 'Density':
        """ Creates a Density instance with the magnitude in kilograms per cubic meter. """
        return Density(kg_m3, lps_unity.Density.KG_M3)

    @staticmethod
    def g_cm3(g_cm3: float) -> 'Density':
        """ Creates a Density instance with the magnitude in grams per cubic centimeter. """
        return Density(g_cm3, lps_unity.Density.G_CM3)

class Timestamp:
    """ Class to represent a specific point in time with nanosecond precision. """

    def __init__(self, t=None):
        """
        Args:
            t (int, optional): Time in nanoseconds. Defaults to the current time in nanoseconds.
        """
        if t is None:
            t = int(time.time_ns())  # Current time in nanoseconds
        self._t = t

    @staticmethod
    def s(seconds: float) -> 'Timestamp':
        """ Creates a Timestamp instance from the given time in seconds. """
        return Timestamp(int(seconds * 1e9))

    @staticmethod
    def ns(nanoseconds: int) -> 'Timestamp':
        """ Creates a Timestamp instance from the given time in nanoseconds. """
        return Timestamp(nanoseconds)

    @staticmethod
    def iso8601(string: str) -> 'Timestamp':
        """ Creates a Timestamp instance from an ISO 8601 formatted string. """
        dt = datetime.datetime.fromisoformat(string)
        return Timestamp(int(dt.timestamp() * 1e9))

    def get_time_t(self) -> int:
        """ Returns the time as a Unix timestamp in seconds. """
        return int(self._t / 1e9)

    def get_s(self) -> float:
        """ Returns the time in seconds. """
        return self._t / 1e9

    def get_ns(self) -> int:
        """ Returns the time in nanoseconds. """
        return self._t

    def to_string(self, format_str: str = "%d/%m/%Y %H:%M:%S") -> str:
        """ Converts the Timestamp to a formatted string. """
        dt = datetime.datetime.fromtimestamp(self.get_s())
        return dt.strftime(format_str)

    def to_iso8601(self) -> str:
        """ Converts the Timestamp to an ISO 8601 formatted string. """
        return self.to_string("%Y-%m-%d %H:%M:%S")

    def sleep(self):
        """ Pauses execution until the time represented by this Timestamp is reached. """
        target_time = self._t / 1e9
        current_time = time.time()
        sleep_time = max(0, target_time - current_time)
        time.sleep(sleep_time)

    def __eq__(self, other: 'Timestamp') -> bool:
        return self._t == other._t

    def __ne__(self, other: 'Timestamp') -> bool:
        return self._t != other._t

    def __gt__(self, other: 'Timestamp') -> bool:
        return self._t > other._t

    def __lt__(self, other: 'Timestamp') -> bool:
        return self._t < other._t

    def __ge__(self, other: 'Timestamp') -> bool:
        return self._t >= other._t

    def __le__(self, other: 'Timestamp') -> bool:
        return self._t <= other._t

    def __str__(self) -> str:
        return self.to_string()

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash((self._t))

    def __add__(self, other):
        if isinstance(other, Time):
            return Timestamp.ns(self.get_ns() + other.get_ns())

        raise NotImplementedError(f'Timestamp + {type(other)}')

    def __sub__(self, other):
        if isinstance(other, Timestamp):
            return Time.ns(self.get_ns() - other.get_ns())

        if isinstance(other, Time):
            return Timestamp.ns(self.get_ns() - other.get_ns())

        raise NotImplementedError(f'Timestamp - {type(other)}')

class Sensitivity(Quantity):
    """ Class to represent sensitivity with predefined units. """

    def __init__(self,
                 magnitude: float,
                 unity: lps_unity.Sensitivity,
                 prefix: lps_unity.Prefix = lps_unity.Prefix.BASE,
                 power: int = 1):
        super().__init__(magnitude, unity, prefix, power)

    def get_db_v_p_upa(self) -> float:
        """ Returns the magnitude in kilograms per cubic meter. """
        return self.get(lps_unity.Sensitivity.DB_V_P_UPA)

    @staticmethod
    def db_v_p_upa(value: float) -> 'Sensitivity':
        """ Creates a sensitivity instance with the magnitude in kilograms per cubic meter. """
        return Sensitivity(value, lps_unity.Sensitivity.DB_V_P_UPA)
