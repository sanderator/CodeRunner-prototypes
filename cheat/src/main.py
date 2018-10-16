#!/usr/bin/env python3

from cheat import dumbcopiers

def main():
    cheat.foo.main()

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-c', '--code_language',
            dest='code_language', default='java',
            help='code language: [java (default) | python | c | matlab')
    parser.add_option('-e', '--exact_copies_only', action='store_true',
            dest='exact_copies_only', default=False,
            help='copies must be exactly the same to trigger an alert')
    parser.add_option('-i', '--input_file',
            dest='input_file', default=False,
            help='student answers file exported from Moodle')
    parser.add_option('-m', '--moodle_language',
            dest='moodle_language', default='french',
            help='Moodle language: [english | french (default)]')
    parser.add_option('-o', '--output_dir',
            dest='output_dir', default='/tmp',
            help='directory to hold student answer code files (default /tmp)')
    parser.add_option('-q', '--question',
            dest='question', default=False,
            help='question number for comparing student codes')
    parser.add_option('-r', '--replace_identifiers', action='store_true',
            dest='replace_identifiers', default=False,
            help="all non-keyword identifiers are replaced by '###'")
    (options, args) = parser.parse_args()
    optionals = {}
    optionals['code_language'] = options.code_language
    optionals['exact_copies_only'] = options.exact_copies_only
    optionals['input_file'] = options.input_file
    optionals['moodle_language'] = options.moodle_language
    optionals['output_dir'] = options.output_dir
    optionals['question'] = options.question
    optionals['replace_identifiers'] = options.replace_identifiers
    dumbcopiers.main(optionals)
