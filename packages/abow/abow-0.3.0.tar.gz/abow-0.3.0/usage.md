# Wiki usage

A wiki allows you to view and edit pages and a Bottle of Wiki is no different.
The navigation bar at the top of the page gives you access to much of the
functionalities.

## Creating a page

To create a new page you can change the last part of the URL of an existing page.
You can also create a [[wiki link|#wiki-links]] to it then click on that link.
Finally you can use the search box in the navigation bar: Type in the name of
the page you want to create and follow the link offered at the bottom of the
search result.

!!! important
    Page name cannot contain slash (`/`) or pipe (`|`) and cannot be empty.

## Editing a page

Click the edit link in the navigation bar to modify a page. When editing, use
the **Preview** button to check the results of your modifications. Use the
**Save** button if you are happy with your changes, or  the **Cancel** button to
discard them.

## Renaming a page

When editing a page, use the **New page name** field to change its name and
press **Save** to rename it.

## Deleting a page

Empty pages are deleted. So to delete a page: edit it, delete all its content
and save it.

## Page tags

Tags help you organize your wiki by letting you add labels to the pages and
search pages having those labels.

When editing a page, you have the possibility to add tags to it with the
dedicated input box. The tags are separated by comma (`,`) or semi-colon(`;`).
Once saved, the tags are displayed at the bottom of the page like the
following example:

[[tag1|action:tag/tag1]]{: .badge .badge-pill .badge-secondary}

Like this example, each tag is a link giving you access to the list of
identically tagged pages. You can also create a link to the list of tagged pages
with an [[action link|#wiki-links]].

# Syntax

A Bottle of Wiki uses the markdown syntax with some extensions. See below for
the details. You can also use any HTML tags in a page. When editing a page, the
editor toolbar gives you access to the most common elements of the syntax.

## Paragraphs

Markdown replaces the carriage return in your text with space and continue the
paragraph. To start a new paragraph, separate it from the previous one with
a blank line. To insert a line break inside a paragraph, end a line with
either at least two spaces or a backslash (`\`).

Example:

=== "Markdown"
    ```md
    This is my
    first paragraph.

    This is my second paragraph with a  
    two spaces line break.

    And this is my third paragraph \
    with a backslash line break.
    ```

=== "Rendered output"
    This is my
    first paragraph.

    This is my second paragraph with a  
    two spaces line break.

    And this is my third paragraph \
    with a backslash line break.

## Text styles

Styling the text is done by enclosing it in special characters detailed below.

| Markdown                                | Rendered output      |
|-----------------------------------------|----------------------|
| `__Bold__` or `**Bold**`                | __Bold__ or **Bold** |
| `_Italic_` or `*Italic*`                | _Italic_ or *Italic* |
| `~~Strike though~~`                     | ~~Strike though~~    |
| `^^Underline^^`                         | ^^Underline^^        |
| `` `Inline code` `` ^_1_^               | `Inline code`        |
| `==Mark==`                              | ==Mark==             |
| `^Superscript^`                         | ^Superscript^        |
| `~Subscript~`                           | ~Subscript~          |
| `++ctrl+alt+delete++` ^_2_^             | ++ctrl+alt+delete++  |

_^1^:_ To use backticks in inline code, enclose it with double backticks.

_^2^:_ Keyboard key presses. See the
[documentation](https://facelessuser.github.io/pymdown-extensions/extensions/keys/)
for details.

## Headings

Headings help you organize your text. They also give you faster access to
portion of it: each heading gets an anchor link and an entry in the table of
content. The anchor link is shown when hovering the mouse over a heading.

To create a heading, start with one or more number sign (`#`) on a new line:

| Markdown                | Rendered output                      |
|-------------------------|--------------------------------------|
| `# Heading level 1`     | <h2 class="m-0">Heading level 1</h2> |
| `## Heading level 2`    | <h3 class="m-0">Heading level 2</h3> |
| `### Heading level 3`   | <h4 class="m-0">Heading level 3</h4> |
| `#### Heading level 4`  | <h5 class="m-0">Heading level 4</h5> |
| `##### Heading level 5` | <h6 class="m-0">Heading level 5</h6> |

!!! note
    * The top-most HTML heading `<h1>` is used by the page title, so markdown
    headings are rendered starting from `<h2>`.
    * Only the top four headings are displayed in the table of content and get
    an anchor link.

## Lists

The different types of list supported are detailed below.

!!! note
    Lists can be nested by indenting them with four spaces.

### Ordered lists

An ordered list starts with a number followed by a period in front of each list
item. You don't have to do the numbering yourself but you have to start with
the number one.

Example:

=== "Markdown"
    ```md
    1. Item one
    2. Item two
        1. Sub-item one
        1. Sub-item two (note the numbering)
    3. Item three
    ```

=== "Rendered output"
    1. Item one
    2. Item two
        1. Sub-item one
        1. Sub-item two (note the numbering)
    3. Item three

### Unordered lists

An unordered list starts with a dash (`-`), an asterisk (`*`) or a plus sign
(`+`) in front of each list item. They can be mixed in the same list.

Example:

=== "Markdown"
    ```md
    - Item one
    - Item two
        * Sub-item one
        + Sub-item two
    * Item three
    ```

=== "Rendered output"
    - Item one
    - Item two
        * Sub-item one
        + Sub-item two
    * Item three

### Definition lists

A definition list is started by a term on a single line, followed by its
definition on the next line. The definition starts with a colon and a space.
Terms must be separated from the previous definition by a blank line. You can
have more than one definition per term and more than one term per definition.

Example:

=== "Markdown"
    ```md
    Term one
    : A definition of term one

    Term two
    Term three
    : A definition of term two and three

    Term four
    : A definition of term four
    : Another definition of term four
    ```

=== "Rendered output"
    Term one
    : A definition of term one

    Term two
    Term three
    : A definition of term two and three

    Term four
    : A definition of term four
    : Another definition of term four

### Task lists

Task lists are similar to the [[unordered lists|#unordered-lists]] with an
additional pair of square brackets between the list marker and the list item.
The square brackets contains either a space or a `x` to indicated the state of
the task.

Example:

=== "Markdown"
    ```md
    - [ ] Item one
    - [ ] Item two
        * [ ] Sub-item one
        + [X] Sub-item two
    * [x] Item three
    ```

=== "Rendered output"
    - [ ] Item one
    - [ ] Item two
        * [ ] Sub-item one
        + [X] Sub-item two
    * [x] Item three

## External links

External links point to resources outside of the wiki. They are denoted by
an arrow (↗). You can use different types of links to display a text of your
choosing or the actual URL. You can also use reference if you want to use
the same URL in multiple places. An optional title can be added.

| Markdown                                        | Rendered output                               |
|-------------------------------------------------|-----------------------------------------------|
| `[example](http://example.com/)`                | [example](http://example.com/)                |
| `[example](http://example.com/ "with a title")` | [example](http://example.com/ "with a title") |
| `<http://example.com/>`                         | <http://example.com/>                         |
| `<email@example.com>`                           | <email@example.com>                           |
| `[example with reference][1]`                   | [example with reference][1]                   |
| `[1]: http://example.com/ "the referenced URL"` |                                               |

[1]: http://example.com/ "the referenced URL"

!!! note
    You can place the referenced URL anywhere in the page but it must be
    at the beginning of a line.

## Wiki links

Wiki links are all the links to another part of the wiki. The syntax uses double
brackets with an optional label: `[[target]]` or `[[label|target]]`. The target
can be a page name, an anchor link or an action detailed in the following
examples. Wiki links to missing page are displayed in a different color.

=== "Markdown"
    ```md
    * [[usage]]
    * [[Help page|usage]]
    * [[example of a wiki link to a missing page]] (unless you follow the link and create the page)
    * Anchor link inside the current page: [[#wiki-links]]
    * Anchor link to another page: [[Wiki links|usage#wiki-links]]
    * [[Edit usage|action:edit/usage]]
    * [[All the pages|action:search/pages]]
    * [[List of pages tagged some_tag|action:tag/some_tag]]
    * [[List of pages containing "some text"|action:search/pages?text=some text]]
    ```

=== "Rendered output"
    * [[usage]]
    * [[Help page|usage]]
    * [[example of a wiki link to a missing page]] (unless you follow the link and create the page)
    * Anchor link inside the current page: [[#wiki-links]]
    * Anchor link to another page: [[Wiki links|usage#wiki-links]]
    * [[Edit usage|action:edit/usage]]
    * [[All the pages|action:search/pages]]
    * [[List of pages tagged some_tag|action:tag/some_tag]]
    * [[List of pages containing "some text"|action:search/pages?text=some text]]

## Images

Although a Bottle of Wiki have no provision for file upload, it can still
display images hosted externally. The syntax for inserting images is similar to
the definition of [[external links|#external-links]] with an exclamation mark
(`!`) at the beginning. The alternate text inside bracket is used in situation
where the image cannot be displayed (e.g. screen-reader).

For example:

=== "Markdown"
    ```md
    ![logo of A Bottle of Wiki](../static/img/abow.svg "A Bottle of Wiki")
    ```

=== "Rendered output"
    ![logo of A Bottle of Wiki](../static/img/abow.svg "A Bottle of Wiki")

!!! tip
    If you need to set the dimension of the image, you use the html tag `<img>`
    directly or add an [[attribute list|#attribute-lists]] to define the width
    and height.

## Code block

Code blocks allow you to insert multiple lines of code in your pages. You can
create one by indenting the code with four or more spaces, or you can use
fences. Fences are three or more backticks (`` ``` ``) or tildes (`~~~`) around
the code block.

Example:

=== "Markdown"
    ````md
        Indented
        code block

    ```
    Fenced
    code block
    ```
    ````

=== "Rendered output"

        Indented
        code block

    ```
    Fenced
    code block
    ```

With fences you don't need to indent the code and you can do much more, such as
defining the code language for syntax highlighting and adding line numbering.
Read below and consult the
[documentation](https://facelessuser.github.io/pymdown-extensions/extensions/superfences/)
for details.

### Syntax highlighting

You can define the language used inside the code block by adding it after the
opening fence:

=== "Markdown"
    ````
    ```sh
    #!/bin/sh

    echo "No place like $HOME"
    ```
    ````
=== "Rendered output"
    ```sh
    #!/bin/sh

    echo "No place like $HOME"
    ```

!!! note
    Syntax highlighting is optional and requires
    [Pygments](https://pygments.org/) to be installed to work properly.

    You can run `#!sh pygmentize -L lexers` to get a list of known languages.

### Line numbering and highlighting

Line numbers are controlled by the keyword `linenums` on the opening fence. It
contains up to three numbers:

* The first one is mandatory to get line numbering and defines the starting
  line number.
* The second one defines the step between numbered lines.
* The third one define the step between _special_ lines, that get a different
  style of line number.

Highlighting lines is done with the keyword `hl_lines`. It contains a list of
line numbers to highlight.

=== "Markdown"
    ````md
    ```sh linenums="1" hl_lines="3"
    #!/bin/sh

    echo "No place like $HOME"
    ```
    ````
=== "Rendered output"
    ```sh linenums="1" hl_lines="3"
    #!/bin/sh

    echo "No place like $HOME"
    ```

## Tabbed content

This markdown
[extension](https://facelessuser.github.io/pymdown-extensions/extensions/tabbed/)
allows you to create tabbed content. A tab is started by three equal signs
(`===`) at the beginning of a line, followed by the tab title in double-quotes.
The content of the tab is on the next lines and has to be indented with four
spaces.

Example:

=== "Markdown"
    ```
    === "First tab"
        Tabbed content

        _Still in the same tab because it is indented_

    === "Second tab"
        More tabbed content
    ```
=== "Rendered output"
    === "First tab"
        Tabbed content

        _Still in the same tab because it is indented_

    === "Second tab"
        More tabbed content

## Blockquotes

Blockquotes use the same syntax as email when citing a reply. Each quoted
paragraph starts with a greater-than sign (`>`). To quote multiple paragraphs,
add a `>` on blank lines between them. Blockquotes can be nested by starting
with multiple greater-than signs.

Example:

=== "Markdown"
    ```md
    > Some quote
    >
    > Still the same blockquote after a quoted blank line
    >> Nested blockquote: a quote inside a quote
    ```

=== "Rendered output"
    > Some quote
    >
    > Still the same blockquote after a quoted blank line
    >> Nested blockquote: a quote inside a quote

## Tables

Tables present data in rows and columns. Pipes (`|`) are used to separate each
column, they are optional at the beginning and at the end of each row. The first
row is the header, separated from the rest of the table by three or more dashes
(`---`).

Text alignment of each row can be set by adding a colon (`:`) on either side of
the header separator:

* `:---` is left aligned (the default).
* `---:` is right aligned.
* `:---:` is centered.

You can use text styles inside the table cells. If you need to insert a pipe in
a cell, escape it with a backslash (`\`).

Example:

=== "Markdown"
    ```md
    | default | left | center | right |
    |---------|:---|:---:|---:|
    | Pipe \| | in | a | table |
    |         | **bold** | _italic_ | `code` |
    ```

=== "Rendered output"

    | default | left | center | right |
    |---------|:---|:---:|---:|
    | Pipe \| | in | a | table |
    |         | **bold** | _italic_ | `code` |

!!! note
    You don't need to align the columns in markdown for them to be correctly
    rendered, but you have to make sure that each row contains the same number
    of pipes.

## Horizontal rules

You can use three or more dashes (`---`), asterisks (`***`) or underscores 
(`___`) on a single line to create an horizontal rule. They must be separated
from the rest of the text by blank lines.

Example:

=== "Markdown"
    ```md

    ---

    *****

    ___

    ```

=== "Rendered output"

    ---

    *****

    ___


## Abbreviations

This markdown
[extension](https://python-markdown.github.io/extensions/abbreviations/) gives
you the possibility to define abbreviations. The syntax is shown in the example
below:

=== "Markdown"
    ```md
    ABOW is a very fine wiki.

    *[ABOW]: A Bottle of Wiki
    ```

=== "Rendered output"
    ABOW is a very fine wiki.

*[ABOW]: A Bottle of Wiki

## Attribute lists

This markdown
[extension](https://python-markdown.github.io/extensions/attr_list/) allows you
to add HTML attributes of the elements with the syntax shown below:

```md
{: #id .class key='value1 value2' }
```

* A word starting with a hash (`#`) is used as the id of the element
* Words starting with a dot (`.`) are added to the class of the element
* Key/value pairs are added as attributes to the element

For block elements like paragraphs, the attribute list should be added on the
next line. For other elements, it should be added directly after without space
or newline.

You can use the classes defined by [bootstrap](https://getbootstrap.com/docs/)
to modify the style of some part of your wiki, for example:

=== "Markdown"
    ```md
    This paragraph is muted.
    {: .text-muted }

    [[usage]]{: .badge .badge-primary }
    ```

=== "Rendered output"
    This paragraph is muted.
    {: .text-muted }

    [[usage]]{: .badge .badge-primary }

## Backslash escaping

Some characters (asterisk, dash, underscore ...) have a special meaning in
markdown. If you want to use them directly, you have to escape them with a
backslash (`\`). To make things easier, any character can be escaped. If you
need a literal backslash, escape it with another backslash (`\\`). Backslash
escaping is not needed inside code.

Additionally, escaping a space inserts a non-breaking space (`&nbsp;`) and
escaping a newline inserts a line break (`<br>`).

Example:

=== "Markdown"
    ```md
    \e\s\c\a\p\e \w\i\t\h \\

    \*\*not bold\*\*

    non-breaking\ space

    line\
    break
    ```
=== "Rendered output"
    \e\s\c\a\p\e \w\i\t\h \\

    \*\*not bold\*\*

    non-breaking\ space

    line\
    break

## Markdown inside HTML blocks

While you can insert HTML blocks in your pages, you can also use markdown syntax
inside HTML blocks by adding `markdown="1"` to the opening HTML tag.

Example:

=== "Markdown"
    ```md
    <div markdown="1">
    **Bold** with markdown syntax
    </div>
    ```

=== "Rendered output"
    <div markdown="1">
    **Bold** with markdown syntax
    </div>

See the
[documentation](https://python-markdown.github.io/extensions/md_in_html/)
for more details.

## Admonitions

Admonitions, or notices, make the text they contains stand out. This markdown
[extension](https://python-markdown.github.io/extensions/admonition/) is
inspired by the admonitions in
[reStructuredText](http://docutils.sourceforge.net/docs/ref/rst/directives.html#specific-admonitions).
The syntax is as follow:

```md
!!! type "optional explicit title within double quotes"
    Any number of other indented markdown elements.

    This is the second paragraph inside the admonition because it is indented.
```

The following types of admonitions are defined, identical to reStructuredText:

* attention
* caution
* danger
* error
* hint
* important
* note
* tip
* warning

For example:

=== "Markdown"
    ```md
    !!! note
        A note without an explicit title, so the capitalized type is used as the
        title.

    !!! warning "An example warning without text"

    !!! tip ""
        A tip with a removed title
    ```

=== "Rendered output"
    !!! note
        A note without an explicit title, so the capitalized type is used as the
        title.

    !!! warning "An example warning without text"

    !!! tip ""
        A tip with a removed title

## Footnotes

This [extension](https://python-markdown.github.io/extensions/footnotes/) allows
you to add footnotes in your pages. The footnote labels are enclosed in square
brackets and starts with a caret (`^`). The footnote content use the same label
followed by a colon and a space.

Labels are rendered as links to the footnote contents, located at the end of
the page. Any text can be used as a label, not just numbers.

Example:

=== "Markdown"
    ```md
    This paragraph[^1] contains[^abc] footnote[^2] labels.

    [^1]:
        A very long footnote using indented text.

        Another paragraph of the same footnote.

    [^abc]: A footnote defined by a text label.

    [^2]: Another footnote. Note that the displayed number depends on the order
        of the footnotes.
    ```

=== "Rendered output"
    This paragraph[^1] contains[^abc] footnote[^2] labels.

[^1]:
    A very long footnote using indented text.

    Another paragraph of the same footnote.

[^abc]: A footnote defined by a text label.

[^2]: Another footnote. Note that the displayed number depends on the order
    of the footnotes.
