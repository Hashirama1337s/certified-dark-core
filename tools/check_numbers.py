#!/usr/bin/env python
"""check_numbers.py -- every row of NUMBERS.md is checked against the shipped file it names.

A row is  | id | printed | meaning | file | locator |  with locator one of
  `line N`         line N of the file contains the printed string verbatim;
  `key a/b/c`      the JSON value at that key path (list indices allowed) contains the printed string verbatim;
  `external`       a published source outside this repository (named in the file column); not machine-checked.
Run from anywhere:  python tools/check_numbers.py      Exit 1 on any mismatch.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def cell(s):
    s = s.strip()
    return s[1:-1] if s.startswith('`') and s.endswith('`') else s


def main():
    rows = []
    for line in open(os.path.join(ROOT, 'NUMBERS.md'), encoding='utf-8'):
        if not re.match(r'^\| N\d', line):
            continue
        parts = re.split(r'(?<!\\)\|', line.rstrip('\n'))[1:-1]
        if len(parts) != 5:
            sys.exit('bad row: ' + line)
        rows.append([cell(p) for p in parts])
    bad, ext = 0, 0
    cache = {}
    for rid, printed, _, fn, loc in rows:
        printed = printed.replace('\\|', '|')
        if loc == 'external':
            ext += 1
            continue
        path = os.path.join(ROOT, fn)
        if not os.path.exists(path):
            print('%s: missing file %s' % (rid, fn)); bad += 1; continue
        if loc.startswith('line '):
            n = int(loc[5:])
            if path not in cache:
                cache[path] = open(path, encoding='utf-8').read().splitlines()
            ok = n <= len(cache[path]) and printed in cache[path][n - 1]
        elif loc.startswith('key '):
            v = json.load(open(path, encoding='utf-8'))
            for k in loc[4:].split('/'):
                v = v[int(k)] if isinstance(v, list) else v[k]
            ok = printed in (v if isinstance(v, str) else json.dumps(v))
        else:
            ok = False
        if not ok:
            print('%s: %r not found at %s %s' % (rid, printed, fn, loc)); bad += 1
    print('check_numbers: %d rows, %d checked, %d external, %d mismatches' % (len(rows), len(rows) - ext, ext, bad))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
