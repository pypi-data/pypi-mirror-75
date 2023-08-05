% # A Bottle of Wiki — personal wiki
% # SPDX-License-Identifier: AGPL-3.0-or-later
% # Copyright (C) 2020  Benoît Monin <benoit.monin@gmx.fr>
% #
% # This program is free software: you can redistribute it and/or modify
% # it under the terms of the GNU Affero General Public License as
% # published by the Free Software Foundation, either version 3 of the
% # License, or (at your option) any later version.
% #
% # This program is distributed in the hope that it will be useful,
% # but WITHOUT ANY WARRANTY; without even the implied warranty of
% # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
% # GNU Affero General Public License for more details.
% #
% # You should have received a copy of the GNU Affero General Public License
% # along with this program.  If not, see <https://www.gnu.org/licenses/>.
%
%rebase('index.tpl')
<div class="alert alert-dark mt-4" role="alert">
<h1 class="font-weight-bold mb-4">{{title}}</h1>
<p>{{err_body}}</p>
<hr />
<p class="mb-0">{{!_('Go <a class="alert-link" href="javascript:history.back()">Back</a> to the previous page or head to the <a class="alert-link" href="{}" >home page</a>.').format(get_url('root'))}}</p>
<div>
