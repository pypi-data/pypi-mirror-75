/* A Bottle of Wiki — personal wiki
 * SPDX-License-Identifier: AGPL-3.0-or-later
 * Copyright (C) 2020  Benoît Monin <benoit.monin@gmx.fr>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

/* Preview action is asynchronous
 * Send the value of the source element to the preview action
 * and insert the result in the dst element
 * Scroll to top when done
 */
function preview() {
    var src = document.getElementById("editor_text");
    var dst_html = document.getElementById("preview");
    var dst_toc = document.getElementById("toc");
    var req = new XMLHttpRequest();
    req.responseType = "json";
    req.open("PUT", "../preview", true);
    req.onreadystatechange = function () {
        if (req.readyState !== 4 || req.status !== 200) {
            return;
        }
        var render = req.response;
        dst_html.innerHTML = render.html;
        dst_toc.innerHTML = render.toc;
        window.scroll(0, 0);
    };
    req.send(src.value);
}

/* Add the tag to the intput element pointed by dst
 */
function add_tag(tag, dst) {
    var elem = document.getElementById(dst);
    if (elem.value) {
        elem.value += "; " + tag;
    } else {
        elem.value = tag;
    }
}

/* Insert markdown in the editor textarea around the selected text
 *
 * self: the button being clicked
 * preamble: the text to insert before the selection
 * postamble: the text to insert after the selection
 * nl_out: if true, insert newline around the inserted markdown if needed
 * nl_in: id true, insert markdown around newline in the selection
 */
function insert_md(self, preamble, postamble, nl_out = false, nl_in = false) {
    const editor = document.getElementById("editor_text");
    const start = editor.selectionStart;
    const end = editor.selectionEnd;
    const before = editor.value.substring(0, start);
    const after = editor.value.substring(end);
    var content = "";

    /* use the button title as the default content */
    if (start !== end) {
        content = editor.value.substring(start, end);
    } else {
        if (self.title) {
            content = self.title;
        } else {
            content = self.innerText;
        }
    }

    /* insert newline inside the selection if needed */
    if (nl_in) {
        content = content.replace(/\n/mg, postamble + "\n" + preamble);
    }

    /* insert newline outside the selection if needed */
    if (nl_out) {
        if (!before.endsWith("\n")) {
            preamble = "\n" + preamble;
        }
        if (!after.startsWith("\n")) {
            postamble = postamble + "\n";
        }
    }

    /* insert the markdown element */
    editor.value = before + preamble + content + postamble + after;

    /* set the text selection to the content */
    editor.selectionStart = start + preamble.length;
    editor.selectionEnd = editor.selectionStart + content.length;

    /* resize the editor and set the focus */
    autosize.update(editor);
    editor.focus();
}
