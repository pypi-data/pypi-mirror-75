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
<h1 class="font-weight-bold mb-4">{{title}} <span class="badge badge-secondary align-bottom ml-2">{{len(pages_list)}}</span></h1>
<ul>
% for page in pages_list:
<li><a href="../view/{{urllib.parse.quote(page)}}">{{page}}</a></li>
% end
</ul>
%if defined('page_exists'):
<hr>
%if page_exists:
<p>{{_('View the page')}} <a class="wikilink" href="../view/{{urllib.parse.quote(pagename)}}">{{pagename}}</a>.</p>
%else:
<p>{{_('The page {} does not exist yet:').format(pagename)}}
<a class="wikilink" href="../edit/{{urllib.parse.quote(pagename)}}">{{_('create it')}}</a>.</p>
%end
%end
