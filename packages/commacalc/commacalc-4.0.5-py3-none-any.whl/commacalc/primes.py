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

import math
import itertools
from collections import Counter


class PrimesList:
    """Structure with list of primes, expanding as they're requested.
    """
    def _gen(self):
        composites = {}     # maps composites to their prime divisors
        # yield 2
        for i in itertools.count(start=3, step=2):
            prime_divisor = composites.pop(i, None)

            if prime_divisor:   # set next composite
                i += prime_divisor
                while i in composites or i & 1 == 0:
                    i += prime_divisor
                composites[i] = prime_divisor
            else:               # i is prime
                composites[i*i] = i
                self.lst.append(i)
                self.set.add(i)
                # print("g{}".format(i), end='')
                yield i

    def __init__(self):
        self.lst = [2]
        self.set = {2}
        self.gen = self._gen()

    def __iter__(self):
        """for i in primes"""
        yield from self.lst
        # yield from self.gen
        while True:
            yield next(self.gen)

    def __contains__(self, item):
        """331 in primes"""
        if self.lst[-1] >= item:
            return item in self.set

        for p in self.gen:
            if p == item:
                return True
            if p > item:
                return False
            # else continue

    def __getitem__(self, key):
        """primes[10:20]"""
        if isinstance(key, int):
            hi_idx = key
        if isinstance(key, slice):
            hi_idx = max(key.start or 0, key.stop or 0)

        while hi_idx >= len(self.lst):
            next(self.gen)
        return self.lst[key]


primes = PrimesList()


def factorize(number):
    """Factorize number to prime numbers.
    """
    primes_iter = iter(primes)
    prime = next(primes_iter)
    square_root = math.isqrt(number)

    while prime <= square_root:
        quotient, remainder = divmod(number, prime)

        if remainder:
            prime = next(primes_iter)
        else:
            yield prime
            number = quotient
            if number == 1:
                return
    yield number


_sups_table = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


def _to_sups(x):
    return str(x).translate(_sups_table)


def factorize_str(number):
    counter = Counter(factorize(number)).items()

    return "{} = {}".format(number, " × ".join(
        "{}{}".format(base, "" if exp == 1 else _to_sups(exp))
        for base, exp in sorted(counter)
    ))


if __name__ == "__main__":
    print(factorize_str(128))
    print(factorize_str(9))
    print(3 in primes)
    print(primes[4:])
    print(factorize_str(9699690))
    print(primes[4:])
