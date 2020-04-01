#! /usr/bin/env python3

from random import randint

def main():
    f = open('weblog.txt', 'r')
    line = f.readline()
    # limit = 0
    while line != '':
        if (randint(0, 15) == 0):
            print(line, end='')
        line = f.readline()
        # limit += 1

if __name__ == '__main__':
    main()
