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

   Richard Lobb, 22 August 2014.
'''

from collections import defaultdict
import os

CSV_FILE = 'sq3responses.csv'
QUESTION_NUM = 5
EXACT_COPIES_ONLY = False
IGNORE_IDENTIFIERS = True  # If true, all non-keyword identifiers are replaced by '###'
LANGUAGE = 'python'

# Remaining constants are not intended to be user-configured.

RESPONSE = 'Response ' + str(QUESTION_NUM)
LANGUAGE_EXTENSIONS = {
    'python': '.py',
    'c'     : '.c',
    'matlab': '.m'
}

ONE_LINE_COMMENTS = {
    'python'    : '#[^\n]*',
    'c'         : '//[^\n]*',
    'matlab'    : '%[^\n]*'
}

MULTI_LINE_COMMENTS = {
    'python'    : "'''.*?'''|\"\"\".*?\"\"\"",
    'c'         : "/\*.*?\*/",
    'matlab'    : "%{.*?}%"
}

# Keyword lists are incomplete but that doesn't matter in this context
KEYWORDS = {
    'python': ['def', 'for', 'if', 'while', 'class', 'return', 'and',
                'pass', 'in', 'try', 'except', 'print', 'input',
                'and', 'from', 'not', 'or', 'else', 'elif'],
    'c'     : ['case', 'switch', 'if', 'for', 'while', 'struct',
                'void', 'typedef', 'int', 'float', 'double', 'char',
                'do', 'else', 'const', 'break', 'long', 'short',
                'signed', 'include', 'define', 'return'],
    'matlab' : ['break', 'case', 'catch', 'continue', 'for', 'function',
                'if', 'return', 'switch', 'try', 'while', 'else']
}

LANGUAGE_EXT = LANGUAGE_EXTENSIONS[LANGUAGE]
KEYWORD_PATTERN = '|'.join(KEYWORDS[LANGUAGE])
ONE_LINE_COMMENT = ONE_LINE_COMMENTS[LANGUAGE]
MULTI_LINE_COMMENT = MULTI_LINE_COMMENTS[LANGUAGE]
IDENTIFIER = "\\b(?!(?:" + KEYWORD_PATTERN + ")\\b)[A-Za-z_][A-Za-z0-9_]*\\b"


#================ Now we begin ===================
def clean(s):
    '''
    Delete comments and blanklines from s.
    Replace all identifiers with 'xxx', collapse all
    whitespace.
    '''
    if not EXACT_COPIES_ONLY:
        s = re.sub(ONE_LINE_COMMENT, '', s)
        s = re.sub(MULTI_LINE_COMMENT, '', s, flags=re.DOTALL)
        if IGNORE_IDENTIFIERS:
            s = re.sub(IDENTIFIER, 'xxx', s)
        s = re.sub('[ \t\n]+', '', s, flags=re.DOTALL)
    return s


def main():
    f = open(CSV_FILE, encoding='utf-8-sig')
    print("COPIES: File '{}', Question {}\n".format(CSV_FILE, QUESTION_NUM))
    rdr = csv.DictReader(f)
    names = {}
    progs = {}
    directory = 'SubmissionsQ' + str(QUESTION_NUM)
    if not os.path.isdir(directory):
        os.mkdir(directory)
    for row in rdr:
        stud = row['Email address'].split('@')[0]
        names[stud] = row['First name'] + ' ' + row['Surname']
        raw_code = row[RESPONSE]
        open(directory + '/' + stud + LANGUAGE_EXT, 'w').write(raw_code)
        code = clean(raw_code)
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
        email_list.append(stud + "@uclive.ac.nz")
    print()
    print("Email list: ", ",".join(email_list))


main()






