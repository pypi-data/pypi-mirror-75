In order to install `toc2md`, first be sure you got last `pip` version typing
at terminal (without `sudo`):
```
    $ python3 -m pip install --user --upgrade pip
```
Now you can install `toc2md` typing (without `sudo`):
```
    $ python3 -m pip install toc2md
```
Usage: `toc2md [-h] [-H] [-V] [file]`

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

For further details type at terminal:
```
    toc2md -H
```
Positional argument:

- `file` - MD file to be backed up, read, processed and rewritten

Optional arguments:

- `-h, --help` - show a help message and exit
- `-H, --user-guide` - open User Guide in PDF format and exit
- `-V, --version` - show program's version number and exit
