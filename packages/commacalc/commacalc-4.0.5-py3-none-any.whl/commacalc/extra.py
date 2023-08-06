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

import math as _math

import commacalc.units


def cbrt(x):
    """Return the cube root of x."""
    return x**(1/3)


def dsp_wh(ratio, diag):
    """Find width and height of a screen, given its ratio and diagonal.

    :param ratio:   Ratio of a screen (e.g. 16/9)
    :param diag:    Diagonal of a screen in inches

    :returns:       Width and Height of a screen in metres
    """
    cosinus = _math.cos(_math.atan(ratio))
    h = diag * cosinus * commacalc.units.inch * 100
    w = h * ratio
    return w, h


def sign(x, value=1):
    """Mathematical signum function.

    :param x:       Object of investigation
    :param value:   The size of the signum (defaults to 1)

    :returns:       Plus or minus value
    """
    return -value if x < 0 else value


def _isqrt(n):
    """isqrt(n)

    :returns:   floor(sqrt(n))

    DEPRECATED: since 3.8 in standard library
    """
    if not isinstance(n, int):
        raise TypeError('an int is required')
    if n < 0:
        raise ValueError('math domain error')

    guess = (n >> n.bit_length() // 2) + 1
    result = (guess + n // guess) // 2
    while abs(result - guess) > 1:
        guess = result
        result = (guess + n // guess) // 2
    while result * result > n:
        result -= 1
    return result


def nCk(n, k):
    """
    DEPRECATED: since 3.8 in standard library as `comb`
    """
    f = _math.factorial
    return f(n) // (f(k) * f(n-k))
