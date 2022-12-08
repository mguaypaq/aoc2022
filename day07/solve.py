#!/usr/bin/python3
"""
Advent of Code 2022 -- Day 7

>>> part1(TEST_INPUT)
95437
>>> part2(TEST_INPUT)
Traceback (most recent call last):
...
NotImplementedError
>>> print(parse(TEST_INPUT))
- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - j (file, size=4060174)
    - d.log (file, size=8033020)
    - d.ext (file, size=5626152)
    - k (file, size=7214296)
"""

import re
import sys

TEST_INPUT = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""


class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def _str_lines(self, depth):
        yield depth * '  ' + f'- {self.name} (file, size={self.size})'


class Dir:
    def __init__(self, name, parent=None):
        self.name = name
        self.size = None
        self._parent = parent
        self._subdir = {}
        self._ls = None

    def parent(self):
        if self._parent is None:
            raise ValueError('no parent')
        return self._parent

    def subdir(self, name):
        try:
            return self._subdir[name]
        except KeyError:
            if self._ls is None:
                new = self._subdir[name] = Dir(name, parent=self)
                return new
            else:
                raise

    def ls(self, contents):
        if self._ls is None:
            subdir = {}
            ls = {}
            for name, size in contents:
                if name in ls:
                    raise ValueError(f'duplicate file name: {name!r}')
                if size is None:  # dir
                    try:
                        child = self._subdir.pop(name)
                    except KeyError:
                        child = Dir(name, parent=self)
                    subdir[name] = ls[name] = child
                else:  # file
                    ls[name] = File(name, size)
            if self._subdir:
                raise ValueError('visited phantom subdir')
            self._subdir = subdir
            self._ls = ls
        else:
            if contents != [
                (child.name, child.size)
                for child in self._ls.values()
            ]:
                raise ValueError('mismatched ls')

    def validate(self):
        if self._ls is None:
            raise ValueError('unknown listing')
        for child in self._subdir.values():
            child.validate()

    def du(self):
        for child in self._subdir.values():
            yield from child.du()
        self.size = sum(child.size for child in self._ls.values())
        yield self.size

    def _str_lines(self, depth):
        yield depth * '  ' + f'- {self.name} (dir)'
        for child in self._ls.values():
            yield from child._str_lines(depth + 1)

    def __str__(self):
        return '\n'.join(self._str_lines(0))


cd_root = re.compile(r'\$ cd /')
cd_parent = re.compile(r'\$ cd \.\.')
cd_subdir = re.compile(r'\$ cd (?P<name>.*)')
ls_cwd = re.compile(r'\$ ls')
ls_dir = re.compile(r'dir (?P<name>.*)')
ls_file = re.compile(r'(?P<size>0|[1-9]\d*) (?P<name>.*)')


def parse(input):
    cwd = root = Dir('/')
    lines = iter(input.splitlines())
    try:
        line = next(lines)
        while True:
            if cd_root.fullmatch(line):
                cwd = root
            elif cd_parent.fullmatch(line):
                cwd = cwd.parent()
            elif m := cd_subdir.fullmatch(line):
                cwd = cwd.subdir(m['name'])
            elif ls_cwd.fullmatch(line):
                contents = []
                try:
                    line = next(lines)
                    while not line.startswith('$'):
                        if m := ls_dir.fullmatch(line):
                            contents.append((m['name'], None))
                        elif m := ls_file.fullmatch(line):
                            contents.append((m['name'], int(m['size'])))
                        else:
                            raise ValueError(f'invalid output: {line!r}')
                        line = next(lines)
                except StopIteration:
                    cwd.ls(contents)
                    raise
                cwd.ls(contents)
                continue
            else:
                raise ValueError(f'invalid command: {line!r}')
            line = next(lines)
    except StopIteration:
        root.validate()
        return root


def part1(input):
    root = parse(input)
    return sum(size for size in root.du() if size <= 100_000)


def part2(input):
    raise NotImplementedError


def main(args):
    input = open('input.txt').read()
    if args == ['1']:
        print(part1(input), file=open('output1.txt', 'w'))
    elif args == ['2']:
        print(part2(input), file=open('output2.txt', 'w'))
    else:
        raise ValueError(f'invalid arguments: {args!r}')


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
