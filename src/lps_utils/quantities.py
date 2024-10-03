"""
Module for representing quantities with units, prefixes, and powers.

This module provides classes for defining physical quantities with units and prefixes,
along with methods to convert between units and prefixes.
"""
import time
import datetime
import threading
import math

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
            return unity_in.convert_to_base()/unity_out.convert_to_base() ** power
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
        return self.__class__(self.magnitude + other.get(self.unity, self.prefix),
                        self.unity,
                        self.prefix,
                        self.power)

    def __sub__(self, other: 'Quantity') -> 'Quantity':
        self._check_compatibility(other)
        return self.__class__(self.magnitude - other.get(self.unity, self.prefix),
                        self.unity,
                        self.prefix,
                        self.power)

    def __mul__(self, other) -> 'Quantity':

        if isinstance(other, type(self)):
            self._check_compatibility(other)
            return self.__class__(self.magnitude * other.get(self.unity, self.prefix),
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
                return self.magnitude / other.get(self.unity, self.prefix)

            return self.__class__(self.magnitude / other.get(self.unity, self.prefix),
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
        return self.__class__(
            self.magnitude ** exponent,
            self.unity,
            self.prefix,
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

    @staticmethod
    def m(m: float) -> 'Distance':
        """ Creates a Distance instance with the magnitude in meters. """
        return Distance(m, lps_unity.Distance.M)

    @staticmethod
    def km(km: float) -> 'Distance':
        """ Creates a Distance instance with the magnitude in kilometers. """
        return Distance(km, lps_unity.Distance.M, lps_unity.Prefix.k)

    @staticmethod
    def nm(nm: float) -> 'Distance':
        """ Creates a Distance instance with the magnitude in nautical miles. """
        return Distance(nm, lps_unity.Distance.NM)

    @staticmethod
    def yd(yd: float) -> 'Distance':
        """ Creates a Distance instance with the magnitude in yards. """
        return Distance(yd, lps_unity.Distance.YD)

    @staticmethod
    def kyd(kyd: float) -> 'Distance':
        """ Creates a Distance instance with the magnitude in kilometers of yards. """
        return Distance(kyd, lps_unity.Distance.YD, lps_unity.Prefix.k)

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

    @staticmethod
    def s(seconds: float) -> 'Time':
        """ Creates a Time instance with the magnitude in seconds. """
        return Time(seconds, lps_unity.Time.S)

    @staticmethod
    def ms(ms: float) -> 'Time':
        """ Creates a Time instance with the magnitude in milliseconds. """
        return Time(ms, lps_unity.Time.S, lps_unity.Prefix.m)

    @staticmethod
    def us(us: float) -> 'Time':
        """ Creates a Time instance with the magnitude in microseconds. """
        return Time(us, lps_unity.Time.S, lps_unity.Prefix.u)

    @staticmethod
    def ns(ns: float) -> 'Time':
        """ Creates a Time instance with the magnitude in nanoseconds. """
        return Time(ns, lps_unity.Time.S, lps_unity.Prefix.n)

    @staticmethod
    def m(minutes: float) -> 'Time':
        """ Creates a Time instance with the magnitude in minutes. """
        return Time(minutes, lps_unity.Time.M)

    @staticmethod
    def h(hours: float) -> 'Time':
        """ Creates a Time instance with the magnitude in hours. """
        return Time(hours, lps_unity.Time.H)

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

    @staticmethod
    def hz(hz: float) -> 'Frequency':
        """ Creates a Frequency instance with the magnitude in hertz. """
        return Frequency(hz, lps_unity.Frequency.HZ)

    @staticmethod
    def khz(hz: float) -> 'Frequency':
        """ Creates a Frequency instance with the magnitude in kilo hertz. """
        return Frequency(hz, lps_unity.Frequency.HZ, lps_unity.Prefix.k)

    @staticmethod
    def rpm(rpm: float) -> 'Frequency':
        """ Creates a Frequency instance with the magnitude in rotations per minute. """
        return Frequency(rpm, lps_unity.Frequency.RPM)

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

    @staticmethod
    def m_s(m_s: float) -> 'Speed':
        """ Creates a Speed instance with the magnitude in meters per second. """
        return Speed(m_s, lps_unity.Speed.M_S)

    @staticmethod
    def km_h(km_h: float) -> 'Speed':
        """ Creates a Speed instance with the magnitude in kilometers per hour. """
        return Speed(km_h, lps_unity.Speed.KM_H)

    @staticmethod
    def kt(kt: float) -> 'Speed':
        """ Creates a Speed instance with the magnitude in knots. """
        return Speed(kt, lps_unity.Speed.KT)

    def __mul__(self, other) -> 'Quantity':

        if isinstance(other, Time):
            return other * self

        return super().__mul__(other)

    def __truediv__(self, other) -> 'Quantity':
        if isinstance(other, Distance):
            return 1/(other/self)

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

    @staticmethod
    def m_s2(m_s2: float) -> 'Acceleration':
        """ Creates an Acceleration instance with the magnitude in meters per second squared. """
        return Acceleration(m_s2, lps_unity.Acceleration.M_S2)

    @staticmethod
    def km_h2(km_h2: float) -> 'Acceleration':
        """ Creates an Acceleration instance with the magnitude in kilometers per hour squared. """
        return Acceleration(km_h2, lps_unity.Acceleration.KM_H2)

    @staticmethod
    def kt_h(kt_h: float) -> 'Acceleration':
        """ Creates an Acceleration instance with the magnitude in knots per hour. """
        return Acceleration(kt_h, lps_unity.Acceleration.KT_H)

    def __mul__(self, other) -> 'Quantity':
        if isinstance(other, Time):
            if self.power == other.power:
                return Speed.m_s(self.get_m_s2() * other.get_s())

            if 2 * self.power == other.power:
                return Distance.m(self.get_m_s2() * other.get_s())

        return super().__mul__(other)

    # def __truediv__(self, other) -> 'Quantity':
    #     return super().__truediv__(other)


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

    @staticmethod
    def rad(rad: float) -> 'Angle':
        """ Creates an Angle instance with the magnitude in radians. """
        return Angle(rad, lps_unity.Angle.RAD)

    @staticmethod
    def deg(deg: float) -> 'Angle':
        """ Creates an Angle instance with the magnitude in degrees. """
        return Angle(deg, lps_unity.Angle.DEG)

    def __truediv__(self, other) -> 'Quantity':
        if isinstance(other, Time):
            return AngularVelocity.rad_s(self.get_rad() / other.get_s())
        return super().__truediv__(other)


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

    def to_string(self, format: str = "%d/%m/%Y %H:%M:%S") -> str:
        """ Converts the Timestamp to a formatted string. """
        dt = datetime.datetime.fromtimestamp(self.get_s())
        return dt.strftime(format)

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
