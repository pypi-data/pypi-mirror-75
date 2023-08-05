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
%import urllib.parse
<!doctype html>
<html lang="{{lang}}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
<link rel="stylesheet" href="{{get_url('static', filepath='css/bootstrap.min.css')}}">
<link rel="stylesheet" href="{{get_url('static', filepath='css/highlight.css')}}">
<link rel="stylesheet" href="{{get_url('static', filepath='css/abow.css')}}">
<link rel="icon" href="{{get_url('static', filepath='img/abow_32.png')}}" sizes="32x32" type="image/png">
<link rel="icon" href="{{get_url('static', filepath='img/abow_16.png')}}" sizes="16x16" type="image/png">
<title>{{title}} — A Bottle of Wiki</title>
</head>
<body>
<header class="navbar navbar-expand-xl sticky-top navbar-dark bg-dark no-gutters shadow-sm">
<a class="navbar-brand ml-xl-3" href="{{get_url('root')}}">A Bottle of Wiki</a>
<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#abow_menu" aria-controls="abow_menu" aria-expanded="false" aria-label={{!_('"Toggle the navigation bar"')}}>
<span class="navbar-toggler-icon"></span>
</button>
<div class="navbar-collapse col-xl-9 ml-auto pl-xl-5 mr-xl-3 collapse" id="abow_menu">
<ul class="navbar-nav mr-auto">
%include('index_nav_item.tpl', item='view', link='../view/' + urllib.parse.quote(get('pagename','')), display=_('View'), enabled=defined('pagename'))
%include('index_nav_item.tpl', item='edit', link='../edit/' + urllib.parse.quote(get('pagename','')), display=_('Edit'), enabled=defined('pagename'))
<li class="nav-item dropdown">
<a class="nav-link dropdown-toggle" href="#" id="abow_menu_dropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
{{_('More')}}
</a>
<div class="dropdown-menu shadow-sm" aria-labelledby="abow_menu_dropdown">
<a class="dropdown-item" href="{{get_url('search')}}">{{_('List of pages')}}</a>
<div class="dropdown-divider"></div>
%if help_page:
<a class="dropdown-item" href="{{get_url('view', pagename=help_page)}}">{{_('Help')}}</a>
%end
<a class="dropdown-item" href="{{get_url('about')}}">{{_('About')}}</a>
</div>
</li>
</ul>
<form class="form-inline" method="get" action="{{get_url('search')}}">
<input type="search" class="form-control form-control-sm" name="text" aria-label={{!_('"Search"')}} placeholder={{!_('"Search"')}}>
</form>
</div>
</header>
<div class="container-fluid">
<div class="row flex-xl-nowrap">
<div class="col-xl-3 d-none d-xl-block d-print-none">
</div>
<main class="col-12 col-xl-6 px-xl-5 py-3">
%for lvl, txt in alerts.get_list():
<div class="alert alert-{{lvl}} fade show" role="alert">
{{_(txt)}}
<button type="button" class="close" data-dismiss="alert" aria-label={{!_('"Close"')}}>
<span aria-hidden="true">&times;</span>
</button>
</div>
%end
%alerts.clear()
{{!base}}
</main>
<div class="col-xl-3 d-none d-xl-block mt-xl-3 abow_toc d-print-none" id="toc">
%if defined('toc'):
{{!toc}}
%end
</div>
</div>
</div>
<script src="{{get_url('static', filepath='js/jquery.slim.min.js')}}"></script>
<script src="{{get_url('static', filepath='js/bootstrap.bundle.min.js')}}"></script>
%if action == 'edit':
<script src="{{get_url('static', filepath='js/autosize.min.js')}}"></script>
<script src="{{get_url('static', filepath='js/abow.js')}}"></script>
<script>
autosize(document.getElementById('editor_text'));
</script>
%end
</body>
</html>
