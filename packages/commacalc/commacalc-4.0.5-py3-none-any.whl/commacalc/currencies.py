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

import os as _os
import pickle as _pickle
from stat import ST_MTIME as _ST_MTIME
from time import time as _time
import threading as _threading


_SYMBOLS = {
    '$': "USD",
    '£': "GBP",
    '€': "EUR",
    '¥': "CNY",
    '₽': "RUB",
}


def replace_symbols(input_):
    """replace €123 with EUR*123"""
    for symbol, code in _SYMBOLS.items():
        input_ = input_.replace(symbol, code+'*')
    return input_


_RATES_URLS = [
    ("https://www.cnb.cz/cs/financni_trhy/devizovy_trh/"
     "kurzy_devizoveho_trhu/denni_kurz.txt"),
    ("https://www.cnb.cz/cs/financni_trhy/devizovy_trh/"
     "kurzy_ostatnich_men/kurzy.txt")
]
_RATES_PICKLE = _os.path.expanduser("~/.rates.pickle")

rates = {}


def _download():
    import httplib2
    import csv
    import io

    h = httplib2.Http()

    for url in _RATES_URLS:
        response, content = h.request(url)

        reader = csv.reader(io.StringIO(content.decode()), delimiter='|')
        next(reader)    # header
        next(reader)    # column names
        for row in reader:
            try:
                country, currname, amount, currcode, rate = row
                rates[currcode] = float(rate.replace(',', '.')) / int(amount)
            except ValueError:
                "Invalid row"


def _dump():
    with open(_RATES_PICKLE, mode="wb") as f:
        _pickle.dump(rates, f)


def _dl_n_dump():
    _download()
    _dump()


def _load():
    global rates

    with open(_RATES_PICKLE, mode="rb") as f:
        rates = _pickle.load(f)

    globals().update(rates)


def rate(currency):
    """Get exchange rate (ČNB)

    :param currency:    Code of currency (e.g. "USD" or "EUR")
    :returns:           Exchange rate in CZK
    """
    if not rates:
        if not _os.path.exists(_RATES_PICKLE):
            _download()
            _threading.Thread(target=_dump).start()
        elif _time() - _os.stat(_RATES_PICKLE)[_ST_MTIME] > 86400:
            _load()
            _threading.Thread(target=_dl_n_dump).start()
        else:
            _load()

    return rates[currency]


# curencies
dollar = rate("USD")
euro = rate("EUR")
sterling = rate("GBP")
ruble = rate("RUB")
yen = rate("JPY")


if __name__ == "__main__":
    print(f"USD: {USD}")    # noqa: F821
    print(f"EUR: {EUR}")    # noqa: F821
    print(f"VND: {VND}")    # noqa: F821
