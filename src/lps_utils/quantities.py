"""
Module for representing quantities with units, prefixes, and powers.

This module provides classes for defining physical quantities with units and prefixes,
along with methods to convert between units and prefixes.
"""
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
        return Quantity(self.magnitude + other.get(self.unity, self.prefix),
                        self.unity,
                        self.prefix,
                        self.power)

    def __sub__(self, other: 'Quantity') -> 'Quantity':
        self._check_compatibility(other)
        return Quantity(self.magnitude - other.get(self.unity, self.prefix),
                        self.unity,
                        self.prefix,
                        self.power)

    def __mul__(self, other) -> 'Quantity':

        if isinstance(other, type(self)):
            self._check_compatibility(other)
            return Quantity(self.magnitude * other.get(self.unity, self.prefix),
                        self.unity,
                        self.prefix,
                        self.power + other.power)

        if isinstance(other, (int, float)):
            return Quantity(self.magnitude * other,
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

            return Quantity(self.magnitude / other.get(self.unity, self.prefix),
                        self.unity,
                        self.prefix,
                        self.power - other.power)

        if isinstance(other, (int, float)):
            return Quantity(self.magnitude / other,
                        self.unity,
                        self.prefix,
                        self.power)

        raise NotImplementedError(f'__truediv__ for {type(self)} and {type(other)}')

    def __rtruediv__(self, scale: float) -> 'Quantity':
        return Quantity(scale / self.magnitude,
                        self.unity,
                        self.prefix,
                        self.power * -1)

    def __pow__(self, exponent: float) -> 'Quantity':
        return Quantity(
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
            return Speed.m_s(self.get_m() / other.get_s())

        if isinstance(other, Speed):
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
            return Distance.m(self.get_s() * other.get_m_s())

        if isinstance(other, Frequency):
            return self / (1/other)

        return super().__mul__(other)

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

        return super().__truediv__(other)
