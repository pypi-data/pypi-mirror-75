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

import os
import setuptools

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='abow',
    version='0.3.0',
    description='A Bottle of Wiki — personal wiki',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://pypi.org/project/abow/',
    author='Benoît Monin',
    author_email='benoit.monin@gmx.fr',
    license='AGPL-3.0-or-later',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Wiki',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Framework :: Bottle',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='wiki bottle markdown',
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires='>=3.5',
    install_requires=[
        'bottle >= 0.12.0',
        'importlib_metadata ~= 1.0; python_version < "3.8"',
        'importlib_resources ~= 1.0; python_version < "3.7"',
        'Markdown >= 3.2',
        'pymdown-extensions >= 7.0',
    ],
    extras_require={
        'dev': [
            'coverage',
            'flake8',
            'pytest',
            ],
        'extra': ['Pygments >= 2.4'],
    },
)
