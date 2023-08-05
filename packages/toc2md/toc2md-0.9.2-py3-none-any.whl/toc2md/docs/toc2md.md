<style>@media print{h2{page-break-before:always}}</style>
<br><br><br><br><br><br><br><br><br><br><br><br><center>
# `toc2md` User Guide

**Version 0.9.1**

[https://pypi.org/project/toc2md/](https://pypi.org/project/toc2md/)

**Carlo Alessandro Verre**

[carlo.alessandro.verre@gmail.com](mailto:carlo.alessandro.verre@gmail.com)

**july 6, 2020**
</center>

## Contents

- [1. Before Usage](#1.)
    - [1.1. Introduction](#1.1.)
    - [1.2. Installation](#1.2.)
- [2. Usage](#2.)
    - [2.1. Format](#2.1.)
    - [2.2. Logic](#2.2.)
    - [2.3. Example](#2.3.)
    - [2.4. Errors](#2.4.)
- [3. After Usage](#3.)
    - [3.1. PDF From ReText](#3.1.)
    - [3.2. PDF From Firefox](#3.2.)
    - [3.3. PDF From LibreOffice Writer](#3.3.)
- [4. Appendices](#4.)
    - [4.1. Documentation](#4.1.)
    - [4.2. Acronyms](#4.2.)
    - [4.3. Credits](#4.3.)

## <a name="1.">1. Before Usage</a>

### <a name="1.1.">1.1. Introduction</a>

toc2md is a small CLI utility written in Python 3, aimed to insert or update a
nested chapter numbering and a linked table of contents (TOC) into a Markdown
(MD) file.

"Nested chapter numbering" means level 1 chapters gets 1-item numbering (1. 2.
...), level 2 chapters gets 2-item numbering (1.1. 1.2. ...) and so on.

"Linked table of contents" means that if we click on a chapter title in the table of contents then (under given conditions) we jump to chapter body.

To read this document you only need a minimum knowledge of MD and HTML.

In [2. Usage](#2.) we show by rules and examples how to use toc2md, alone or as
a coroutine together with ReText MD editor.

In [3. After Usage](#3.) we discuss three ways to get a PDF document from a MD file.

### <a name="1.2.">1.2. Installation</a>

Be sure you got last `pip` version typing at terminal (without `sudo`):
```
    $ python3 -m pip install --user --upgrade pip
```
Now you can install `toc2md` typing (without `sudo`):
```
    $ python3 -m pip install toc2md
```
## <a name="2.">2. Usage</a>

### <a name="2.1.">2.1. Format</a>

Usage: `toc2md [-h] [-H] [-V] [file]`

Positional argument:

- `file` - MD file to be backed up, read, processed and rewritten

Optional arguments:

- `-h, --help` - show a help message and exit
- `-H, --user-guide` - open User Guide in PDF format and exit
- `-V, --version` - show program's version number and exit

### <a name="2.2.">2.2. Logic</a>

If we type at terminal:
```
    $ toc2md example.md
```
toc2md program:

- copies `example.md` into a timestamped backup file `example-YYYY.mm.dd-HH:MM:SS.md`
- writes on standard output something like:
```
    file '/home/xxxx/example.md' has been backed up
    into '/home/xxxx/example-2020.06.05-18.19.07.md'
```
- reads example.md
- checks correct heading sequence (see below)
- deletes old chapter numbering (if any) and old TOC (if any)
- inserts new nested chapter numbering and new linked TOC
- rewrites the updated version into example.md
- writes on standard output something like:
```
    file '/home/xxxx/example.md' has been updated
```
There is neither configuration file nor options. Logic has been kept as simple
as possible, but the file to be processed must obey some rule, as follows.

toc2md processing is driven by headings in input file. A heading for us is a line
which starts with a '#' character. The heading level is the number of leading '#'
characters, between 1 and 6. So a heading is made by:

- a string of 1 to 6 '#' characters
- a blank
- a title

Title must start with an alphabetic character.

'#' characters after the sixth are silently discarded.

The blank after '#' characters if not present is silently inserted.

Any line not starting with '#' is treated as normal text, including MD headings as:
```
    Something
    ===
```
or HTML headings like:
```
    <h3>Something Else</h3>
```
which are anyway deprecated and **must** be avoided.

Titles in headings are:

- level 1 heading: title of the whole document
- first level 2 heading: title of the TOC
- following level 2 headings: titles of level 1 chapters (as 1. 2. ...)
- level 3 headings: titles of level 2 chapters (as 1.1. 1.2. ...)
- level 4 headings: titles of level 3 chapters (as 1.1.1. 1.1.2. ...)
- level 5 headings: titles of level 4 chapters (as 1.1.1.1. 1.1.1.2. ...)
- level 6 headings: titles of level 5 chapters (as 1.1.1.1.1. 1.1.1.1.2. ...)

So the input file **must** contain the following headings, freely intermixed with
normal text, but in this order:

- one level 1 heading with title of the whole document
- one level 2 heading with title of the TOC
- one level 2 heading with title of the first level 1 chapter (1.)
- zero or more level 2..6 headings with titles of level 1..5 chapters

**Beware: no** heading can **ever** have a level higher than that of the previous
heading plus one.

Each non-heading line in input is transcribed as it is into output, except for
those between the first and second level 2 headings. These lines are supposed to
be the old TOC and hence are deleted and replaced in output by the new TOC.

Chapter numbering in input headings is deleted and replaced in output by the new
chapter numbering.

### <a name="2.3.">2.3. Example</a>

An example will make everything clearer. As MD editor we will use ReText.

**Beware**: from another MD editor you could get a different behavior.

We open a terminal window and type:
```
    $ retext example.md &
```
The '&' forks ReText as a separate process allowing us to use concurrently the
terminal window and the ReText window.

In ReText window we write:

![example0.md.png](example0.md.png)

We save (by clicking **File &#8594; Save**, or typing **Ctrl+S**, or clicking the **[&#8595;]** button), then on terminal window we run:
```
    $ toc2md example.md
```
and the text in ReText window magically becomes:

![example1.md.png](example1.md.png)

Note in the newly created TOC the links pointing to chapter headings.

**Beware**: if after running '`toc2md example.md`' ReText opens a dialog sub-window
like this:

![error.png](error.png)

don't click **[Reload]**! The sub-window means you forgot to save! Click
**[X Cancel]** (maybe twice) on sub-window, save ReText window, and run '`toc2md
example.md`' in the terminal window again.

Now we realize Cats eat Mice, Frogs like Rains, and after Rains the Sun comes,
so we insert Mice in Cats, Frogs between Cats and Dogs, and Sun after Rains.

![example2.md.png](example2.md.png)

As before, we save ReText window and we run '`toc2md example.md`' in terminal window,
so the text in ReText window becomes:

![example3.md.png](example3.md.png)

Done!

### <a name="2.4.">2.4. Errors</a>

toc2md can fail with one of the following error messages:
```
    ERROR: no file
    ERROR: file '...' has no '.md' extension
    ERROR: file '...' not found
    ERROR: heading sequence error in line ... '#...'
```

## <a name="3.">3. After Usage</a>

As an example, we will use this same User Manual you are reading, born as `toc2md.md`, edited and processed concurrently by Retext and toc2md.

![toc2md.md.png](toc2md.md.png)

If we export `toc2md.md` from Retext by **File &rarr; Export &rarr; HTML** into,
say, `toc2md.retext.html` and we open it by Firefox (or any other HTML browser)
links in our TOC work fine as we expected, we click a line in TOC and we
jump on the desired chapter.

![toc2md.retext.html.png](toc2md.retext.html.png)

Now we will explore three different ways to obtain a PDF document from our MD file:

- exporting directly from ReText
- exporting from Firefox via HTML format
- exporting from LibreOffice Writer via HTML format


As you can expect, from a more complex procedure we will get a higher degree of
control and a better final quality.

### <a name="3.1.">3.1. PDF From ReText</a>

We can directly export `toc2md.md` from ReText by
**File &rarr; Export &rarr; PDF** into a file, say `toc2md.retext.pdf`

We get a not-indexed PDF file with page numbers in page bottom right corners and nothing else.

Procedure is instantaneous, control on final result is absent, quality is
suitable for a quick-and-dirty draft:

- links in table of contents do not work
- no way to insert page breaks
- no way to manually format the final result

![toc2md.retext.pdf.png](toc2md.retext.pdf.png)

By the way, if we print directly from ReText by **File &rarr; Print** we obtain
on paper the same result.

### <a name="3.2.">3.2. PDF From Firefox</a>

In order to force page breaks in given points of the final PDF document we can insert a line:
```
    <p style="break-after:page"></p>
```
in all corresponding places of our MD file. Alternatively, we can force a page
break for each heading of a given level by a single line, for example if we
insert:
```
    <style>@media print{h2{page-break-before:always}}</style>
```
as first line of our MD file, then we get a page break before each level 2 heading (level 1 chapter).

**Beware:** These tricks work with Firefox only, while they do not work exporting
our PDF file from ReText or from LibreOffice Writer.

We proceed as follows:

1. we export `toc2md.md` from Retext by **File &rarr; Export &rarr; HTML** into
`toc2md.retext.html`
2. we open toc2md.retext.html HTML file by Firefox
3. optionally we control page headers and footers via
**[&#8801;] button &rarr; Print...&rarr; Print... &rarr; Options &rarr; Header and Footer**
4. optionally we control paper size and other print parameters via
**[&#8801;] button &rarr; Print... &rarr; Print... &rarr; Page Setup**
5. finally we export into toc2md-firefox.pdf by
**[&#8801;] button &rarr; Print... &rarr; Print... &rarr; General &rarr; Print to File &rarr; Print**

Procedure is fast, control of result and final quality are good for printing but not for web publishing:

- as before, links in table of contents do not work
- as before, resulting PDF file is not indexed

![toc2md.firefox.pdf.png](toc2md.firefox.pdf.png)

By the way, if we print directly from Firefox by
**File &rarr; Print... &rarr; Print... &rarr; Print** we obtain on paper the same
result.

### <a name="3.3.">3.3. PDF From LibreOffice Writer</a>

We proceed as follows:

1. we export `toc2md.md` from Retext by **File &rarr; Export &rarr; HTML** into
`toc2md.retext.html`
2. we replace in `toc2md.retext.html` each string **`'<table>'`** with string **`'<table border=1>'`** and we write result in `toc2md.sed.html`, in order to maintain visibility of table borders (see for instance the table in [4.2. Acronyms](#4.2.))
3. open `toc2md.sed.html` by LibreOffice Writer
4. make changes at our taste (for instance change text font or alignment,
insert page breaks by **Ctrl-Enter**, insert headers and/or footers with page number, resize or move pictures, or whatever else...)
5. finally export from Writer into `toc2md.writer.pdf` by
**File &rarr; Export As &rarr; Export Directly As PDF**

Step 2. can be performed typing at terminal:
```
    $ sed 's/<table>/<table border=1>/' <toc2md.retext.html >toc2md.sed.html
```
Procedure is a bit cumbersome, control of final result is maximum, result is an indexed, professional-looking PDF file, good for printing and web publishing.

If we open `toc2md.writer.pdf` by a PDF browser:

- the toc2md-generated links in TOC jump perfectly to chapters
- the file is said "indexed" because in the side pane on the left we can view
the "Index", which is a Writer-generated TOC which matches one-to-one the
toc2md-generated TOC and remains visible when we scroll down along the file

![toc2md.writer.png](toc2md.writer.pdf.png "toc2md.writer.pdf.png")

**Beware:** Writer can not distinguish '#'-headings from the others, so the
two TOCs (the Writer-generated at left and the toc2md-generated in the text)
they will only have a one-to-one match if we have avoided entering MD headings
as:
```
    Something
    ===
```
or HTML headings as:
```
    <h3>Something Else</h3>
```
in our MD file.

## <a name="4.">4. Appendices</a>

### <a name="4.1.">4.1. Documentation</a>

If we type at terminal:
```
    $ cd ~/.local/lib/python3.*/site-packages/toc2md/docs
```
we can find all versions of the `toc2md` User Guide discussed in [3. After Usage](#3.):

- `toc2md.md` - original file edited by ReText and toc2md
- `toc2md.retext.html` - exported by ReText, in input to FireFox
- `toc2md.sed.html` - toc2md.retext.html modified by sed, in input to Writer
- `toc2md.retext.pdf` - directly exported by ReText (low quality)
- `toc2md.firefox.pdf` - exported by FireFox from toc2md.retext.html (medium quality)
- `toc2md.writer.pdf` - exported by Writer from toc2md.sed.html (high quality)

Anyway the "official" version of the `toc2md` User Guide is
`toc2md.writer.pdf`. We can view it typing at terminal:
```
    $ toc2md -H
```
### <a name="4.2.">4.2. Acronyms</a>
<p></p>

|INITIALS|MEANING                      |
|--------|-----------------------------|
|CLI     |Command Language Interface   |
|HTML    |HyperText Markup Language    |
|MD      |MarkDown                     |
|ODT     |Open Document Text           |
|PDF     |Page Description Format      |
|PyPI    |Python Package Index         |
|TOC     |Table Of Contents            |
|toc2md  |Table Of Contents to MarkDown|

### <a name="4.3.">4.3. Credits</a>

The `toc2md` project has been:

- developed in [Python](http://www.python.org) 3.8.2
- by [Idle](https://docs.python.org/3/library/idle.html) 3.8.2
- built and published on PyPI thanks to [flit](https://pypi.org/project/flit) 2.3.0
- on [Linux Xubuntu](https://xubuntu.org) 20.04 LTS

This toc2md.pdf file has been:

- written by [ReText](https://pypi.org/project/ReText) 7.1.0
- processed by [toc2md](https://pypi.org/project/toc2md) 0.9.1
- exported from ReText in HTML format and translated into PDF format by
[Firefox](https://www.mozilla.org/en-US/firefox) 76.0.1

During tests we used:

- [ReText](https://pypi.org/project/ReText) 7.1.0 to write MD, HTML and PDF files
- [Firefox](https://www.mozilla.org/en-US/firefox) 76.0.1 and
[LibreOffice Writer](https://www.libreoffice.org) 6.4.3.2 to translate HTML
files into PDF format
- [Atril](https://atril.com) 1.24.0 to check PDF files

