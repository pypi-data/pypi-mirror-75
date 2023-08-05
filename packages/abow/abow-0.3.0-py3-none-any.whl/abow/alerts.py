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

import collections

# the queue of alerts
_queue = collections.deque()


def add(lvl, txt):
    '''Add a new alert to the queue
    '''
    global _queue
    _queue.append((lvl, txt))


def get_list():
    '''Return the list of alerts
    '''
    global _queue
    return list(_queue)


def clear():
    '''Clear the queue of alerts
    '''
    global _queue
    _queue.clear()
