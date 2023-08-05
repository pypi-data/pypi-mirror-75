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
%import urllib.parse
<h1 class="font-weight-bold text-muted text-right font-italic mb-5">{{title}}</h1>
<div class="abow_view text-justify mb-5">
%if html:
{{!html}}
%else:
<p>{{_('The page {} does not exist yet:').format(pagename)}}
<a class="wikilink" href="../edit/{{urllib.parse.quote(pagename)}}">{{_('create it')}}</a>.</p>
%end
</div>
%if tags:
<div class="mb-4 d-print-none">
% for tag in tags:
<a href="../tag/{{urllib.parse.quote(tag)}}" class="badge badge-pill badge-secondary">{{tag}}</a>
% end
</div>
%end
