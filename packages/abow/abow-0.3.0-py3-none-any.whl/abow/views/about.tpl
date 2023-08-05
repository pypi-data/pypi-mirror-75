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
% #_ Do not translate A Bottle of Wiki
<h1 class="font-weight-bold mb-4">{{_('About A Bottle of Wiki')}}</h1>
<div class="text-justify mb-5">
<p><img src="{{get_url('static', filepath='img/abow.svg')}}" alt="A Bottle of Wiki logo"class="mr-2">{{version}}</p>
<h2>{{_('License')}}</h2>
<p>Copyright (C) 2020 <a href="mailto:benoit.monin@gmx.fr">Benoît Monin</a></p>
% #_ Do not translate A Bottle of Wiki
<p>{{_('''A Bottle of Wiki is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.''')}}</p>
<h2>{{_('Included software')}}</h2>
% #_ Do not translate A Bottle of Wiki
<p>{{_('A Bottle of Wiki includes the following software:')}}</p>
<ul>
<li><a href="https://getbootstrap.com/">Bootstrap</a> {{_('version')}} 4.4.1. {{_('Released under MIT license.')}}</li>
<li><a href="https://jquery.com/">Jquery slim</a> {{_('version')}} 3.4.1. {{_('Released under MIT license.')}}</li>
<li><a href="http://www.jacklmoore.com/autosize/">Autosize</a> {{_('version')}} 4.0.2+gd32047a. {{_('Released under MIT license.')}}</li>
<li>{{_('Modified Markdown extensions tables and wikilinks')}}. <a href="https://python-markdown.github.io/">Python-Markdown</a> {{_('version')}} 3.2.1. {{_('Released under BSD license.')}}</li>
</ul>
<h2>{{_('Configuration')}}</h2>
%for k, v in sorted(config.items()):
%if k.startswith('abow.') and config.meta_get(k, 'help'):
<div class="card mb-2">
<div class="card-header d-flex">
<span class="font-weight-bold mr-auto">{{k.split('.')[1]}}</span>
<small class="text-muted ml-3">{{_(config.meta_get(k, 'help'))}}</small>
</div>
<div class="card-body">
<p class="card-text {{'' if v else 'text-muted font-italic'}}">{{v if v else _('empty')}}</p>
</div>
</div>
%end
%end
</div>
