'''Checks student-submitted Java code.
Can handle multiple modules submitted into Answer, multiple support files,
or some combination of the two. Handles multiple packages.
Handles unittest-ing.

Functions from this module must be imported into a CR template with, eg,
from python_code_checkr import interpret
This file is intended to be a support file for some CR prototype, eg, we use
LOCAL_PROTOTYPE_python_code_checkr

Works (mostly) by:
- filtering out import and from...import... declarations in
  the Answer and .py support files
- replacing everything into one and the same package

Limitations and works-by are sufficient for my current needs;
I may gradually be adding additional stuff.

(cc) CC BY-NC 4.0 2016-2020 Peter Sander
'''

import os
import subprocess
import sys


# arbitrary names
_testfile = 'tester.py'


def _remove_cruft(student_answer, unittesting=False):
    '''Filters the student answer, mostly to get rid of expressions
    and keywords that would be incompatible with all the code being
    smushed into one single file.
    '''
    filtered_student_answer = student_answer \
        .replace('import ', '#import ') \
        .replace('from ', '#from ')
    if unittesting:
        num_main_calls = student_answer.count("if __name__ == '__main__'")
        filtered_student_answer = filtered_student_answer \
            .replace("if __name__ == '__main__'",
                     "if __name__ == '__NOT_MAIN__'",
                     num_main_calls - 1) \
            .replace('''if __name__ == '__main__':
    main()
''', '''if __name__ == '__main__':
    hijack()
''')
    else:
        filtered_student_answer = filtered_student_answer \
        .replace("if __name__ == '__main__'",
                 "if __name__ == '__NOT_MAIN__'")
    return filtered_student_answer


def _add_cruft(student_answer, unittesting=False):
    '''Adds imports if needed for unittesting.
    '''
    return f'''
import unittest
from hijack_unittest import hijack

{student_answer}
''' if unittesting else student_answer


def _assemble_student_answer(student_answer, unittesting=False):
    '''Removes 'unneeded' expressions and adds necessary expressions.
    '''
    return _add_cruft(_remove_cruft(student_answer, unittesting), unittesting)


def _assemble_support_files(ncoding='utf-8'):
    '''Inputs support files, assembles files into a string,
    then filters out cruft.
    '''
    support_files = '\n\n\n'.join([
        open(f, encoding=ncoding).read()
        for f in os.listdir()
        if f.endswith('.py')])
    return _remove_cruft(support_files)


def _assemble_tester(student_answer, testcode, support_files, ncoding='utf-8'):
    '''Smushes student answer and support files together with an
    executable tester class and writes everything out into one file.
    '''
    tester = f'''
{student_answer}
{support_files}
{testcode}
'''

    # write out the string containing all the classes into a file
    with open(_testfile, mode='w', encoding=ncoding) as f:
        print(tester, file=f)


def interpret(student_answer, testcode, unittesting=False, ncoding='utf-8'):
    '''Assembles code (student answer, support files, tester class.
    Then runs the tester code.
    '''
    student_answer = _assemble_student_answer(student_answer, unittesting)
    support_files = _assemble_support_files(ncoding)
    _assemble_tester(student_answer, testcode, support_files)
    if subprocess.call(['python3', _testfile]):
        # code didn't compile
        print('** Further testing aborted **', file=sys.stderr)
