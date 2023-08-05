# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import re
import shutil
import typing as typ
import logging
import collections
try:
    import builtins
except ImportError:
    import __builtin__ as builtins
import pathlib2 as pl
range = getattr(builtins, 'xrange', range)
str = getattr(builtins, 'unicode', str)
logger = logging.getLogger('pylint_ignore')
ENTRY_TEMPLATE = """
### Line {lineno} - {entry.msg_id} ({entry.symbol})

- message: {entry.msg_text}
- author : {entry.author}
- date   : {entry.date}
- path   : {entry.path}
{ignored_line}

```
{ctx_src_text}
```


"""
_FILE_HEADER_PATTERN = """
^
    \\#\\#\\s
    File:\\s(?P<path>.+)
$
"""
FILE_HEADER_RE = re.compile(_FILE_HEADER_PATTERN, flags=re.VERBOSE)
_ENTRY_HEADER_PATTERN = """
^
    \\#\\#\\#\\s
    Line\\s(?P<lineno>\\d+)
    \\s-\\s
    (?P<msg_id>\\w\\d+)
    \\s
    \\((?P<symbol>.*)\\)
$
"""
ENTRY_HEADER_RE = re.compile(_ENTRY_HEADER_PATTERN, flags=re.VERBOSE)
_LIST_ITEM_PATTERN = """
^
\\s*-\\s(?P<key>message|author|date|path|ignored)
\\s*:\\s
(?P<value>.*)
$
"""
LIST_ITEM_RE = re.compile(_LIST_ITEM_PATTERN, flags=re.VERBOSE)
_SOURCE_TEXT_PATTERN = """
(```|~~~)(?P<language>\\w+)?
    (
        (?:\\s+(?P<def_lineno>\\d+):\\s(?P<def_line>.*))?
        \\s+\\.\\.\\.
    )?
    (?:\\s+\\d+:\\s?.*)?
    (?:\\s+\\d+:\\s?.*)?
    \\s*\\>\\s+(?P<source_lineno>\\d+):\\s(?P<source_line>.*)
    (?:\\s+\\d+:\\s?.*)?
    (?:\\s+\\d+:\\s?.*)?
    \\s*
(```|~~~)
"""
SOURCE_TEXT_RE = re.compile(_SOURCE_TEXT_PATTERN, flags=re.VERBOSE)
SourceText = typ.NamedTuple('SourceText', [('new_lineno', int), (
    'old_lineno', int), ('source_line', str), ('text', str), ('start_idx',
    int), ('end_idx', int), ('def_line_idx', typ.Optional[int]), (
    'def_line', typ.Optional[str])])
MaybeSourceText = typ.Optional[SourceText]
Key = typ.NamedTuple('Key', [('msg_id', str), ('path', str), ('symbol', str
    ), ('msg_text', str), ('source_line', str)])
Entry = typ.NamedTuple('Entry', [('msg_id', str), ('path', str), ('symbol',
    str), ('msg_text', str), ('author', str), ('date', str), ('ignored',
    typ.Optional[str]), ('srctxt', MaybeSourceText)])


class ObsoleteEntry(Exception):
    pass


Catalog = typ.Dict[Key, Entry]
CONTEXT_LINES = 2
_SRC_CACHE = {}


def read_source_lines(path):
    if path not in _SRC_CACHE:
        if len(_SRC_CACHE) > 2:
            _SRC_CACHE.popitem()
        with pl.Path(path).open(mode='r', encoding='utf-8') as fobj:
            full_src_text = fobj.read()
        _keepends = True
        lines = full_src_text.splitlines(_keepends)
        _SRC_CACHE[path] = lines
    return _SRC_CACHE[path]


def find_source_text_lineno(path, old_source_line, old_lineno):
    old_line_idx = old_lineno - 1
    lines = read_source_lines(path)
    for offset in range(100):
        for line_idx in {old_line_idx - offset, old_line_idx + offset}:
            is_matching_line = 0 <= line_idx < len(lines) and lines[line_idx
                ].rstrip() == old_source_line.rstrip()
            if is_matching_line:
                return line_idx + 1
    raise ObsoleteEntry('source text not found')


