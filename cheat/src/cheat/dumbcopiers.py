#! /usr/bin/env python3

import re
import csv
'''Program to check for nearly-exact copies.
   Reads the quiz results CSV_FILE exported from the quiz server
   (filename CSV_FILE below), extracts the responses for the given
   question (parameter QUESTION_NUM below) and then compares all pairs
   of submissions, printing those that are deemed "equal".

   Unless EXACT_COPIES_ONLY is true, all comments and white space
   are removed. Also, if IGNORE_IDENTIFIERS is True, all non-keyword
   identifiers (roughly) are replaced by 'xxx' before comparison.

   @author: Richard Lobb, 22 August 2014.
   @author: Peter Sander (usability mods)
'''

from collections import defaultdict
import os
from . import EXACT_COPIES_ONLY
from . import IGNORE_IDENTIFIERS
from . import LANGUAGE_EXTENSIONS
from . import ONE_LINE_COMMENTS
from . import MULTI_LINE_COMMENTS
from . import KEYWORDS
from . import HEADERS_LANG


def setup(optionals):
    language = optionals['code_language']
    keyword_pattern = '|'.join(KEYWORDS[language])
    language_stuff = {
        'LANGUAGE_EXT': LANGUAGE_EXTENSIONS[language],
        'ONE_LINE_COMMENT': ONE_LINE_COMMENTS[language],
        'MULTI_LINE_COMMENT': MULTI_LINE_COMMENTS[language],
        'IDENTIFIER': "\\b(?!(?:" + keyword_pattern + ")\\b)[A-Za-z_][A-Za-z0-9_]*\\b"
    }
    return language_stuff


#================ Now we begin ===================
def clean(s, language_stuff, optionals):
    '''
    Delete comments and blanklines from s.
    Replace all identifiers with 'xxx', collapse all
    whitespace.
    '''
    if not optionals['exact_copies_only']:
        s = re.sub(language_stuff['ONE_LINE_COMMENT'], '', s)
        s = re.sub(language_stuff['MULTI_LINE_COMMENT'], '', s, flags=re.DOTALL)
        if optionals['replace_identifiers']:
            s = re.sub(language_stuff['IDENTIFIER'], 'xxx', s)
        s = re.sub('[ \t\n]+', '', s, flags=re.DOTALL)
    return s

def main(optionals):
    language_stuff = setup(optionals)
    input_file = optionals['input_file']
    output_dir = '%s/SubmissionsQ%s' % (optionals['output_dir'], optionals['question'])
    headers = HEADERS_LANG[optionals['moodle_language']]
    first_name = headers['first_name']
    surname = headers['surname']
    response = headers['response'] + ' ' + optionals['question']
    email_address = headers['email']
    f = open(input_file, encoding='utf-8-sig')
    print("COPIES: File '{}', Question {}\n".
            format(input_file, optionals['question']))
    rdr = csv.DictReader(f)
    names = {}
    progs = {}
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    for row in rdr:
        stud = row[email_address].split('@')[0]
        names[stud] = row[first_name] + ' ' + row[surname]
        raw_code = row[response]
        open(output_dir + '/' + stud + language_stuff['LANGUAGE_EXT'], 'w').write(raw_code)
        code = clean(raw_code, language_stuff, optionals)
        progs[stud] = code

    studs = list(progs)
    studs.sort()
    known = set()

    for i, stud in enumerate(studs):
        if progs[stud] == '-': continue
        copiers = []
        for other in studs[i + 1:]:
            if progs[stud] == progs[other] and other not in known:
                copiers.append(other)
                known.add(other)
                known.add(stud)
        if copiers:
            print(stud, names[stud])
            for bod in copiers:
                print('    {} {}'.format(bod , names[bod]))
            print()

    print()
    print("{} students involved in 'collaborating':".format(len(known)))
    email_list = []
    for stud in sorted(known):
        print(' ', stud, names[stud])
        email_list.append(stud + "@etu.unice.fr")
    print()
    print("Email list: ", ",".join(email_list))
