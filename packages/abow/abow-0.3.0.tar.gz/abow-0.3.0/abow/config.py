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

try:
    from importlib import resources
except ImportError:
    import importlib_resources as resources
import os
import os.path
import locale
import textwrap

# keep a reference of the configuration
_cfg = None


def _resource_path(res):
    '''Return the absolute path of a package resource

    Note: this only works if the package is not compressed
    '''
    with resources.path(__package__, res) as p:
        return str(p)


def _set_default(cfg):
    '''Set the default configuration values
    '''

    # not shown to the user, internal paths
    cfg.setdefault('abow.locale_path', _resource_path('locale'))
    cfg.setdefault('abow.static_path', _resource_path('static'))
    cfg.setdefault('abow.template_path', _resource_path('views'))

    cfg.meta_set('abow.backend_path', 'help', __('Path to the backend storage'))
    cfg.meta_set('abow.backend_path', 'extra_help',
                 'The backend is where A Bottle of Wiki stores the pages content '
                 'and attributes. It should points to a directory writable by '
                 'the user running the application.')
    cfg.meta_set('abow.backend_path', 'dflt_help', 'the current directory')
    cfg.setdefault('abow.backend_path', os.path.abspath('.'))

    cfg.meta_set('abow.static_url', 'help', __('Base url for the static resources, '
                 'if hosted outside of the app'))
    cfg.meta_set('abow.static_url', 'extra_help',
                 'Define this url if you want to serve the static resources '
                 'directly from a webserver instead of through the application.')
    cfg.meta_set('abow.static_url', 'dflt_help', 'blank, static resources are hosted by the app')
    cfg.setdefault('abow.static_url', '')

    cfg.meta_set('abow.locale', 'help', __('The locale to use'))
    cfg.meta_set('abow.locale', 'extra_help',
                 'Set this value to override the locale settings. '
                 'English and french localization are available.')
    cfg.meta_set('abow.locale', 'dflt_help', 'the current locale from the environnment variables')
    cfg.setdefault('abow.locale', locale.getdefaultlocale()[0] or 'en_US')

    cfg.meta_set('abow.welcome_page', 'help', __('Name of the welcome page '
                 'of the wiki'))
    welcome_page = 'welcome'
    cfg.meta_set('abow.welcome_page', 'extra_help',
                 'The welcome page is the page you reach when connecting '
                 'to the root of the application.')
    cfg.meta_set('abow.welcome_page', 'dflt_help', welcome_page)
    cfg.setdefault('abow.welcome_page', welcome_page)

    cfg.meta_set('abow.help_page', 'help', __('Name of the help page '
                 'of the wiki'))
    help_page = 'usage'
    cfg.meta_set('abow.help_page', 'extra_help',
                 'The help page, if set, is available as a menu entry in the '
                 'navigation bar.')
    cfg.meta_set('abow.help_page', 'dflt_help', help_page)
    cfg.setdefault('abow.help_page', help_page)


def _load_cfg_files(cfg):
    '''Load the configuration files one by one
    '''
    # global configuration
    cfg.load_config(os.path.join('/', 'etc', 'abow', 'config'))

    # user configuration
    if 'XDG_CONFIG_HOME' in os.environ:
        path = [os.path.expandvars('$XDG_CONFIG_HOME')]
    else:
        path = [
            os.path.expanduser('~'),
            '.config'
            ]
    cfg.load_config(os.path.join(*path, 'abow', 'config'))

    # specific configuration
    if 'ABOW_CONFIG' in os.environ:
        cfg.load_config(os.path.expandvars('$ABOW_CONFIG'))


def init(cfg):
    '''Initialize the configuration dictionary

    Set the default value
    '''
    global _cfg
    _cfg = cfg

    _set_default(cfg)
    _load_cfg_files(cfg)


def get(key, default=None):
    '''Return the value of the configuration or the default value
    '''
    global _cfg
    return _cfg.get(key, default)


def print_file():
    '''Print the default configuration file to stdout

    Note: this function is meant to be used independently of the app
    '''
    from bottle import ConfigDict
    cfg = ConfigDict()
    _set_default(cfg)

    # wrapper for multiline comments
    wrapper = textwrap.TextWrapper(initial_indent='# ', subsequent_indent='# ')

    # header
    header = '''\
        -- A Bottle of Wiki configuration file --

        The configuration is read from the following paths:
         * /etc/abow/config
         * $XDG_CONFIG_HOME/abow/config, defaulting to ~/.config/abow/config
         * $ABOW_CONFIG, if defined
        Paths are tried one after one and each configuration file can
        override the settings of the previous ones.
        The settings used can be viewed in the 'about' page.
        '''
    print(textwrap.indent(textwrap.dedent(header), '# ', lambda line: True))
    print('[abow]')

    # the user-modifiable configuration options (i.e. with help text)
    for k in sorted(cfg.keys()):
        if k.startswith('abow.') and cfg.meta_get(k, 'help'):
            print('\n##', cfg.meta_get(k, 'help'))
            print(wrapper.fill(cfg.meta_get(k, 'extra_help', '-')))
            print('# Default value if unset:', cfg.meta_get(k, 'dflt_help'))
            print('#{} ='.format(k.split('.')[1]))