def read_source_text(path, new_lineno, old_lineno):
    lines = read_source_lines(path)
    line_idx = new_lineno - 1
    line_indent_lvl = len(lines[line_idx]) - len(lines[line_idx].lstrip())
    start_idx = max(0, line_idx - CONTEXT_LINES)
    end_idx = min(len(lines), line_idx + CONTEXT_LINES + 1)
    src_lines = lines[start_idx:end_idx]
    src_text = ''.join(src_lines)
    source_line = lines[line_idx]
    def_line_idx = None
    def_line = None
    maybe_def_idx = line_idx
    while maybe_def_idx > 0:
        line_text = lines[maybe_def_idx]
        indent_lvl = len(line_text) - len(line_text.lstrip())
        if line_text.strip() and indent_lvl < line_indent_lvl:
            first_token = line_text.lstrip().split()[0]
            if first_token in ('def', 'class'):
                is_defline_before_ctx_src = 0 <= maybe_def_idx < start_idx
                if is_defline_before_ctx_src:
                    def_line_idx = maybe_def_idx
                    def_line = lines[maybe_def_idx]
                break
        maybe_def_idx -= 1
    return SourceText(new_lineno, old_lineno, source_line, src_text,
        start_idx, end_idx, def_line_idx, def_line)


CATALOG_HEADER = """# Catalog file for `pylint-ignore`

This file is parsed by `pylint-ignore` to determine which `pylint` messages are ignored.

The reccomended approach to using `pylint-ignore` is:

- If a message is valid, update your code rather than ignoring the message.
- If a message should always be ignored, to do so via the usual
  `pylintrc` file or `setup.cfg` file rather than this `pylint-ignore.md`
  file.
- If a message should be ignored, write a short comment why it is ok.
- If a message should not be ignored, remove the section.


"""
EntryValues = typ.Dict[str, str]


def _init_entry_item(entry_vals):
    old_ctx_src_text = entry_vals['ctx_src_text']
    old_source_text_match = SOURCE_TEXT_RE.match(old_ctx_src_text)
    if old_source_text_match is None:
        raise ObsoleteEntry('Invalid source text')
    path = entry_vals['path']
    old_source_line = old_source_text_match.group('source_line')
    old_lineno = int(entry_vals['lineno'])
    srctxt = None
    try:
        new_lineno = find_source_text_lineno(path, old_source_line, old_lineno)
        srctxt = read_source_text(path, new_lineno, old_lineno)
        source_line = srctxt.source_line
    except ObsoleteEntry:
        source_line = old_source_line
    catalog_entry = Entry(entry_vals['msg_id'], entry_vals['path'],
        entry_vals['symbol'], entry_vals['message'], entry_vals['author'],
        entry_vals['date'], entry_vals.get('ignored'), srctxt)
    catalog_key = Key(catalog_entry.msg_id, catalog_entry.path,
        catalog_entry.symbol, catalog_entry.msg_text, source_line)
    return catalog_key, catalog_entry


def _dumps_entry(entry):
    srctxt = entry.srctxt
    if srctxt is None:
        lineno = -1
        ctx_src_text = ''
    else:
        lineno = srctxt.new_lineno
        last_ctx_lineno = srctxt.end_idx + 1
        padding_size = len(str(last_ctx_lineno))
        src_lines = []
        def_line = srctxt.def_line
        def_line_idx = srctxt.def_line_idx
        if def_line and def_line_idx:
            def_lineno = def_line_idx + 1
            line = def_line.rstrip()
            src_lines.append('  {0:>{1}}: {2}'.format(def_lineno,
                padding_size, line))
            if def_lineno + CONTEXT_LINES < srctxt.new_lineno:
                src_lines.append('  ...')
        for offset, line in enumerate(srctxt.text.splitlines()):
            src_lineno = srctxt.start_idx + offset + 1
            padded_line = ' ' + line if line.strip() else ''
            if lineno == src_lineno:
                dumps_line = '> {0:>{1}}:{2}'.format(src_lineno,
                    padding_size, padded_line)
            else:
                dumps_line = '  {0:>{1}}:{2}'.format(src_lineno,
                    padding_size, padded_line)
            src_lines.append(dumps_line)
        ctx_src_text = '\n'.join(src_lines)
    ignored_line = '' if entry.ignored is None else '- ignored: {0}'.format(
        entry.ignored)
    entry_text = ENTRY_TEMPLATE.format(entry=entry, lineno=lineno,
        ctx_src_text=ctx_src_text, ignored_line=ignored_line)
    return entry_text.lstrip('\n')


