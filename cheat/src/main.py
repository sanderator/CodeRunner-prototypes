#!/usr/bin/env python3

from cheat import dumbcopiers

def main():
    cheat.foo.main()

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-a', '--answers',
            dest='file', default=False,
            help='student answers file exported from Moodle')
    parser.add_option('-i', '--interface_language',
            dest='interface_language', default='english',
            help='Moodle language: english (default) / french')
    parser.add_option('-q', '--question',
            dest='question_num', default=False,
            help='question number for comparing student codes')
    (options, args) = parser.parse_args()
    optionals = {}
    optionals['file'] = options.file
    optionals['interface'] = options.interface_language
    optionals['question'] = options.question_num
    dumbcopiers.main(optionals)
