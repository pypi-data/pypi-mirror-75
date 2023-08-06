#!/usr/bin/python
from subprocess import PIPE, run


def main():
    proc = run(['pacman', '-Qi'], stdout=PIPE, stderr=PIPE)
    out = proc.stdout.decode("utf-8").strip()

    def dec(size):
        n, m = size.split()
        if m.startswith('K'):
            m = 1000
        elif m.startswith('M'):
            m = 1000000
        else:
            m = 1
        return int(float(n)*m)

    raw = []
    for line in out.split('\n'):
        if line.startswith('Name'):
            name = line.split(':')[1].strip()
        if 'Size' in line:
            size = line.split(':')[1].strip()
            raw.append((dec(size), name))

    for size, name in sorted(raw)[-22:]:
        print(f'{size} {name}')


if __name__=='__main__': main()
