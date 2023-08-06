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

from math import *                      # noqa: F401, F403
import sys as _sys
import re as _re
import numbers as _numbers

import commacalc.currencies as _currencies
import commacalc.units as _units
import commacalc.pretty_number as _pretty_number

from commacalc.currencies import *      # noqa: F401, F403
from commacalc.units import *           # noqa: F401, F403
from commacalc.extra import *           # noqa: F401, F403
# from commacalc.primes import *


_PREFIX_FUNCTIONS = {
    '√': "sqrt",
    '∛': "cbrt",
}

_POSTFIX_FUNCTIONS = {
    '²': "**2",
    '³': "**3",
}


def _replace_functions(input_):
    """replace √123 or √(123) with sqrt(123)"""
    for symbol, value in _PREFIX_FUNCTIONS.items():
        input_ = _re.sub(
            rf'{symbol}(-?[\d.]+)',
            rf'{value}(\1)',
            input_
        )
    for symbol, value in _PREFIX_FUNCTIONS.items():
        input_ = _re.sub(
            rf'{symbol}\(',
            rf'{value}(',
            input_
        )

    for symbol, value in _POSTFIX_FUNCTIONS.items():
        input_ = _re.sub(
            rf'([\d.]+){symbol}',
            rf'(\1){value}',
            input_
        )
    for symbol, value in _POSTFIX_FUNCTIONS.items():
        input_ = _re.sub(
            rf'\){symbol}',
            rf'){value}',
            input_
        )

    return input_


def main():
    input_ = ''.join(_sys.argv[1:])

    input_ = _replace_functions(input_)
    input_ = _currencies.replace_symbols(input_)
    input_ = _units.replace_symbols(input_)

    result = eval(input_)
    if isinstance(result, _numbers.Real):
        result = _pretty_number.PrettyNumber(result)
    print(result)


if __name__ == '__main__':
    _sys.exit(main())
