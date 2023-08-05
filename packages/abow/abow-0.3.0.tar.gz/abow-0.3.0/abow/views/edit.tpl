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
<div id="preview" class="abow_view text-justify mb-5"></div>
<form method="post">
<div class="btn-toolbar m-1 rounded bg-light shadow-sm" role="toolbar" id="editor_toolbar" aria-label={{!_('"Editor toolbar"')}}>
<div class="btn-group my-1 mr-1" role="group">
<a role="button" class="btn btn-sm btn-secondary" href="javascript:;" onclick="insert_md(this, '**', '**')" title={{!_('"Bold"')}}><strong>{{_('B')}}</strong></a>
<a role="button" class="btn btn-sm btn-secondary" href="javascript:;" onclick="insert_md(this, '_', '_')" title={{!_('"Italic"')}}><em>{{_('I')}}</em></a>
<a role="button" class="btn btn-sm btn-secondary" href="javascript:;" onclick="insert_md(this, '~~', '~~')" title={{!_('"Strike through"')}}><del>{{_('S')}}</del></a>
<a role="button" class="btn btn-sm btn-secondary" href="javascript:;" onclick="insert_md(this, '^^', '^^')" title={{!_('"Underline"')}}><ins>{{_('U')}}</ins></a>
</div>
<div class="btn-group my-1 mr-1" role="group">
<a role="button" class="btn btn-sm btn-secondary" href="javascript:;" onclick="insert_md(this, '# ', '', true, true)" title={{!_('"Heading level 1"')}}>{{_('H1')}}</a>
<a role="button" class="btn btn-sm btn-secondary" href="javascript:;" onclick="insert_md(this, '## ', '', true, true)" title={{!_('"Heading level 2"')}}>{{_('H2')}}</a>
<a role="button" class="btn btn-sm btn-secondary" href="javascript:;" onclick="insert_md(this, '### ', '', true, true)" title={{!_('"Heading level 3"')}}>{{_('H3')}}</a>
<a role="button" class="btn btn-sm btn-secondary" href="javascript:;" onclick="insert_md(this, '#### ', '', true, true)" title={{!_('"Heading level 4"')}}>{{_('H4')}}</a>
</div>
<div class="btn-group my-1 mr-1" role="group">
<a role="button" class="btn btn-sm btn-secondary" href="javascript:;" onclick="insert_md(this, '[...](', ')')" title={{!_('"External link"')}}>{{_('Link')}}</a>
<a role="button" class="btn btn-sm btn-secondary" href="javascript:;" onclick="insert_md(this, '[[', ']]')" title={{!_('"Wiki link"')}}>{{_('Wiki')}}</a>
</div>
<div class="btn-group my-1" role="group">
<button id="editor_toolbar_more" type="button" class="btn btn-sm btn-secondary dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
{{_('More')}}
</button>
<div class="dropdown-menu shadow-sm" id="editor_toolbar_menu" aria-labelledby="editor_toolbar_more">
<a class="dropdown-item" href="javascript:;" onclick="insert_md(this, '`', '`')">{{_('Code')}}</a>
<a class="dropdown-item" href="javascript:;" onclick="insert_md(this, '==', '==')">{{_('Mark')}}</a>
<a class="dropdown-item" href="javascript:;" onclick="insert_md(this, '^', '^')">{{_('Superscript')}}</a>
<a class="dropdown-item" href="javascript:;" onclick="insert_md(this, '~', '~')">{{_('Subscript')}}</a>
<div class="dropdown-divider"></div>
<a class="dropdown-item" href="javascript:;" onclick="insert_md(this, '1. ', '', true, true)">{{_('Ordered list')}}</a>
<a class="dropdown-item" href="javascript:;" onclick="insert_md(this, '* ', '', true, true)">{{_('Unordered list')}}</a>
<div class="dropdown-divider"></div>
<a class="dropdown-item" href="javascript:;" onclick="insert_md(this, '> ', '', true, true)">{{_('Block quote')}}</a>
<a class="dropdown-item" href="javascript:;" onclick="insert_md(this, '```\n', '\n```', true)">{{_('Code block')}}</a>
</div>
</div>
</div>
<div class="form-group">
<textarea class="form-control text-monospace" id="editor_text" name="content">{{content}}</textarea>
</div>
<div class="input-group mb-3">
<div class="input-group-prepend">
<span class="input-group-text" id="inputPageName">{{_('New page name')}}</span>
</div>
<input type="text" class="form-control" aria-describedby="inputPageName" name="new_pagename" autocomplete="off" value="{{pagename}}" pattern="[^/|]*" required title="{{_('Page name cannot be blank and cannot contain \'/\' or \'|\'')}}">
</div>
<div class="input-group">
<div class="input-group-prepend">
<span class="input-group-text" id="inputTags">{{_('Tags')}}</span>
</div>
<input type="text" class="form-control" aria-describedby="inputTags" id="tags_text" name="tags" autocomplete="off" value="{{tags}}">
</div>
%if all_tags:
<div class="border rounded border-top-0 p-2 mb-4">
% for tag in all_tags:
<a href="javascript:add_tag('{{tag}}', 'tags_text')" class="badge badge-pill badge-secondary align-text-bottom" role="button">{{tag}}</a>
% end
</div>
%end
<div class="my-4">
<a class="btn btn-outline-primary" role="button" href="javascript:preview()">{{_('Preview')}}</a>
<button type="submit" class="btn btn-outline-primary">{{_('Save')}}</button>
<a class="btn btn-outline-primary" role="button" href="../view/{{urllib.parse.quote(pagename)}}">{{_('Cancel')}}</a>
</div>
</form>
