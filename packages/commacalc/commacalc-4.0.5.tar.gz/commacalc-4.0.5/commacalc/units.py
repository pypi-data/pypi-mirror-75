# Copyright (C) 2016  Pachol, Vojtěch <pacholick@gmail.com>
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/>.

import re as _re
import math as _math


_SYMBOLS = {
    'da': "10",     # deca
    'h': "100",     # hecto
    'k': "1000",    # kilo
    'M': "1000000",     # mega
    'G': "1000000000",  # giga
    'T': "1000000000000",   # tera
    'P': "1000000000000000",    # peta
    'E': "1000000000000000000",     # exa
    'Z': "1000000000000000000000",  # zetta
    'Y': "1000000000000000000000000",   # yotta
    'R': "1000000000000000000000000000",    # ronna
    'Q': "1000000000000000000000000000000",     # quecca

    'd': "0.1",     # deci
    'c': "0.01",    # centi
    'm': "0.001",   # mili
    'μ': "0.000001",    # micro (greek mu)
    'µ': "0.000001",    # micro (micro sign)
    'u': "0.000001",    # micro (‘u’ is also allowed)
    'n': "0.000000001",     # nano
    'p': "0.000000000001",  # pico
    'f': "0.000000000000001",   # femto
    'a': "0.000000000000000001",    # atto
    'z': "0.000000000000000000001",     # zepto
    'y': "0.000000000000000000000001",  # yocto
    'r': "0.000000000000000000000000001",   # ronto
    'q': "0.000000000000000000000000000001",    # quecto

    '°': "(π/180)",
}


def replace_symbols(input_):
    """replace 123k with 1000*123"""
    for symbol, value in _SYMBOLS.items():
        input_ = _re.sub(
            r'(\d+){}'.format(symbol),
            r'\1*{}'.format(value),
            input_
        )
    return input_


def from_fahrenheit(fahrenheit):
    """Convert Fahrenheits to Centigrade."""
    return (fahrenheit - 32)*5/9


C = from_fahrenheit


def to_fahrenheit(c):
    """Convert Centigrade to Fahrenheits."""
    return c*9/5 + 32


def prefix(x, dimension=1):
    """Give the number an appropriate SI prefix.

    :param x:   Too big or too small number.
    :returns:   String containing a number between 1 and 1000 and SI prefix.
    """
    if x == 0:
        return "0  "

    length = _math.floor(_math.log10(abs(x)))
    if abs(length) > 30:
        length = int(_math.copysign(30, length))

    div, mod = divmod(length, 3*dimension)
    return "{:.3g} {}".format(
        x*10**(-length + mod),
        " kMGTPEZYRQqryzafpnµm"[div])


# maths
π = _math.pi
φ = (1 + _math.sqrt(5))/2


# time
days_in_year = 365.242189       # tropical year
# days_in_year = 365.256363004    # sideral year
seconds_in_day = 86400
year = yr = seconds_in_year = days_in_year*seconds_in_day


# physics
c = 299792458
"""Speed of light in vacuum (exact) [ m s⁻¹ ]"""
G = 6.6740831e-11
"""Gravitational constant [ m³ kg⁻¹ s⁻² ]"""
h = 6.62607015e-34
"""Planck constant (exact) [ m² kg s⁻¹ ]"""
ħ = h/(2*π)
"""Reduced Planck constant [ m² kg s⁻¹ ]"""
k_e = 8.9875517873681764e9
"""Coulomb constant (exact) [ m³ kg s⁻² C⁻² ]"""
k_B = 1.380649e-23
"""Boltzmann constant (exact) [ m² kg K⁻¹ s⁻² ]"""
N_A = 6.02214076e23
"""Avogadro constant (exact) [ mol⁻¹ ]"""
g = 9.80665
"""Standard gravity (exact) [ m s⁻² ]"""

eV = 1.602176634e-19
"""Electronvolt (exact) [ m² kg s⁻² ]"""
q = eV
"""Elementary charge (exact) [ s A ]"""

µ_0 = 4*π*1e-7
"""Permeability of Vacuum [ kg m s⁻² A⁻² ]"""
ε_0 = 1/(µ_0*c**2)
"""Permittivity of Vacuum [ s⁴ A² kg⁻¹ m⁻³ ]"""
α = q**2/(4*π*ε_0*ħ*c)
"""Fine-structure constant [ ]"""


# astronomy
ly = 9460730472580800
"""Light-year (exact) [ m ]"""
au = 149597870700
"""Astronomical unit (exact) [ m ]"""
pc = 648000/π*au
"""Parsec (exact) [ m ]"""


# imperial units to metric (exact)
inch = 0.0254
foot = ft = 0.3048
yard = yd = 0.9144
mile = mi = 1609.344
acre = ac = 4046.8564224
pound = lb = 0.45359237
# imperial units to metric (not exact)
barrel = 0.15897
gallon_uk = 0.004546090
gallon_us = 0.003785412
ounce_int = oz = 0.028349523125
ounce_troy = toz = ozt = 0.0311034768


if __name__ == "__main__":
    print(prefix(0.9, 2))
