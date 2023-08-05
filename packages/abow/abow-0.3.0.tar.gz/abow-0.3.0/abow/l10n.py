# A Bottle of Wiki — personal wiki
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2020  Benoît Monin <benoit.monin@gmx.fr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import gettext
import locale

from . import alerts
from . import config


def deferred_gettext(message):
    '''Pass-through to be used before gettext is installed
    '''
    return message


def init():
    '''Setup the locale and install the translation
    '''
    # setup the locale
    try:
        lang = locale.setlocale(locale.LC_ALL, config.get('abow.locale'))
    except locale.Error:
        lang = locale.setlocale(locale.LC_ALL, '')
        alerts.add('warning',
                   __('Invalid locale "{cfg}", using "{dflt}"').format(
                       cfg=config.get('abow.locale'), dflt=lang))

    # let the time in C locale for bottle 'last-modified' html header
    locale.setlocale(locale.LC_TIME, 'C')

    # install the translation
    translation = gettext.translation('abow',
                                      localedir=config.get('abow.locale_path'),
                                      languages=[lang],
                                      fallback=True)
    translation.install()


def get_lang():
    '''Return the html lang attributes from the current locale
    '''
    try:
        return locale.getlocale()[0].replace('_', '-')
    except AttributeError:
        return 'en'