def _parse_ctx_src_text(fence, lines):
    ctx_src_text_lines = [fence + '\n']
    while True:
        _, next_line = next(lines)
        ctx_src_text_lines.append(next_line)
        is_close_fence = next_line.strip() == fence
        if is_close_fence:
            break
    return ''.join(ctx_src_text_lines)


def _iter_entry_values(catalog_path):
    entry_vals = {}
    with catalog_path.open(mode='r', encoding='utf-8') as fobj:
        lines = iter(enumerate(fobj))
        try:
            while True:
                i, line = next(lines)
                catalog_lineno = i + 1
                if line.startswith('```'):
                    fence = line[:3]
                    entry_vals['ctx_src_text'] = _parse_ctx_src_text(fence,
                        lines)
                    continue
                file_header = FILE_HEADER_RE.match(line)
                entry_header = ENTRY_HEADER_RE.match(line)
                if (file_header or entry_header) and 'msg_id' in entry_vals:
                    yield entry_vals
                    entry_vals = {'path': entry_vals['path']}
                if file_header:
                    rel_path = file_header.group('path')
                    abspath = (catalog_path.parent / rel_path).absolute()
                    entry_vals = {'path': str(abspath)}
                    continue
                if entry_header:
                    entry_vals['catalog_lineno'] = str(catalog_lineno)
                    entry_vals.update(entry_header.groupdict())
                    assert 'msg_id' in entry_vals
                    continue
                list_item = LIST_ITEM_RE.match(line)
                if list_item:
                    entry_vals[list_item.group('key')] = list_item.group(
                        'value')
        except StopIteration:
            pass
    if 'msg_id' in entry_vals:
        yield entry_vals


DEFAULT_CATALOG_PATH = pl.Path('.') / 'pylint-ignore.md'


def load(catalog_path=DEFAULT_CATALOG_PATH):
    if not catalog_path.exists():
        return {}
    catalog = collections.OrderedDict()
    for entry_vals in _iter_entry_values(catalog_path):
        try:
            catalog_key, catalog_entry = _init_entry_item(entry_vals)
            catalog[catalog_key] = catalog_entry
        except ObsoleteEntry:
            pass
        except (KeyError, ValueError) as ex:
            lineno = entry_vals['catalog_lineno']
            path = entry_vals['path']
            logmsg = 'Error parsing entry on line {0} of {1}: {2}'.format(
                lineno, path, ex)
            logger.error(logmsg, exc_info=True)
    return catalog


def dumps(catalog):
    seen_paths = set()
    catalog_chunks = [CATALOG_HEADER]
    entries = [e for e in catalog.values() if e.srctxt]
    entries.sort(key=lambda e: (e.path, e.srctxt and e.srctxt.new_lineno, e
        .msg_text))
    pwd = pl.Path('.').absolute()
    for entry in entries:
        if entry.path not in seen_paths:
            rel_path = pl.Path(entry.path).absolute().relative_to(pwd)
            catalog_chunks.append('## File: {0}\n\n'.format(rel_path))
            seen_paths.add(entry.path)
        catalog_chunks.append(_dumps_entry(entry))
    return ''.join(catalog_chunks)


def dump(catalog, catalog_path=DEFAULT_CATALOG_PATH):
    catalog_text = dumps(catalog)
    tmp_path = catalog_path.parent / (catalog_path.name + '.tmp')
    with tmp_path.open(mode='w', encoding='utf-8') as fobj:
        fobj.write(catalog_text)
    shutil.move(str(tmp_path), str(catalog_path))
