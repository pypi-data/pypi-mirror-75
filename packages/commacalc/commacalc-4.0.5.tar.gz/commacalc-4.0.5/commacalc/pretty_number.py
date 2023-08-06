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

from colorama import Style
from itertools import zip_longest


class PrettyNumber:
    """Class for making pretty console output of a number."""

    def _swap_color_functions(self):
        p = self.get_color
        self.get_color = self.get_reset
        self.get_reset = p

    def _reset_color_functions(self):
        self.get_color = self.GET_COLOR
        self.get_reset = self.GET_RESET

    def get_color(self):
        """Get highlighting string and swap with reset."""
        self._swap_color_functions()
        return Style.BRIGHT

    def get_reset(self):
        """Get reset string and swap with color."""
        self._swap_color_functions()
        return Style.RESET_ALL

    def split(self):
        """Split the number into its parts."""
        # s = str(self.NUMBER)
        s = '{:.12g}'.format(self.NUMBER)
        self.int_part, self.dot, self.frac_part = s.partition(".")
        _, self.minus, self.int_part = self.int_part.rpartition("-")
        self.frac_part, self.e, self.exponent = self.frac_part.partition("e")
        _, self.exp_plusminus, self.exponent = self.exponent.rpartition("-")
        if self.exp_plusminus == '':
            _, self.exp_plusminus, self.exponent = self.exponent.rpartition(
                "+")

    def color_thousands(self):
        """Color thousands in integer and fractional parts of the number."""
        lst = []
        for i in map(lambda s: ''.join(reversed(s)),
                     zip_longest(*[reversed(self.int_part)]*3, fillvalue='')):
            lst.append(i)
            lst.append(self.get_reset())
        lst.reverse()
        self.int_part = ''.join(lst)

        lst = []
        self._reset_color_functions()
        for i in map(''.join,
                     zip_longest(*[iter(self.frac_part)]*3, fillvalue='')):
            lst.append(self.get_reset())
            lst.append(i)
        lst.append(self.get_reset())
        self.frac_part = ''.join(lst)

    def __init__(self, number):
        """
        :param number: The number to print
        """
        self.GET_COLOR = self.get_color
        self.GET_RESET = self.get_reset

        self.NUMBER = number
        self.split()
        self.color_thousands()

    def __str__(self):
        return ''.join((self.minus, self.int_part, self.dot, self.frac_part,
                        self.e, self.exp_plusminus, self.exponent))
